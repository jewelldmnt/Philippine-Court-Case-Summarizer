from nltk.tokenize import RegexpTokenizer
import pandas as pd
import numpy as np
import re
from nltk.tokenize import  sent_tokenize
from transformers import Trainer, TrainingArguments, LEDTokenizer, LEDForConditionalGeneration, AutoModel
from torch.utils.data import DataLoader, Dataset
import transformers
import torch

class preprocess:
    def __init__(self, file_path):
        # Tokenization and cleaning related variable
        self.regex_tokenizer = RegexpTokenizer(r"[a-zA-Z0-9]+|\.(?![a-zA-Z0-9])")
        self.stopwords = ['the','of','to']
        
        # Model related variables
        self.encoder_max_token = 8192
        self.decoder_max_token = 1024
        self.LED_tokenizer = LEDTokenizer.from_pretrained("allenai/led-base-16384")
        self.LED_model = LEDForConditionalGeneration.from_pretrained("allenai/led-base-16384", gradient_checkpointing=True, use_cache=False)
        self.global_mask = []

        # Data related variables
        self.df = pd.read_csv(file_path)
        self.court_cases = []
        self.rulings = []
        self.issues = []
        self.facts = []
        self.led_court = []

        # Actual Data input to the model
        self.encoder_inputs = []
        self.decoder_rulings = []
        self.decoder_issues = []
        self.decoder_facts = []
        self.global_mask = []
        self.final_data = []

        # Unknown token variables
        try:
            with open('unknown_tokens.txt', 'r') as f:
                self.unknown_tokens = f.read().splitlines()
        except:
            self.unknown_tokens = []
        self.found_new_unknown_token = False

        # Preprocess and prepare raw data
        self.df.dropna(inplace=True)
        self.df = self.df.drop_duplicates()
        self.preprocess()
        self.find_unknown_token()
        if self.found_new_unknown_token:
            self.add_tokens_tokenizer_model()
        self.add_globalmask()
        self.prepare_LED_data()

    def return_model_tokenizer_data(self):
        return self.LED_model, self.LED_tokenizer, self.final_data

    def return_visualization_data(self):
        return self.court_cases, self.rulings, self.issues, self.facts

    def prepare_LED_data(self):
        # length of encoder and decoder inputs are the same and should be a list of strings
        for i in range(len(self.encoder_inputs)):
            # Tokenize the input (court case text)
            inputs = self.LED_tokenizer(self.encoder_inputs[i], 
                               max_length=self.encoder_max_token, 
                               padding="max_length", 
                               truncation=True, 
                               return_tensors="pt")
            
            # Tokenize the issues (segmentation)
            issues_output = self.LED_tokenizer(self.decoder_issues[i], 
                                max_length=self.decoder_max_token,
                                padding="max_length", 
                                truncation=True, 
                                return_tensors="pt")

            # Tokenize the issues (segmentation)
            facts_output = self.LED_tokenizer(self.decoder_facts[i], 
                                max_length=self.decoder_max_token,
                                padding="max_length", 
                                truncation=True, 
                                return_tensors="pt")

            # Tokenize the issues (segmentation)
            ruling_output = self.LED_tokenizer(self.decoder_rulings[i], 
                                max_length=self.decoder_max_token,
                                padding="max_length", 
                                truncation=True, 
                                return_tensors="pt")

            # prepare court case input ids
            input_ids = inputs.input_ids
            attention_mask = inputs.attention_mask

            # prepare decoder input ids
            issues_input_ids = issues_output.input_ids.clone()
            facts_input_ids = facts_output.input_ids.clone()
            ruling_input_ids = ruling_output.input_ids.clone()

            # ensure global_attention_mask is padded to the correct length
            global_attention_mask = self.global_mask[i]
            if len(global_attention_mask) < 8192:
                padding_length = 8192 - len(global_attention_mask)
                global_attention_mask = global_attention_mask + [0] * padding_length
    
            global_attention_mask = torch.tensor(global_attention_mask).unsqueeze(0)  # convert to tensor and match input shape
            '''print('court: ',len(input_ids[0]))
            print('issues: ',len(issues[0]))
            print('facts: ',len(facts[0]))
            print('ruling: ',len(ruling[0]))
            print('global_attention_mask: ',len(global_attention_mask[0]))'''  # debugging here

            # prepare final data structure
            data = {
                "input_ids": input_ids,
                "attention_mask": attention_mask,
                "global_attention_mask": global_attention_mask,
                "issues_input_ids": issues_input_ids,
                "facts_input_ids": facts_input_ids,
                "ruling_input_ids": ruling_input_ids
            }

            # append final data
            self.final_data.append(data)
        
        
    def add_globalmask(self):
        '''
        Add global mask to the first tokens of the start of each segment.
        '''
        # Prepare encoder/decoder inputs and global attention mask
        current_label = ''
        for i in range(len(self.court_cases)):
            # instantiate lists for encoder, decoder and attention masks
            list_encoder = []
            list_issues = []
            list_facts = []
            list_ruling = []
            list_attntn = []
    
            for sentence in self.court_cases[i]:  # process each sentence one by one
                # Tokenize each sentence
                token = self.regex_tokenizer.tokenize(sentence)
                token_ids = self.LED_tokenizer.convert_tokens_to_ids(token)  # Convert to token IDs for LED input
                global_attntn = [0] * len(token_ids)  # Initialize global attention for each sentence

                if sentence in self.issues[i]:
                    list_encoder.append(sentence)
                    list_issues.append(sentence)
    
                    if current_label != "<ISSUES>" and len(token) >= 7:
                        # Add special token and set global attention for the first 3 tokens
                        global_attntn = [1] * 2 + [0] * (len(token) - 2)
                    else:
                        global_attntn = [0] * len(token)
                    # Append to decoder inputs and global mask
                    list_attntn.append(global_attntn)
                    current_label = "<ISSUES>"
    
                if sentence in self.facts[i]:
                    list_encoder.append(sentence)
                    list_facts.append(sentence)
    
                    if current_label != "<FACTS>" and len(token) >= 7:
                        # Add special token and set global attention for the first 3 tokens
                        global_attntn = [1] * 3 + [0] * (len(token) - 3)
                    else:
                        global_attntn = [0] * len(token)
                    # Append to decoder inputs and global mask
                    list_attntn.append(global_attntn)
                    current_label = "<FACTS>"
    
                elif sentence in self.rulings[i]:
                    list_encoder.append(sentence)
                    list_ruling.append(sentence)
    
                    if current_label != "<RULING>" and len(token) >= 7:
                        # Add special token and set global attention for the first 3 tokens
                        global_attntn = [1] * 4 + [0] * (len(token) - 4)
                    else:
                        global_attntn = [0] * len(token)
                    # Append to decoder inputs and global mask
                    list_attntn.append(global_attntn)
                    current_label = "<RULING>"

            '''x = ' '.join(list_encoder)
            x = self.regex_tokenizer.tokenize(x)
            y = [attn for attn_list in list_attntn for attn in attn_list]''' # debugging here

            # Concatenate and append strings and attention
            self.encoder_inputs.append(' '.join(list_encoder))  # Combine encoder segments
            self.decoder_rulings.append(' '.join(list_ruling))  # Combine ruling segments
            self.decoder_issues.append(' '.join(list_issues))   # Combine issue segments
            self.decoder_facts.append(' '.join(list_facts))     # Combine fact segments
            self.global_mask.append([attn for attn_list in list_attntn for attn in attn_list])  # Flatten global attention


                
    def add_tokens_tokenizer_model(self):
        '''
        Add unknown token including special tokens to the tokenizer and resize the token embedding of the model.
        '''
        # Add special tokens if not in tokenizer
        special_tokens = ['<RULING>', '<ISSUES>', '<FACTS>']
        if not set(special_tokens).issubset(set(self.unknown_tokens)):
            self.unknown_tokens.extend(special_tokens)
                    
        # Add the new tokens to the tokenizer
        self.tokenizer.add_tokens(self.unknown_tokens)

        # Resize the model's token embeddings to match the new tokenizer length
        self.LED_model.resize_token_embeddings(len(self.tokenizer))

    def find_unknown_token(self):
        '''
        Iterate over each cases, converting the tokens into IDs. Check if there is an unknown token in input_ids
        '''
        for case_tokens in self.court_cases:
            input_ids = self.LED_tokenizer.convert_tokens_to_ids(case_tokens)
            for input_id in input_ids:
                if input_ids == 100 and input_ids not in self.unknown_tokens:
                    print(case_tokens[i]," : ",input_ids[i])
                    self.found_new_unknown_token = True
                    self.unknown_tokens.append(case_tokens[i])

    def preprocess(self):
        '''
        Clean characters and tokenize court cases and segments.
        '''
        # Lowercase the text and Remove unnecessary characters
        self.court_cases = [self.change_char(text.lower()) for text in self.df["whole_text"]]
        self.rulings = [self.change_char(text.lower()) for text in self.df["ruling"]]
        self.facts = [self.change_char(text.lower()) for text in self.df["facts"]]
        self.issues = [self.change_char(text.lower()) for text in self.df["issues"]]
        
        # Tokenize the text, storing words and numbers only
        self.court_cases = [self.regex_tokenizer.tokenize(text) for text in self.court_cases]
        self.rulings = [self.regex_tokenizer.tokenize(text) for text in self.rulings]
        self.facts = [self.regex_tokenizer.tokenize(text) for text in self.facts]
        self.issues = [self.regex_tokenizer.tokenize(text) for text in self.issues]

        # Remove stopwords
        self.court_cases = [self.removestop(token_list) for token_list in self.court_cases]
        self.rulings = [self.removestop(token_list) for token_list in self.rulings]
        self.facts = [self.removestop(token_list) for token_list in self.facts]
        self.issues = [self.removestop(token_list) for token_list in self.issues]

        # Add a filter to accept only lists with tokens lower than 8192
        indices_to_remove = []
        for i in range(len(self.court_cases)):
            if len(self.court_cases[i]) > 8192:
                indices_to_remove.append(i)
        
        # Remove elements from all lists based on indices_to_remove
        for i in reversed(indices_to_remove):
            self.court_cases.pop(i)
            self.rulings.pop(i)
            self.facts.pop(i)
            self.issues.pop(i)

        # Join tokens to form full strings for each case
        self.court_cases = [' '.join(token) for token in self.court_cases]
        self.rulings = [' '.join(token) for token in self.rulings]
        self.facts = [' '.join(token) for token in self.facts]
        self.issues = [' '.join(token) for token in self.issues]
    
        # Split into sentences
        self.court_cases = [sent_tokenize(text) for text in self.court_cases] # text is the whole court case
        self.rulings = [sent_tokenize(text) for text in self.rulings]
        self.facts = [sent_tokenize(text) for text in self.facts]
        self.issues = [sent_tokenize(text) for text in self.issues]

    def removestop(self, token_list):
        """
        Remove stopwords from a list of tokens. Handles case where stopwords are in lower case.
        """
        return [token for token in token_list if token.lower() not in self.stopwords]

    def change_char(self, text):
        """
        Cleans up text by removing or replacing certain characters and patterns.
    
        Args:
            text: A string to be cleaned.
    
        Returns:
            A cleaned version of the string.
        """
        # More specific substitutions first
        text = re.sub(r"\bno\.\b", "number ", text, flags=re.IGNORECASE)  # Replace "no." with "number"
        text = re.sub(r"r.a.", "ra ", text, flags=re.IGNORECASE)    # Replace "R.A." with "ra"
        text = re.sub(r"section (\d+)\.", r"section \1", text) # Replace "section N." with "section N" where N is a number
        text = re.sub(r"sec.", r"sec", text) # Replace "section N." with "section N" where N is a number
        text = re.sub(r"p.d.", r"pd", text) # Replace ".d." with "pd" where N is a number
        text = re.sub(r"no.", r"number", text) # Replace "no." to "number"
        text = re.sub(r"\brtc\b", "regional trial court", text)  # Replace "rtc" with "regional trial court"
        
        # Remove unwanted characters, but keep periods at the end of words
        text = re.sub(r"[(),'\"’”\[\]]", " ", text)   # Remove specific punctuation
    
        # Remove stray or special characters
        text = re.sub(r"[“”]", " ", text)              # Remove “ and ”
        text = re.sub(r"\u2033", " ", text)            # Remove double prime (″)
        text = re.sub(r"\u2032", " ", text)            # Remove prime (′)
        
        # Remove specific meaningless characters
        text = re.sub(r"\bg\b", " ", text)
        text = re.sub(r"\br\b", " ", text)
    
        # Return cleaned text
        return text
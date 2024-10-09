from nltk.tokenize import RegexpTokenizer
import pandas as pd
import numpy as np
import re
from nltk.tokenize import  sent_tokenize
from transformers import Trainer, TrainingArguments, BartTokenizer, BartForSequenceClassification
import transformers
import torch
from sklearn.model_selection import train_test_split
from datasets import Dataset
from nltk.tokenize import sent_tokenize
import IPython.display
from sklearn.utils import resample

class preprocess:
    def __init__(self, file_path):
        # Tokenization and cleaning related variable
        self.regex_tokenizer = RegexpTokenizer(r"[a-zA-Z0-9]+|\.(?![a-zA-Z0-9])")
        
        # Model related variables
        self.max_token = 128
        self.id2label = {0: "rulings", 1: "facts", 2: "issues"}
        self.label2id = {"rulings": 0, "facts": 1, "issues": 2}
        self.BART_tokenizer  = BartTokenizer.from_pretrained("facebook/bart-base")
        self.BART_model  = BartForSequenceClassification.from_pretrained("facebook/bart-base", num_labels=3, 
                                                                      id2label=self.id2label, label2id=self.label2id,
                                                                      problem_type="single_label_classification")

        # Data related variables
        self.df = pd.read_csv(file_path)
        self.two_sentence = []
        self.two_sentence_tokens = []
        self.tokenized_sentences = []
        self.segment_labels = []
        self.data = {}

        # Final preprocessing output
        self.train_dataset = None
        self.eval_dataset = None
        
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
        print('Preprocessing Done!')

        # Find and store unknown tokens
        self.find_unknown_token()
        print('Found Unknown Token!')
        self.set_model_configuration()
        print('Configured Model!')

    def return_model_tokenizer_data(self):
        print('Model configuration: ', self.BART_model.config)
        return self.BART_model, self.BART_tokenizer, self.train_dataset, self.eval_dataset

    def prepare_LED_data(self):
        self.data = {
            'text': self.tokenized_sentences,
            'labels': self.segment_labels,
        }

        self.df = pd.DataFrame.from_dict(self.data)

        train_data, eval_data = train_test_split(self.df, test_size=0.1, random_state=42)

        train_data = Dataset.from_pandas(train_data)
        eval_data = Dataset.from_pandas(eval_data)

        # Map 
        self.train_dataset = train_data.map(
            self.process_data_to_model_inputs,
            batched=True,
            remove_columns=["text", '__index_level_0__']
        )

        self.eval_dataset = eval_data.map(
            self.process_data_to_model_inputs,
            batched=True,
            remove_columns=["text", '__index_level_0__']
        )

        self.train_dataset.set_format(
            type="torch",
            columns=["input_ids", "attention_mask", "labels"],
        )
        self.eval_dataset.set_format(
            type="torch",
            columns=["input_ids", "attention_mask", "labels"],
        )
        print('Prepared Data for LED Model!')

    def process_data_to_model_inputs(self, batch):
        # Tokenize the inputs
        inputs = self.BART_tokenizer(
            batch["text"],
            padding="max_length",
            truncation=True,
            max_length=128,
        )
        # Prepare input IDs and attention masks
        batch["input_ids"] = inputs["input_ids"]
        batch["attention_mask"] = inputs["attention_mask"]

        return batch

    def preprocess(self):
        '''
        Clean characters and tokenize court cases and segments.
        '''
        # Lowercase the text and Remove unnecessary characters
        self.two_sentence = [self.change_char(text.lower()) for text in self.df["heading"]]

        # Tokenize the text, storing words and numbers only
        self.two_sentence_tokens = [self.regex_tokenizer.tokenize(text) for text in self.two_sentence]
        
        # Join tokens to form full strings for each case
        self.two_sentence = [' '.join(token) for token in self.two_sentence_tokens]

        # Create label-to-ID mapping
        label_mapping = {"facts": 0, "issues": 1, "ruling": 2}
        self.segment_labels = [label_mapping[label] for label in self.df["label"]]

        # Tokenize each string into sentences
        self.tokenized_sentences = [sent_tokenize(sentence)[:5] for sentence in self.two_sentence]

        # Add label to each tokenized sentence
        self.segment_labels = [[label] * len(tokens) for label, tokens in zip(self.segment_labels, self.tokenized_sentences)]

        # Flatten the lists while ensuring consistent length between tokenized sentences and segment labels
        filtered_data = [(sentence, label) for sublist, label_sublist in zip(self.tokenized_sentences, self.segment_labels)
                         for sentence, label in zip(sublist, label_sublist) if len(self.regex_tokenizer.tokenize(sentence)) <= self.max_token]
        
        # Remove duplicates by converting to a set and back to a list
        filtered_data = list(set(filtered_data))
        
        # Unzip the filtered data back into separate lists
        self.tokenized_sentences, self.segment_labels = zip(*filtered_data) if filtered_data else ([], [])

        # Convert to lists (if needed)
        self.tokenized_sentences = list(self.tokenized_sentences)
        self.segment_labels = list(self.segment_labels)

        # Balance the labels by upsampling the minority classes
        self.balance_labels()

    def balance_labels(self):
        '''
        Downsample the majority classes to balance the dataset.
        '''
        # Create a DataFrame from tokenized sentences and labels for easy manipulation
        df_balancing = pd.DataFrame({
            'sentence': self.tokenized_sentences,
            'label': self.segment_labels
        })
    
        # Get the count of each class
        label_counts = df_balancing['label'].value_counts()
        min_count = label_counts.min()  # Find the size of the smallest class (change this back, number is used for presentation only)
    
        # Separate the DataFrame by label
        df_facts = df_balancing[df_balancing['label'] == 0]
        df_issues = df_balancing[df_balancing['label'] == 1]
        df_rulings = df_balancing[df_balancing['label'] == 2]
    
        # Downsample the majority classes to match the smallest class
        df_facts_downsampled = resample(df_facts, replace=False, n_samples=min_count, random_state=42)
        df_issues_downsampled = resample(df_issues, replace=False, n_samples=min_count, random_state=42)
        df_rulings_downsampled = resample(df_rulings, replace=False, n_samples=min_count, random_state=42)
    
        # Combine the downsampled dataframes
        df_balanced = pd.concat([df_facts_downsampled, df_issues_downsampled, df_rulings_downsampled])
    
        # Shuffle the dataset to ensure randomness
        df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)
    
        # Update the tokenized sentences and segment labels with the balanced data
        self.tokenized_sentences = df_balanced['sentence'].tolist()
        self.segment_labels = df_balanced['label'].tolist()

        # Clear the output and print value count
        IPython.display.clear_output(wait=True)
        value_counts = df_balanced['label'].value_counts()
        print(value_counts)
        

    def find_unknown_token(self):
        '''
        Iterate over each case, converting the tokens into IDs. Check if there is an unknown token in input_ids.
        '''
        unk_id = self.BART_tokenizer.unk_token_id
        for tokens in self.two_sentence_tokens:
            input_ids = self.BART_tokenizer.convert_tokens_to_ids(tokens)
            for i, token_id in enumerate(input_ids):
                if token_id == unk_id and tokens[i] not in self.unknown_tokens:  # Check if the token is unknown
                    self.found_new_unknown_token = True
                    self.unknown_tokens.append(tokens[i])  # Add the unknown token to the list
        print(f"Added {len(self.unknown_tokens)} new tokens\n")

    def set_model_configuration(self):
        '''
        Configure Model.
        '''
        # Add the new tokens to the tokenizer
        if self.unknown_tokens:
            self.BART_tokenizer.add_tokens(self.unknown_tokens)

        # Resize the model's token embeddings to match the new tokenizer length
        self.BART_model.resize_token_embeddings(len(self.BART_tokenizer))
        
        self.BART_model.config.max_position_embeddings = self.max_token
        # Safely delete generation-related fields
        if hasattr(self.BART_model.config, 'early_stopping'):
            del self.BART_model.config.early_stopping
        if hasattr(self.BART_model.config, 'num_beams'):
            del self.BART_model.config.num_beams
        if hasattr(self.BART_model.config, 'no_repeat_ngram_size'):
            del self.BART_model.config.no_repeat_ngram_size
        if hasattr(self.BART_model.config, 'forced_bos_token_id'):
            del self.BART_model.config.forced_bos_token_id

    def change_char(self, text):
        """
        Cleans up text by removing or replacing certain characters and patterns.
        """
        # Custom cleaning logic
        text = re.sub(r"section (\d+)\.", r"section \1", text)
        text = re.sub(r"sec.", r"sec", text)
        text = re.sub(r"p.d.", r"pd", text)
        text = re.sub(r"\bno.\b", r"number", text)
        text = re.sub(r"\brtc\b", "regional trial court", text)
        text = re.sub(r"[(),'\"’”\[\]]", " ", text)
        text = re.sub(r"[“”]", " ", text)
        text = re.sub(r"\u2033", " ", text)
        text = re.sub(r"\u2032", " ", text)
        text = re.sub(r"\bg\b", " ", text)
        text = re.sub(r"\br\b", " ", text)

        return text
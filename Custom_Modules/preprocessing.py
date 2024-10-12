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
    def __init__(self, file_path, heading_file_path):
        """
        Initializes the preprocessing class by loading the dataset, setting up tokenizers and models, and
        preparing the data for training and evaluation. It also configures the BART model and handles
        missing/duplicate values.

        Parameters:
            file_path (str): Path to the dataset CSV file.

        Class Variables:
            self.max_token: Specifies the maximum number of tokens allowed in a sequence.
            self.id2label: Dictionary that maps numerical IDs to their corresponding label names.
            self.label2id: Dictionary that maps label names to their corresponding numerical IDs.
            self.BART_tokenizer: Initializes the BART tokenizer by loading the pre-trained tokenizer.
            self.BART_model: Initializes the BART model for sequence classification by loading the pre-trained model.
            self.df: Reads a CSV file from the specified file_path into a pandas DataFrame.
            self.two_sentence: List intended to store processed text data.
            self.two_sentence_tokens: List designated to store tokenized versions of the text data in self.two_sentence.
            self.tokenized_sentences: List meant to hold sentences that have been tokenized
            self.segment_labels: List intended to store labels corresponding to segments or sentences within the text data.
            self.data: Dictionary that has the text and labels for further processing or model input.
            self.unknown_tokens: List designed to keep track of tokens that are not recognized by the tokenizer
            self.train_dataset: Placeholder variable intended to hold the training dataset.
            self.eval_dataset: Placeholder variable intended to hold the evaluation dataset.
        """
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
        self.heading_df = pd.read_csv(heading_file_path)
        self.headings = [phrase for phrase in self.heading_df['heading']]
        self.df_balanced = None
        self.two_sentence = []
        self.two_sentence_tokens = []
        self.tokenized_sentences = []
        self.segment_labels = []
        self.data = {}
        self.unknown_tokens = []

        # Final preprocessing output
        self.train_dataset = None
        self.eval_dataset = None

        # Preprocess and prepare raw data
        self.df.dropna(inplace=True)
        self.df = self.df.drop_duplicates('heading')
        self.preprocess()
        print('Preprocessing Done!')

        # Find and store unknown tokens
        self.find_unknown_token()
        self.set_model_configuration()
        print('Model Configured!')

    def return_model_tokenizer_data(self):
        """
        Returns the model, tokenizer, and the preprocessed train and eval datasets.

        Returns:
            BART_model (BartForSequenceClassification): Configured BART model for sequence classification tasks with three labels.
            
            BART_tokenizer (BartTokenizer): Configured Tokenizer used to preprocess and convert input text into token IDs compatible with the BART model.
            
            train_dataset (datasets.Dataset): Preprocessed dataset used for training, consisting of tokenized input sentences and their corresponding labels.
            
            eval_dataset (datasets.Dataset): Preprocessed dataset used for evaluation, consisting of tokenized input sentences and their corresponding labels.
        """
        return self.BART_model, self.BART_tokenizer, self.train_dataset, self.eval_dataset

    def prepare_LED_data(self):
        """
        Prepares the data for training and evaluation by tokenizing the sentences and mapping them
        to the corresponding labels. It also formats the datasets for compatibility with PyTorch.
        """
        self.data = {
            'text': self.tokenized_sentences,
            'labels': self.segment_labels,
        }

        # Convert the data into a dataframe
        self.df = pd.DataFrame.from_dict(self.data)

        train_data, eval_data = train_test_split(self.df, test_size=0.1, random_state=42)

        # Convert into a Dataset class
        train_data = Dataset.from_pandas(train_data)
        eval_data = Dataset.from_pandas(eval_data)

        # Map out and remove the unnecesary columns
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

        # Convert to torch data the specifiec columns
        self.train_dataset.set_format(
            type="torch",
            columns=["input_ids", "attention_mask", "labels"],
        )
        self.eval_dataset.set_format(
            type="torch",
            columns=["input_ids", "attention_mask", "labels"],
        )

    def process_data_to_model_inputs(self, batch):
        """
        Tokenizes and processes a batch of data for model inputs, including input_ids and attention masks.

        Parameters:
            batch (dict): A batch of input sentences and labels.

        Returns:
            batch (dict): Batch with tokenized input_ids and attention_mask.
        """
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
        """
        Preprocesses the raw text data by cleaning, tokenizing, and segmenting sentences. It also balances
        the dataset by handling class imbalance.
        """
        # Remove data that doesnt give that much meaning
        self.remove_noisy_data()

        # Tokenize the text, storing words and numbers only
        self.sentences_tokens = [self.regex_tokenizer.tokenize(text) for text in self.df["heading"]]
        
        # Join tokens to form full strings for each case
        self.sentences = [' '.join(token) for token in self.sentences_tokens]

        # Create label-to-ID mapping
        label_mapping = {"facts": 0, "issues": 1, "ruling": 2}
        self.segment_labels = [label_mapping[label] for label in self.df["label"]]

        # Tokenize each string into sentences
        self.tokenized_sentences = [sent_tokenize(sentence)[:4] for sentence in self.sentences]

        # Add label to each tokenized sentence
        self.segment_labels = [[label] * len(tokens) for label, tokens in zip(self.segment_labels, self.tokenized_sentences)]

        # Flatten the lists while ensuring consistent length between tokenized sentences and segment labels
        filtered_data = [(sentence, label) for sublist, label_sublist in zip(self.tokenized_sentences, self.segment_labels)
                         for sentence, label in zip(sublist, label_sublist) if len(self.regex_tokenizer.tokenize(sentence)) <= self.max_token]
        
        # Unzip the filtered data back into separate lists
        self.tokenized_sentences, self.segment_labels = zip(*filtered_data) if filtered_data else ([], [])

        # Convert to lists (if needed)
        self.tokenized_sentences = list(self.tokenized_sentences)
        self.segment_labels = list(self.segment_labels)

        # Balance the labels by downsampling the majority classes
        self.balance_labels()

    def remove_noisy_data(self):
        """
        Drop unnecesary data, those that may cause noise.
        """
        for index, row in self.df.iterrows():
            token_len = len(self.regex_tokenizer.tokenize(row['heading']))
            
            if (token_len > 8 or row['heading'] in self.headings):
                continue
            else:
                # Mark this row as invalid
                self.df.at[index, 'heading'] = None
        
        # Drop rows where 'heading' is None
        self.df.dropna(subset=['heading'], inplace=True)

    def balance_labels(self):
        """
        Balances the dataset by downsampling majority classes to match the size of the minority class, ensuring
        that all labels are represented equally in the training data.
        """
        # Create a DataFrame from tokenized sentences and labels for easy manipulation
        df_balancing = pd.DataFrame({
            'sentence': self.tokenized_sentences,
            'label': self.segment_labels
        })
    
        # Get the count of each class
        label_counts = df_balancing['label'].value_counts()
        min_count = label_counts.min()  # Find the size of the smallest class
    
        # Separate the DataFrame by label
        df_facts = df_balancing[df_balancing['label'] == 0]
        df_issues = df_balancing[df_balancing['label'] == 1]
        df_rulings = df_balancing[df_balancing['label'] == 2]
    
        # Downsample the majority classes to match the smallest class
        df_facts_downsampled = resample(df_facts, replace=False, n_samples=min_count, random_state=42)
        df_issues_downsampled = resample(df_issues, replace=False, n_samples=min_count, random_state=42)
        df_rulings_downsampled = resample(df_rulings, replace=False, n_samples=min_count, random_state=42)
    
        # Combine the downsampled dataframes
        self.df_balanced = pd.concat([df_facts_downsampled, df_issues_downsampled, df_rulings_downsampled])
    
        # Shuffle the dataset to ensure randomness
        self.df_balanced = self.df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)
    
        # Update the tokenized sentences and segment labels with the balanced data
        self.tokenized_sentences = self.df_balanced['sentence'].tolist()
        self.segment_labels = self.df_balanced['label'].tolist()

        # Clear the output and print value count
        IPython.display.clear_output(wait=True)
        

    def find_unknown_token(self):
        """
        Identifies unknown tokens in the dataset that are not present in the tokenizer's vocabulary and
        adds them to a list of unknown tokens.
        """
        unk_id = self.BART_tokenizer.unk_token_id
        for tokens in self.two_sentence_tokens:
            input_ids = self.BART_tokenizer.convert_tokens_to_ids(tokens)
            for i, token_id in enumerate(input_ids):
                if token_id == unk_id and tokens[i] not in self.unknown_tokens:
                    self.found_new_unknown_token = True
                    self.unknown_tokens.append(tokens[i])

    def set_model_configuration(self):
        """
        Configures the BART model by resizing token embeddings based on the new vocabulary and removing
        unnecessary fields for generation. Adds unknown tokens to the tokenizer if found.
        """
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
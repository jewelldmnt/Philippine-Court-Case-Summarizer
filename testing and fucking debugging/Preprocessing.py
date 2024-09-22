from nltk.tokenize import RegexpTokenizer
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
import re

class preprocess:
    def __init__(self, file_path):
        self.df = pd.read_csv('new_court_cases.csv')
        self.tokenizer = RegexpTokenizer(r"\w+|[^\w\s]+")
        self.court_cases = None
        self.rulings = None
        self.issues = None
        self.facts = None

        # drop null values in the comment
        print("shape of initial dataframe: ", self.df.shape)
        self.df.dropna(inplace=True)
        print("shape of dataframe when null values were dropped: ", self.df.shape)
        
        # preprocess
        self.preprocess()

        # drop duplicates
        self.df = self.df.drop_duplicates()
        print("shape of dataframe when preprocessed and duplicated values where dropped: ", self.df.shape)
        
        # append to dataframe
        self.df["preprocessed_court_text"] = self.court_cases
        self.df["rulings"] = self.rulings
        self.df["facts"] = self.facts
        self.df["issues"] = self.issues

    def preprocess(self):
        # lowercase the text
        self.court_cases = [text.lower() for text in self.df["whole_text"]]
        self.rulings = [text.lower() for text in self.df["ruling"]]
        self.facts = [text.lower() for text in self.df["facts"]]
        self.issues = [text.lower() for text in self.df["issues"]]
        
        # tokenize the text, storing words only
        self.court_cases = [self.tokenizer.tokenize(text) for text in self.court_cases]
        self.rulings = [self.tokenizer.tokenize(text) for text in self.rulings]
        self.facts = [self.tokenizer.tokenize(text) for text in self.facts]
        self.issues = [self.tokenizer.tokenize(text) for text in self.issues]
        
        # concatenate back to string format
        self.court_cases = [' '.join(tokens) for tokens in self.court_cases]
        self.rulings = [' '.join(tokens) for tokens in self.rulings]
        self.facts = [' '.join(tokens) for tokens in self.facts]
        self.issues = [' '.join(tokens) for tokens in self.issues]

    def split_into_chunks(self):
        pass

    def remove_newlines(self, strings):
          """Removes newline characters from a list of strings using regular expressions.
        
          Args:
            strings: A list of strings.
        
          Returns:
            A new list of strings without newline characters.
          """

          pattern = r"\n"
          return [re.sub(pattern, "", s) for s in strings]

    def give_courtcases(self):
        self.court_cases = self.remove_newlines(self.court_cases)
        return self.court_cases

    def give_rfi(self): # issues muna sa ngayon
        return self.facts
# =============================================================================
# Program Title: Data Preprocessing
# Programmer: Miguel Tolentino, Jewell Anne Diamante
# Date Written: September 29, 2024
# Date Revised: October 16, 2024
#
# Purpose:
#     This program is designed to preprocess legal document datasets to prepare
#     them for input into a finetuned BART model for classification. It performs
#     tokenization, padding, truncation, and cleaning of text data to ensure that
#     the input is in the correct format for the model. The preprocessing steps
#     are tailored for handling legal text documents, ensuring that all relevant
#     information is captured while ensuring efficient model performance.
#
# Where the program fits in the general system design:
#     This program is part of a legal document classification system where
#     preprocessing is a crucial first step before training the model. By transforming
#     raw legal text data into tokenized and clean input, the system ensures that
#     the BART model can learn from well-prepared data, ultimately improving the
#     classification accuracy.
#
# Data Structures, Algorithms, and Control:
#     - Data Structures:
#         - **Dataset (`raw_data`, `preprocessed_data`)**: The `raw_data` consists
#           of legal documents in their original form. The `preprocessed_data` is
#           the tokenized and cleaned dataset that is ready for model input.
#         - **List (`tokens`)**: Stores tokenized text for each document. Each
#           document's text is split into tokens using the BART tokenizer.
#         - **TextField/Tokenize (`BART tokenizer`)**: A tokenizer that converts
#           raw text data into tokenized format compatible with the BART model,
#           handling subword tokenization.
#
#     - Algorithms:
#         - **Text Cleaning**: The preprocessing step includes removing unnecessary
#           characters (e.g., punctuation, special characters), standardizing text
#           (e.g., converting all text to lowercase), and eliminating stopwords
#           and other irrelevant data to focus the model's attention on the most
#           meaningful parts of the legal documents.
#         - **Tokenization**: The BART tokenizer converts raw text into tokens, with
#           each token representing words, subwords, or characters, depending on
#           the model's needs. This step also handles padding and truncation of
#           text sequences to ensure they fit within the model’s maximum sequence
#           length.
#         - **Padding and Truncation**: This step ensures that all tokenized inputs
#           are of uniform length by padding shorter sequences and truncating longer
#           ones to the predefined maximum length set by the BART model. This ensures
#           compatibility with the model’s architecture, which requires inputs of
#           the same size.
#
#     - Control:
#         - The program processes data in a sequential flow: text is first cleaned,
#           then tokenized, followed by padding and truncation. Afterward, the
#           preprocessed data is prepared for input into the model.
#         - Exception handling is applied to ensure the text is clean and properly
#           tokenized, and that the dataset is correctly formatted for the model’s
#           input layer.
# =============================================================================


from nltk.tokenize import RegexpTokenizer
import pandas as pd
import numpy as np
import re
from nltk.tokenize import sent_tokenize
from transformers import BartTokenizer, BartForSequenceClassification
import transformers
import torch
from sklearn.model_selection import train_test_split
from datasets import Dataset
from nltk.tokenize import sent_tokenize
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
import IPython.display
from sklearn.utils import resample


class preprocess:
    def __init__(
        self, file_path=None, heading_file_path=None, is_training=True
    ):
        """
        Initializes the preprocessing class by loading the dataset, setting up 
        tokenizers and models, and preparing the data for training and evaluation. 
        It also configures the BART model and handles missing/duplicate values.

        Parameters:
            file_path (str): Path to the dataset CSV file.

        Class Variables:
            self.BART_tokenizer: Initializes the BART tokenizer by loading the 
                                    pre-trained tokenizer.
            self.df: Reads a CSV file from the specified file_path into a pandas
                                     DataFrame.
            self.heading_df: CSV fiel to be read containing heading tokens.
            self.columns_to_clean: column names to be cleaned
            self.sentence: List intended to store processed text data.
            self.sentence_tokens: List designated to store tokenized versions of 
                                    the text data in self.two_sentence.
            self.tokenized_sentences: List meant to hold sentences that have been 
                                    tokenized
            self.segment_labels: List intended to store labels corresponding to 
                                    segments or sentences within the text data.
            self.data: Dictionary that has the text and labels for further processing 
                                    or model input.
            self.train_dataset: Placeholder variable intended to hold the training 
                                    dataset.
            self.eval_dataset: Placeholder variable intended to hold the evaluation 
                                    dataset.
        """
        if is_training:
            # Tokenization and cleaning related variable
            self.regex_tokenizer = RegexpTokenizer(
                r"[a-zA-Z0-9]+|\.(?![a-zA-Z0-9])"
            )

            # Model related variables
            self.max_token = 128
            self.id2label = {0: "rulings", 1: "facts", 2: "issues"}
            self.label2id = {"rulings": 0, "facts": 1, "issues": 2}
            self.BART_tokenizer = BartTokenizer.from_pretrained(
                "facebook/bart-base"
            )
            self.BART_model = BartForSequenceClassification.from_pretrained(
                "facebook/bart-base",
                num_labels=3,
                id2label=self.id2label,
                label2id=self.label2id,
                problem_type="single_label_classification",
            )

            # Data related variables
            self.df = pd.read_csv(file_path)
            self.heading_df = pd.read_csv(heading_file_path)
            self.label_mapping = {"facts": 0, "issues": 1, "ruling": 2}
            self.segment_heading = [
                phrase for phrase in self.heading_df["heading"]
            ]
            self.segment_heading_labels = [
                self.label_mapping[label] for label in self.heading_df["label"]
            ]
            self.stop_words = set(stopwords.words("english"))
            custom_stopwords = {"s", "g", "r", "gr"}
            self.stop_words.update(custom_stopwords)
            self.headings = []
            self.labels = []
            self.df_balanced = None
            self.sentences = []
            self.sentences_tokens = []
            self.tokenized_sentences = []
            self.segment_labels = []
            self.data = {}
            self.unknown_tokens = []

            # Final preprocessing output
            self.train_dataset = None
            self.eval_dataset = None

            # Clear the output and print value count
            IPython.display.clear_output(wait=True)

            # Preprocess and prepare raw data
            self.df.dropna(inplace=True)

    def paragraph_segmentation(self):
        """
        Extract the paragraph into single lines, while also pre-cleaning the data
        """
        # Loop through each row in the dataframe
        for index, row in self.df.iterrows():
            # Extract lines for each section (facts, issues, ruling) and clean the data
            facts_lines = self.extract_paragraph(
                self.remove_unnecesary_char(row["facts"])
            )
            issues_lines = self.extract_paragraph(
                self.remove_unnecesary_char(row["issues"])
            )
            ruling_lines = self.extract_paragraph(
                self.remove_unnecesary_char(row["ruling"])
            )

            # Add the lines and corresponding labels to the lists
            for line in facts_lines:
                if line.strip() and line not in self.headings:
                    self.headings.append(line)
                    self.labels.append("facts")

            for line in issues_lines:
                if line.strip() and line not in self.headings:
                    self.headings.append(line)
                    self.labels.append("issues")

            for line in ruling_lines:
                if line.strip() and line not in self.headings:
                    self.headings.append(line)
                    self.labels.append("ruling")

        # Create a new dataframe with the headings (lines) and labels
        self.df = pd.DataFrame({"heading": self.headings, "label": self.labels})
        print("Removing Unnecesary Characters Completed")
        print("Paragraph Segmentation Completed")

    def remove_noisy_data(self):
        """
        Drop unnecesary data, those that may cause noise.
        """
        for index, row in self.df.iterrows():
            token_len = len(self.regex_tokenizer.tokenize(row["heading"]))

            # Keep only headings with more than 8 tokens or those specifically allowed in self.headings
            if token_len <= 8:
                if row["heading"] not in self.segment_heading:
                    # Mark this row as invalid
                    self.df.at[index, "heading"] = None

        # Drop rows where 'heading' is None
        self.df.dropna(subset=["heading"], inplace=True)
        print("Removing Noisy Data Completed")

    def tokenize(self):
        """
        Tokenize the data by filtering useful data such as:
            - tokenizing by words and number and sentence enders
            - taking 8 tokens and above only
            - taking the first two sentence and concatenating them
            - mapping the tokens with their labels
        """
        # Tokenize the text, storing words and numbers only
        self.sentences_tokens = [
            self.regex_tokenizer.tokenize(text) for text in self.df["heading"]
        ]

        # Join tokens to form full strings for each case
        self.sentences = [" ".join(token) for token in self.sentences_tokens]

        # Create label-to-ID mapping
        self.segment_labels = [
            self.label_mapping[label] for label in self.df["label"]
        ]

        # Tokenize each string into sentences storing the first two only
        self.tokenized_sentences = [
            sent_tokenize(sentence)[:2] for sentence in self.sentences
        ]

        # Join the two sentence together
        self.tokenized_sentences = [
            " ".join(sentences) for sentences in self.tokenized_sentences
        ]

        # Filter and process data: keep only sentences where the number of tokens > 8
        filtered_data = []
        for sentence, label in zip(
            self.tokenized_sentences, self.segment_labels
        ):
            tokenized_sentence = self.regex_tokenizer.tokenize(sentence)
            if (
                len(tokenized_sentence) > 8 or sentence in self.segment_heading
            ):  # Keep only sentences with more than 8 tokens
                filtered_data.append((sentence, label))

        # Unzip the filtered data back into separate lists
        self.tokenized_sentences, self.segment_labels = (
            zip(*filtered_data) if filtered_data else ([], [])
        )

        # Convert to lists
        self.tokenized_sentences = list(self.tokenized_sentences)
        self.segment_labels = list(self.segment_labels)
        print("Tokenization Completed")

    def balance_labels(self):
        """
        Balances the dataset by downsampling majority classes to match the size 
        of the minority class, ensuring that all labels are represented equally 
        in the training data.
        """
        # Create the DataFrame from tokenized sentences and labels
        df_balancing = pd.DataFrame(
            {"sentence": self.tokenized_sentences, "label": self.segment_labels}
        )

        # Get the count of each class
        label_counts = df_balancing["label"].value_counts()
        print(label_counts)

        # Separate the DataFrame by label
        df_facts = df_balancing[df_balancing["label"] == 0]
        df_issues = df_balancing[df_balancing["label"] == 1]
        df_rulings = df_balancing[df_balancing["label"] == 2]

        # Downsample labels 0 and 2 to 8000 samples each
        df_facts_downsampled = resample(
            df_facts, replace=False, n_samples=8000, random_state=42
        )
        df_rulings_downsampled = resample(
            df_rulings, replace=False, n_samples=8000, random_state=42
        )

        # Upsample label 1 to 8000 samples if needed
        df_issues_upsampled = resample(
            df_issues, replace=True, n_samples=8000, random_state=42
        )

        # Combine the balanced datasets
        self.df_balanced = pd.concat(
            [df_facts_downsampled, df_issues_upsampled, df_rulings_downsampled]
        )

        # Shuffle the dataset to ensure randomness
        self.df_balanced = self.df_balanced.sample(
            frac=1, random_state=42
        ).reset_index(drop=True)
        print(self.df_balanced["label"].value_counts())

        # Update the tokenized sentences and segment labels with the balanced data
        self.tokenized_sentences = self.df_balanced["sentence"].tolist()
        self.segment_labels = self.df_balanced["label"].tolist()

        # Add heading labels
        self.tokenized_sentences = (
            self.tokenized_sentences + self.segment_heading
        )
        self.segment_labels = self.segment_labels + self.segment_heading_labels

        # Update user
        print("Data Balancing Completed")

    def prepare_BART_data(self, tokenizer):
        """
        Prepares the data for training and evaluation by tokenizing the sentences 
        and mapping them to the corresponding labels. It also formats the datasets 
        for compatibility with PyTorch.

        Parameters:
            tokenizer: The configured BART Tokenizer
        """
        self.BART_tokenizer = tokenizer
        self.data = {
            "text": self.tokenized_sentences,
            "labels": self.segment_labels,
        }

        # Convert the data into a dataframe
        self.df = pd.DataFrame.from_dict(self.data)

        train_data, eval_data = train_test_split(
            self.df, test_size=0.1, random_state=42
        )

        # Convert into a Dataset class
        train_data = Dataset.from_pandas(train_data)
        eval_data = Dataset.from_pandas(eval_data)

        # Map out and remove the unnecesary columns
        self.train_dataset = train_data.map(
            self.process_data_to_model_inputs,
            batched=True,
            remove_columns=["text", "__index_level_0__"],
        )

        self.eval_dataset = eval_data.map(
            self.process_data_to_model_inputs,
            batched=True,
            remove_columns=["text", "__index_level_0__"],
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
        Tokenizes and processes a batch of data for model inputs, including input_ids 
        and attention masks.

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

    def extract_paragraph(self, text):
        """
        Description:
            Extracts lines from the input text after preprocessing.

            This function checks if the input text is NaN (not a number). If it 
            is NaN, an empty list is returned. If the text is valid, it is converted 
            to lowercase, preprocessed using the `preprocess_text` function, and 
            then split into individual lines. The resulting lines are returned as 
            a list.

        Parameters:
            text (str or NaN): The input text to be processed, which may be a 
                                string or NaN.

        Returns:
            list: A list of lines extracted from the preprocessed text. Returns 
            an empty list if the input text is NaN.
        """
        if pd.isna(text):  # Check if the text is NaN
            return []
        # Preprocess the text before splitting into lines
        text = text.lower()  # Convert text to lowercase and preprocess
        return str(
            text
        ).splitlines()  # Ensure text is a string before splitting into lines

    def remove_unnecesary_char(self, text: str) -> str:
        """
        Cleans up the text by removing or replacing specific patterns (e.g., 
        punctuation, abbreviations) to standardize the input.

        Parameters:
            text (str): The raw input text.

        Returns:
            text (str): The cleaned and standardized text.
        """
        try:
            # Remove all phrases that start with "(emphasis" or "(citations", 
            # and end with a closing parenthesis.
            text = re.sub(r"\(emphasis[^\)]*\)", "", text)
            text = re.sub(r"\(emphases[^\)]*\)", "", text)
            text = re.sub(r"\(citations[^\)]*\)", "", text)
            text = re.sub(r"emphasis in the original\.", "", text)

            # Replaces the Unicode double prime symbol (″) with a space.
            text = re.sub(r"\u2033", '"', text)

            # Replaces the Unicode prime symbol (′) with a space.
            text = re.sub(r"\u2032", "'", text)

            # Replaces the symbol (’) with (').
            text = re.sub(r"’", "'", text)

            # Replaces the symbol (’) with (').
            text = re.sub(r"”", '"', text)

            # Handles "person's" -> "person" and "peoples'" -> "people"
            text = re.sub(r"(\w+)'s|(\w+)s'", r"\1\2", text)

            # Replaces instances of 'section 1.' (or any number) with 'section 1', 
            # removing the dot after the number.
            text = re.sub(r"section (\d+)\.", r"section \1", text)

            # Replaces 'sec.' with 'sec', removing the period after 'sec'.
            text = re.sub(r"sec\.", r"sec", text)

            # Replaces 'p.d.' with 'pd', removing the periods.
            text = re.sub(r"p\.d\.", r"pd", text)

            # Replaces 'no.' with 'number', changing the abbreviation to the full word.
            text = re.sub(r"\bno\.\b", r"number", text)

            # Replaces the abbreviation 'rtc' with 'regional trial court'.
            text = re.sub(r"\brtc\b", "regional trial court", text)

            # Removes any of the following punctuation characters: ( ) , ' " ’ ” [ ].
            text = re.sub(r"[(),'\"’”\[\]]", " ", text)

            # Removes the special characters “ and ” (different types of quotation marks).
            text = re.sub(r"[“”]", " ", text)

            # Replaces standalone 'g' with a space (possibly targeting abbreviations like 'G').
            text = re.sub(r"\bg\b", " ", text)

            # Replaces standalone 'r' with a space (possibly targeting abbreviations like 'R').
            text = re.sub(r"\br\b", " ", text)

            # Replaces multiple spaces (except for newlines) with a single space.
            text = re.sub(r"([^\S\n]+)", " ", text)

            # Remove single letters or numbers followed by punctuation like a) or 1.
            text = re.sub(
                r"\b[a-zA-Z0-9]\)\s?", "", text
            )  # Matches single letters or digits followed by ')'
            text = re.sub(
                r"\b[a-zA-Z0-9]\.\s?", "", text
            )  # Matches single letters or digits followed by '.'

            # Remove any kind of leading or trailing invisible characters 
            # (including non-breaking spaces)
            text = re.sub(r"^\s*\n", "", text, flags=re.MULTILINE)

            # Removes leading and trailing spaces from the text.
            return text.strip()
        except Exception as e:
            return ""

    def segment_paragraph(self, preprocessed_text: str, original_text: str) -> dict:
        # Split the text into paragraphs based on empty lines
        preprocessed_paragraphs = preprocessed_text.split("\n")
        original_paragraphs = original_text.split("\n")

        # Filter out empty paragraphs and trim any extra spaces
        paragraph_list = [
            paragraph.strip() for paragraph in preprocessed_paragraphs if paragraph.strip()
        ]
        original_paragraph_list = [
            paragraph.strip() for paragraph in original_paragraphs if paragraph.strip()
        ]

        paragraph_dict = {}
        for idx, paragraph in enumerate(paragraph_list):
            # Split the paragraph into sentences using a regex for sentence end markers
            sentences = re.split(r"(?<=[.!?]) +", paragraph)

            # Key is the first 2 sentences, or all sentences if fewer than 2
            key = " ".join(sentences[:2])

            # Value is the entire paragraph
            paragraph_dict[key] = original_paragraph_list[idx]

        return paragraph_dict

    def return_data(self):
        """
        Returns the model, tokenizer, and the preprocessed train and eval datasets.

        Returns:
            train_dataset (datasets.Dataset): Preprocessed dataset used for training, 
                    consisting of tokenized input sentences and their corresponding 
                    labels.

            eval_dataset (datasets.Dataset): Preprocessed dataset used for evaluation, 
                    consisting of tokenized input sentences and their corresponding 
                    labels.
        """
        return self.train_dataset, self.eval_dataset

    def output_csv_file(self, filepath="preprocessed_sentence_label.csv"):
        """
        Outputs a csv file.

        Parameters:
            filepath (str): the file path of the csv file and must end with .csv
        """
        # Output CSV file
        self.df_balanced.to_csv(filepath)

# =============================================================================
# Program Title: BART Model Configuration for Sequence Classification
# Programmers: Miguel Tolentino
# Date Written: September 29, 2024
# Date Revised: October 14, 2024
#
# Purpose:
#     This program is designed to configure and preprocess a BART model for
#     sequence classification tasks. The model classifies text into three
#     categories: 'rulings', 'facts', and 'issues'. It includes the configuration
#     of the BART model and tokenizer, as well as handling unknown tokens that
#     may appear in the input data.
#
#     The goal is to configure a pre-trained BART model for classification tasks,
#     allowing it to classify legal text or other types of documents into predefined
#     categories.
#
# Where the program fits in the general system design:
#     This program is part of a larger pipeline for document classification. It
#     processes the input data by tokenizing and identifying unknown tokens that
#     need to be added to the model's tokenizer. Once the model is configured, it
#     can be used for tasks such as text classification, specifically categorizing
#     legal text into 'rulings', 'facts', and 'issues'.
#
# Data Structures, Algorithms, and Control:
#     - Data Structures:
#         - **Dictionary (`id2label`)**: A mapping from label IDs to label names
#           ('rulings', 'facts', 'issues').
#         - **Dictionary (`label2id`)**: A mapping from label names ('rulings',
#           'facts', 'issues') to label IDs.
#         - **List (`unknown_tokens`)**: A list of tokens that are not found in the
#           tokenizer's vocabulary.
#     - Algorithms:
#         - **Tokenization**: Prepares the input data by converting text into tokens
#           using the BART tokenizer.
#         - **Unknown Token Detection**: Identifies tokens not found in the tokenizer's
#           vocabulary and adds them to the model's tokenizer.
#         - **Model Configuration**: Resizes the model's token embeddings based on
#           the updated vocabulary and removes unnecessary fields for generation.
#     - Control:
#         - The program follows a sequential execution flow: tokenization, unknown
#           token detection, model configuration, and resizing of token embeddings.
#           Error handling is built-in to handle issues such as unknown tokens.
# =============================================================================


from transformers import BartTokenizer, BartForSequenceClassification
import IPython.display

# Clear the output and print value count
IPython.display.clear_output(wait=True)


class model_configure:
    def __init__(self):
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

        # Find and store unknown tokens
        self.unknown_tokens = []

    def return_model_tokenizer(self):
        """
        Returns the model, tokenizer, and the preprocessed train and eval datasets.

        Returns:
            BART_model (BartForSequenceClassification): Configured BART model for 
                    sequence classification tasks with three labels.

            BART_tokenizer (BartTokenizer): Configured Tokenizer used to preprocess 
                    and convert input text into token IDs compatible with the BART model.
        """
        return self.BART_model, self.BART_tokenizer

    def find_unknown_token(self, sentence_tokens):
        """
        Identifies unknown tokens in the dataset that are not present in the 
        tokenizer's vocabulary and adds them to a list of unknown tokens.

        Parameters:
            sentence_tokens: List of tokens of each sentences in the dataset.
        """
        unk_id = self.BART_tokenizer.unk_token_id
        for tokens in sentence_tokens:
            input_ids = self.BART_tokenizer.convert_tokens_to_ids(tokens)
            for i, token_id in enumerate(input_ids):
                if token_id == unk_id and tokens[i] not in self.unknown_tokens:
                    self.found_new_unknown_token = True
                    self.unknown_tokens.append(tokens[i])

    def set_model_configuration(self, sentence_tokens):
        """
        Configures the BART model by resizing token embeddings based on the new 
        vocabulary and removing unnecessary fields for generation. Adds unknown 
        tokens to the tokenizer if found.

        Parameters:
            sentence_tokens: List of tokens of each sentences in the dataset.
        """
        # Clear the output and print value count
        IPython.display.clear_output(wait=True)
        self.find_unknown_token(sentence_tokens)

        # Add the new tokens to the tokenizer
        if self.unknown_tokens:
            self.BART_tokenizer.add_tokens(self.unknown_tokens)

        # Resize the model's token embeddings to match the new tokenizer length
        self.BART_model.resize_token_embeddings(len(self.BART_tokenizer))
        self.BART_model.config.max_position_embeddings = self.max_token

        # Safely delete generation-related fields
        if hasattr(self.BART_model.config, "early_stopping"):
            del self.BART_model.config.early_stopping
        if hasattr(self.BART_model.config, "num_beams"):
            del self.BART_model.config.num_beams
        if hasattr(self.BART_model.config, "no_repeat_ngram_size"):
            del self.BART_model.config.no_repeat_ngram_size
        if hasattr(self.BART_model.config, "forced_bos_token_id"):
            del self.BART_model.config.forced_bos_token_id

        print("Model Configuration Completed")

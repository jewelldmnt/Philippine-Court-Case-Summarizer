# =============================================================================
# Program Title: Topic Segmentation Using Fine-tuned BART Model
# Programmer: Jewell Anne Diamante
# Date Written: October 9, 2024
# Date Revised: October 14, 2024
#
# Purpose:
#     This program leverages a fine-tuned BART (Bidirectional and Auto-Regressive
#     Transformer) model for sequence classification to perform topic segmentation
#     on textual data. It classifies text paragraphs into predefined categories
#     such as 'facts', 'issues', and 'rulings' based on their content. The model's
#     predictions are then used to organize the paragraphs into respective segments
#     and output them in a structured format.
#
# Where the program fits in the general system design:
#     This program fits into a natural language processing (NLP) pipeline where the
#     goal is to segment legal or similar structured documents into meaningful
#     sections. It could be part of a larger system used for document classification,
#     summarization, or information extraction, specifically in contexts like legal
#     case analysis or other structured text domains.
#
# Data Structures, Algorithms, and Control:
#     - Data Structures:
#         - **Dictionary (`tokenized_paragraphs`)**: Holds paragraphs as keys and
#           their respective tokens or content as values. This is used for sequential
#           classification where each paragraph is evaluated individually.
#         - **Dictionary (`predicted_labels_dict`)**: Stores the predicted labels for
#           each paragraph, mapping the content to the predicted category ('facts',
#           'issues', 'rulings').
#         - **Dictionary (`categorized_dict`)**: This dictionary organizes paragraphs
#           into categories based on their predicted labels. The keys are 'facts',
#           'issues', and 'rulings', with values being lists of paragraphs belonging
#           to those categories.
#     - Algorithms:
#         - **Sequence Classification**: The `sequence_classification` method tokenizes
#           input paragraphs, performs inference with the fine-tuned BART model, and
#           assigns labels ('facts', 'issues', 'rulings') to each paragraph based on
#           predicted probabilities. The class also tracks the previous label to avoid
#           shifting classification when the model's confidence is below a specified
#           threshold.
#         - **Label Mapping and Segmentation**: The `label_mapping` function organizes
#           paragraphs into their respective categories ('facts', 'issues', 'rulings')
#           based on predicted labels.
#         - **Writing Output**: The `write_output_segments` function sorts the paragraphs
#           into categories and writes the segmented output into a text file for easy
#           viewing and further processing.
#     - Control:
#         - The program flows sequentially, starting with loading the model, followed
#           by classifying the text, categorizing the paragraphs, and finally writing
#           the categorized output into a text file.
#         - It uses a threshold to ensure that only confident predictions are considered
#           valid. If the model's probability is below the threshold, the program retains
#           the previous label to maintain consistency in the segmentation process.
#         - File operations (reading and writing) are implemented with careful handling
#           to ensure proper encoding and output.
# =============================================================================


import re
import torch
from transformers import BartForSequenceClassification, BartTokenizer
from torch.nn.functional import softmax
from fuzzywuzzy import fuzz
from typing import List, Dict



class TopicSegmentation:
    def __init__(self, model_path: str = "jijemini/case-bart"):
        """
        Description:
            Initialize the TopicSegmentation class with a fine-tuned BART model 
            for sequence classification.

        Parameters:
            model_path (str): The path to the pre-trained or fine-tuned model.
        """
        # Setup labels
        self.id2label = {0: "rulings", 1: "facts", 2: "issues"}
        self.label2id = {"rulings": 0, "facts": 1, "issues": 2}
        self.facts_headings = [
            'facts',
            'antecedents',
            'the antecedents',
            'the factual antecedents',
            'evidence for the prosecution',
            'evidence for the defense',
            'the charges',
            'the defense\'s version',
            'defense\'s version',
            'the prosecution\'s version',
            'proceedings before the court of appeals',
            'the facts',
            'version of the prosecution',
            'version of the defense',
            'the facts and the case'
        ]
        self.issues_headings = [
            'the issue',
            'the issues'
            'the issues presented',
            'the issue before the court',
            'the issues before the court',
            'issue',
            'issues',
            'the present',
            'petition',
            'presented',
        ]
        self.ruling_headings = [
            'ruling of the rtc',
            'ruling of the ca',
            'the ruling of the ca',
            'our ruling',
            'the ruling of the court',
            'the rulings of the court',
            'the ruling of this court',
            'proper penalty',
            'the court\'s ruling',
        ]

        # Load the fine-tuned BART model and tokenizer
        self.model = BartForSequenceClassification.from_pretrained(
            model_path, 
            id2label=self.id2label, 
            label2id=self.label2id,
            problem_type="single_label_classification",
            ignore_mismatched_sizes=True
        )
        self.tokenizer = BartTokenizer.from_pretrained(model_path)
        self.model.eval()  # Set model to evaluation mode

        print("Model id2label:", self.model.config.id2label)
        print("Model label2id:", self.model.config.label2id)


    def is_similar_heading(self, line: str, headings: List[str], threshold: int = 75) -> bool:
        """
        Check if the line is similar to any of the provided headings based on a similarity threshold.
        """
        line_lower = line.lower()
        for heading in headings:
            if fuzz.ratio(line_lower, heading.lower()) >= threshold:
                return True
        return False


    def sequence_classification(
        self, tokenized_paragraphs: dict, threshold: float = 0.0
    ) -> dict:
        """
        Description:
            Performs sequence classification on tokenized paragraphs and assigns 
            labels based on the predicted probabilities.

        Parameters:
            tokenized_paragraphs (dict): A dictionary with paragraph keys and values.
            threshold (float): A threshold for the classification confidence.

        Returns:
            predicted_labels_dict (dict): A dictionary with paragraph keys and 
            their values as lists where:
                - list[0]: Predicted label
                - list[1]: Probability of the predicted label
        """
        predicted_labels_dict = {}
        previous_label = "rulings"  # To keep track of the previous label

        for key, value in tokenized_paragraphs.items():

            if self.is_similar_heading(key, self.facts_headings):
                predicted_label = "facts"
                max_probability = 0.9813336682478882
            elif self.is_similar_heading(key, self.issues_headings):
                predicted_label = "issues"
                max_probability = 0.9813336682478882
            elif self.is_similar_heading(key, self.ruling_headings):
                predicted_label = "rulings"
                max_probability = 0.9813336682478882
            
            else:  
                # Tokenize the input
                inputs = self.tokenizer(
                    key,
                    return_tensors="pt",
                    max_length=128,
                    truncation=True,
                    padding=True,
                )

                # Perform inference
                with torch.no_grad():
                    outputs = self.model(**inputs)

                # Get the predicted label (logits are raw predictions before softmax)
                logits = outputs.logits

                # Calculate softmax probabilities
                probabilities = softmax(logits, dim=-1)

                # Get the predicted class ID and its probability
                predicted_class_id = torch.argmax(probabilities, dim=-1).item()
                max_probability = probabilities[0][predicted_class_id].item()  # Get the max probability

                # Check if the probability is below the threshold
                if max_probability < threshold:
                    predicted_label = previous_label  # Use the previous label if below threshold
                else:
                    id2label = self.model.config.id2label  # Get the label mapping from model config
                    predicted_label = id2label[predicted_class_id]  # Map class ID to label

            # Store the predicted label and probability in the dictionary
            predicted_labels_dict[value] = [predicted_label, max_probability]
            previous_label = predicted_label  # Update previous label for the next iteration

            print(f"Text: {value}\nLabel: {predicted_label}\nProbability: {max_probability}\n\n")

        return predicted_labels_dict


    def label_mapping(self, predicted_labels_dict: dict) -> dict:
        """
        Description:
            Organizes paragraphs into categories (facts, issues, rulings) based on 
            their predicted labels and probabilities.

        Parameters:
            predicted_labels_dict (dict): A dictionary where keys are paragraphs 
                                        (or paragraph snippets) and values are 
                                        lists:
                                        - list[0]: Predicted label (e.g., "facts", 
                                                    "issues", "rulings").
                                        - list[1]: Probability of the predicted label.

        Returns:
            categorized_dict (dict): A dictionary with keys 'facts', 'issues', 
                                    'rulings', and values being lists of tuples 
                                    (paragraph, probability).
        """
        # Initialize the result dictionary with empty lists for each category
        categorized_dict = {"facts": [], "issues": [], "rulings": []}

        # Iterate through the predicted labels dictionary and categorize the paragraphs
        for paragraph, (label, probability) in predicted_labels_dict.items():
            if label == "facts":
                categorized_dict["facts"].append((paragraph, probability))
            elif label == "issues":
                categorized_dict["issues"].append((paragraph, probability))
            elif label == "rulings":
                categorized_dict["rulings"].append((paragraph, probability))

        return categorized_dict


    def write_output_segments(
        self,
        predicted_labels_dict: dict,
        output_file: str = "output_segments.txt",
    ):
        """
        Description:
            Writes the segmented paragraphs into different sections based on 
            their predicted labels.

        Parameters:
            lists as values, where:
                - list[0]: Predicted label (e.g., 'facts', 'issues', 'rulings')
                - list[1]: Probability of the predicted label.
            output_file (str): The output file to write the segmented results.
        """
        facts = []
        issues = []
        rulings = []

        # Sort paragraphs into categories based on their labels
        for key, value in predicted_labels_dict.items():
            label, probability = value  # Unpack the label and probability
            if label == "facts":  # Adjust based on your label names
                facts.append(f"{key} (Probability: {probability:.2f})")
            elif label == "issues":
                issues.append(f"{key} (Probability: {probability:.2f})")
            elif label == "rulings":
                rulings.append(f"{key} (Probability: {probability:.2f})")

        # Write the segmented output to a file
        with open(output_file, "w", encoding='utf-8') as file:
            file.write("FACTS:\n")
            for fact in facts:
                file.write(f"{fact}\n")

            file.write("\nISSUES:\n")
            for issue in issues:
                file.write(f"{issue}\n")

            file.write("\nRULINGS:\n")
            for ruling in rulings:
                file.write(f"{ruling}\n")

        print(f"Output segments written to '{output_file}'.")

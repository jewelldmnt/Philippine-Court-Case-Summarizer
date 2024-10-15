import re
import torch
from transformers import BartForSequenceClassification, BartTokenizer
from torch.nn.functional import softmax

class TopicSegmentation:
    def __init__(self, model_path: str):
        """
        Description:
            Initialize the TopicSegmentation class with a fine-tuned BART model for sequence classification.

        Parameters:
            model_path (str): The path to the pre-trained or fine-tuned model.
        """
        # Load the fine-tuned BART model and tokenizer
        self.model = BartForSequenceClassification.from_pretrained(model_path, ignore_mismatched_sizes=True)
        self.tokenizer = BartTokenizer.from_pretrained(model_path)
        self.model.eval()  # Set model to evaluation mode


    def sequence_classification(self, tokenized_paragraphs: dict, threshold: float = 0.4) -> dict:
        """
        Description:
            Performs sequence classification on tokenized paragraphs and assigns labels based on the predicted probabilities.

        Parameters:
            tokenized_paragraphs (dict): A dictionary with paragraph keys and values.
            threshold (float): A threshold for the classification confidence.

        Returns:
            predicted_labels_dict (dict): A dictionary with paragraph keys and their predicted labels.
        """
        predicted_labels_dict = {}
        previous_label = 'facts'  # To keep track of the previous label

        for key, value in tokenized_paragraphs.items():
            # Tokenize the input
            inputs = self.tokenizer(key, return_tensors="pt", max_length=128, truncation=True, padding=True)
            
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

            # Store the predicted label in the dictionary
            predicted_labels_dict[value] = predicted_label
            print('label:',predicted_label)
            print('key: ',key,'\n')
            previous_label = predicted_label  # Update previous label for the next iteration

        return predicted_labels_dict

    def label_mapping(self, predicted_labels_dict: dict) -> dict:
        """
        Description:
            Organizes paragraphs into categories (facts, issues, ruling) based on their predicted labels.

        Parameters:
            predicted_labels_dict (dict): A dictionary where keys are paragraphs (or paragraph snippets)
                                        and values are their predicted labels (e.g., "facts", "issues", "ruling").

        Returns:
            categorized_dict (dict): A dictionary with keys 'facts', 'issues', 'ruling', and values being lists of paragraphs.
        """
        # Initialize the result dictionary with empty lists for each category
        categorized_dict = {
            "facts": [],
            "issues": [],
            "rulings": []
        }
        print('\n\n')
        # Iterate through the predicted labels dictionary and categorize the paragraphs
        for paragraph, label in predicted_labels_dict.items():
            print('label: ', label)
            print('paragraph: ', paragraph,'\n')
            if label == "facts":
                categorized_dict["facts"].append(paragraph)
            elif label == "issues":
                categorized_dict["issues"].append(paragraph)
            elif label == "rulings":
                categorized_dict["rulings"].append(paragraph)

        return categorized_dict

    def write_output_segments(self, predicted_labels_dict: dict, output_file: str = "output_segments.txt"):
        """
        Description:
            Writes the segmented paragraphs into different sections based on their predicted labels.

        Parameters:
            predicted_labels_dict (dict): A dictionary with paragraphs and their predicted labels.
            output_file (str): The output file to write the segmented results.
        """
        facts = []
        issues = []
        rulings = []

        # Sort paragraphs into categories based on their labels
        for key, label in predicted_labels_dict.items():
            if label == "facts":  # Adjust based on your label names
                facts.append(key)
            elif label == "issues":
                issues.append(key)
            elif label == "rulings":
                rulings.append(key)

        # Write the segmented output to a file
        with open(output_file, "w") as file:
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

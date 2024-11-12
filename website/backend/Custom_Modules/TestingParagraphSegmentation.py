import re
import torch
from transformers import BartForSequenceClassification, BartTokenizer
from torch.nn.functional import softmax


class ParagraphSegmentation:
    def __init__(self, model_path: str):
        """
        Description:
            Initialize the ParagraphSegmentation class with a fine-tuned BART model for sequence classification.

        Parameters:
            model_path (str): The path to the pre-trained or fine-tuned model.
        """
        # Load the fine-tuned BART model and tokenizer
        self.model = BartForSequenceClassification.from_pretrained(
            model_path, ignore_mismatched_sizes=True
        )
        self.tokenizer = BartTokenizer.from_pretrained(model_path)
        self.model.eval()  # Set model to evaluation mode

    def split_paragraph(self, paragraphs: list) -> dict:
        """
        Description:
            Splits each paragraph into the first 2 sentences and returns a dictionary
            where the key is the first 2 sentences, and the value is the full paragraph.

        Parameters:
            paragraphs (list): List of paragraphs to be split.

        Returns:
            dict: A dictionary with first 2 sentences as the key and full paragraph as the value.
        """
        paragraph_dict = {}

        for paragraph in paragraphs:
            # Split the paragraph into sentences using a regex for sentence end markers
            sentences = re.split(r"(?<=[.!?]) +", paragraph)

            # Key is the first 2 sentences, or all sentences if fewer than 2
            key = " ".join(sentences[:2])

            # Value is the entire paragraph
            paragraph_dict[key] = paragraph

        return paragraph_dict

    def sequence_classification(
        self, tokenized_paragraphs: dict, threshold: float = 0.4
    ) -> dict:
        """
        Description:
            Performs sequence classification on tokenized paragraphs and assigns labels based on the predicted probabilities.

        Parameters:
            tokenized_paragraphs (dict): A dictionary with paragraph keys and values.
            threshold (float): A threshold for the classification confidence.

        Returns:
            dict: A dictionary with paragraph keys and their predicted labels.
        """
        predicted_labels_dict = {}
        previous_label = "facts"  # To keep track of the previous label

        for key, value in tokenized_paragraphs.items():
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
            max_probability = probabilities[0][
                predicted_class_id
            ].item()  # Get the max probability

            # Check if the probability is below the threshold
            if max_probability < threshold:
                predicted_label = (
                    previous_label  # Use the previous label if below threshold
                )
            else:
                id2label = (
                    self.model.config.id2label
                )  # Get the label mapping from model config
                predicted_label = id2label[
                    predicted_class_id
                ]  # Map class ID to label

            # Store the predicted label in the dictionary
            predicted_labels_dict[key] = predicted_label
            previous_label = (
                predicted_label  # Update previous label for the next iteration
            )

        return predicted_labels_dict

    def write_output_segments(
        self,
        predicted_labels_dict: dict,
        output_file: str = "output_segments.txt",
    ):
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

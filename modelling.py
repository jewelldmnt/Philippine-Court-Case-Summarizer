from preprocessing_v3 import *
import evaluate
import numpy as np
import torch
from datasets import Dataset
from transformers import AdamW
import time
from transformers import Trainer, TrainingArguments
import evaluate
from sklearn.metrics import accuracy_score, f1_score, recall_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
accuracy = evaluate.load("accuracy")

class Modelling:
    def __init__(self, train_data, eval_data, BART_tokenizer, BART_model):
        self.all_predictions = []
        self.all_labels = []
        self.train_data = train_data
        self.eval_data = eval_data
        self.BART_tokenizer = BART_tokenizer
        self.BART_model = BART_model
        self.accuracy = evaluate.load("accuracy")  # Load the accuracy metric
        
        self.training_args = TrainingArguments(
            output_dir="my_awesome_model",
            learning_rate=5e-5,  # Adjusted learning rate
            per_device_train_batch_size=8,  # Increased batch size
            per_device_eval_batch_size=8,   # Increased eval batch size
            num_train_epochs=1,
            weight_decay=0.01,
            eval_strategy="steps",  # Evaluate every few steps
            eval_steps=500,         # Adjust evaluation frequency
            logging_steps=100,      # Adjust logging frequency
            load_best_model_at_end=True,
            fp16=True,              # Mixed precision training
            gradient_accumulation_steps=2,  # Simulate larger batch sizes
            dataloader_num_workers=4,  # For efficient data loading
        )
        
        self.trainer = Trainer(
            model=self.BART_model,
            args=self.training_args,
            train_dataset=self.train_data,
            eval_dataset=self.eval_data,
            tokenizer=self.BART_tokenizer,
            compute_metrics=self.compute_metrics,
        )

    def train_model(self):
        self.trainer.train()

    def compute_metrics(self, eval_pred):
        try:
            predictions, labels = eval_pred
            try:
                # Ensure predictions and labels are NumPy arrays to safely access their shape
                predictions = np.array(predictions)
                labels = np.array(labels)
                
                print(f"Predictions shape: {predictions.shape}")
                print(f"Labels shape: {labels.shape}\n")
            except AttributeError as e:
                print(f"Error accessing shapes: {e}")
                print(f"Predictions type: {type(predictions)}")
                print(f"Labels type: {type(labels)}")
                return {}
        
            # Handle case where data is smaller and not batched
            if len(predictions.shape) == 1:
                predictions = np.expand_dims(predictions, 0)  # Add batch dimension if missing
            
            if len(predictions.shape) > 2:
                # Apply a reduction if predictions have more than two dimensions (e.g., for sequence classification)
                predictions = predictions[:, 0, :]  # Take the first token's logits for each sequence
        
            # Convert logits to predicted labels
            predictions = np.argmax(predictions, axis=1)
        
            # Handle empty predictions or labels case
            if len(predictions) == 0 or len(labels) == 0:
                return {"accuracy": 0.0, "f1": 0.0, "recall": 0.0}
            
            # Handle case where there's only one class in the labels
            if len(np.unique(labels)) == 1:
                return {"accuracy": 1.0 if (predictions == labels).all() else 0.0}
        
            # Use the loaded accuracy metric from `evaluate`
            accuracy_result = self.accuracy.compute(predictions=predictions, references=labels)
            
            # Compute other metrics using sklearn
            f1 = f1_score(labels, predictions, average='weighted')
            recall = recall_score(labels, predictions, average='weighted')
            
            return {"accuracy": accuracy_result['accuracy'], "f1": f1, "recall": recall}
        except Exception as e:
            print(e)
            return {}


    def calc_accuracy(self):
        # Get the device the model is on (usually 'cuda' if available, otherwise 'cpu')
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Move the model to the device (if not already on it)
        self.BART_model.to(device)
    
        # Assuming eval_dataset is already loaded and tokenized
        for example in self.eval_data:
            # Move input tensors to the same device as the model
            input_ids = example['input_ids'].unsqueeze(0).to(device)  # Add batch dimension (1, sequence_length)
            attention_mask = example['attention_mask'].unsqueeze(0).to(device)  # Add batch dimension (1, sequence_length)
            labels = example['labels'].to(device)
        
            # Prepare inputs for the model
            inputs = {
                'input_ids': input_ids,
                'attention_mask': attention_mask,
            }
        
            # Perform inference
            with torch.no_grad():
                outputs = self.BART_model(**inputs)
        
            # Get the predicted label (logits are raw predictions before softmax)
            logits = outputs.logits
            predicted_class_id = torch.argmax(logits, dim=-1).item()  # Get scalar value
        
            # Store predictions and labels
            self.all_predictions.append(predicted_class_id)
            self.all_labels.append(labels.item())  # Convert tensor to scalar value for labels
            
        self.plot_accuracy()

        
    def plot_accuracy(self):
        # Convert lists to numpy arrays
        self.all_predictions = np.array(self.all_predictions)
        self.all_labels = np.array(self.all_labels)
        
        # Compute accuracy, F1 score, and recall
        accuracy = accuracy_score(self.all_labels, self.all_predictions)
        f1 = f1_score(self.all_labels, self.all_predictions, average='weighted')
        recall = recall_score(self.all_labels, self.all_predictions, average='weighted')
        
        print(f"Accuracy: {accuracy:.4f}")
        print(f"F1 Score: {f1:.4f}")
        print(f"Recall: {recall:.4f}")
        
        # Compute confusion matrix
        conf_matrix = confusion_matrix(self.all_labels, self.all_predictions)
        
        # Plot confusion matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=self.BART_model.config.id2label.values(), yticklabels=self.BART_model.config.id2label.values())
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.title('Confusion Matrix')
        plt.show()

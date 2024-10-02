from transformers import LEDTokenizer, LEDForConditionalGeneration
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AdamW
class dataset(Dataset):
    def __init__(self, data):
        self.data = data
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]

class modelling:
    def __init__(self, model, tokenizer, data, epochs = 3):
        self.data = data
        self.model = model
        self.epochs = epochs
        self.tokenizer = tokenizer
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Move the model to the GPU
        self.model.to(self.device)

        self.optimizer = AdamW(self.model.parameters(), lr=5e-5)  # Adjust learning rate as needed
        self.criterion = torch.nn.CrossEntropyLoss(ignore_index=self.tokenizer.pad_token_id)  # Ignore padding tokens in loss

        # Instantiate the dataset and DataLoader
        self.dataset = dataset(data=self.data)  # Replace with actual preprocessed data
        self.dataloader = DataLoader(self.dataset, batch_size=2, shuffle=True)  # Batch size can be adjusted based on your memory capacity

    def finetune(self):
        self.model.train()  # Put model in training mode

        global_step = 0  # To track the number of steps globally
        start_time = time.time()  # Track start time for runtime calculation
        
        for self.epoch in range(self.epochs):
            epoch_loss  = 0
            for batch in self.dataloader:
                global_step += 1
                
                # Encoder Decoder input ids
                input_ids = batch["input_ids"].to(self.device)
                attention_mask = batch["attention_mask"].to(self.device)
                global_attention_mask = batch["global_attention_mask"].to(self.device)
                issues_ids = batch["issues_input_ids"].to(self.device)
                facts_ids = batch["facts_input_ids"].to(self.device)
                rulings_ids = batch["rulings_input_ids"].to(self.device)
                
                # Step 1: Forward pass for issues (segment 1)
                issues_output = model(input_ids=input_ids,
                                      attention_mask=attention_mask,
                                      labels=issues_ids,
                                      global_attention_mask=global_attention_mask)
            
                # Step 2: Forward pass for facts (segment 2)
                facts_output = model(input_ids=input_ids,
                                     attention_mask=attention_mask,
                                     labels=facts_ids, 
                                     global_attention_mask=global_attention_mask)
            
                # Step 3: Forward pass for rulings (segment 3)
                rulings_output = model(input_ids=input_ids,
                                       attention_mask=attention_mask,
                                       labels=rulings_ids,
                                       global_attention_mask=global_attention_mask)
            
                # Sum up all losses and backpropagate
                loss = issues_output.loss + facts_output.loss + rulings_output.loss
                loss.backward()
                
                # Update weights and reset gradients
                self.optimizer.step()
                self.optimizer.zero_grad()

                # Accumulate the loss for the epoch
                epoch_loss += loss.item()

                # Log metrics for this step
                print(f"Global Step {global_step}, Loss: {loss.item()}")

            # Epoch-level logging
            epoch_time = time.time() - start_time  # Time for the entire epoch
            avg_loss = epoch_loss / len(self.dataloader)  # Average loss for the epoch
            steps_per_second = global_step / epoch_time  # Steps processed per second
            samples_per_second = (global_step * self.dataloader.batch_size) / epoch_time
            
            # Estimated FLOPs (can be complex to calculate exactly, so this is simplified)
            total_flos = global_step * input_ids.numel() * 2  # Example FLOPs (simplified estimate)
            
            # Print epoch-level summary
            print(f"Epoch {epoch + 1}/{self.epochs}, Avg Loss: {avg_loss}")
            print(f"TrainOutput(global_step={global_step}, "
                  f"training_loss={avg_loss}, "
                  f"metrics={{'train_runtime': {epoch_time:.4f}, "
                  f"'train_samples_per_second': {samples_per_second:.4f}, "
                  f"'train_steps_per_second': {steps_per_second:.4f}, "
                  f"'total_flos': {total_flos:.2f}, "
                  f"'train_loss': {avg_loss}, "
                  f"'epoch': {epoch + 1}}})")
        

from transformers import AutoTokenizer, AutoModel
import torch

class LegalBert:
    def __init__(self):
        # Use the fine-tuned Legal BERT model
        self.tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
        self.model = AutoModel.from_pretrained("nlpaueb/legal-bert-base-uncased")
        
        # Extend the positional embeddings
        self.extend_positional_embeddings(self.model, new_max_position_embeddings=16000)

    def extend_positional_embeddings(self, model, new_max_position_embeddings):
        # Get the original embeddings
        old_embeddings = model.embeddings.position_embeddings.weight
        old_num_embeddings, embedding_dim = old_embeddings.size()

        # Create new positional embeddings matrix
        new_embeddings = torch.nn.Embedding(new_max_position_embeddings, embedding_dim)
        
        # Initialize the new embeddings with the original values
        new_embeddings.weight.data[:old_num_embeddings, :] = old_embeddings.data

        # Initialize the remaining embeddings (if any) with a uniform distribution
        if new_max_position_embeddings > old_num_embeddings:
            new_embeddings.weight.data[old_num_embeddings:, :] = torch.nn.init.uniform_(torch.empty(new_max_position_embeddings - old_num_embeddings, embedding_dim))
        
        # Replace the model's position embeddings with the new extended ones
        model.embeddings.position_embeddings = new_embeddings
        model.config.max_position_embeddings = new_max_position_embeddings

    def get_context_vectors(self, text):
        # Tokenize and encode text with the Legal BERT model
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=16000)
        outputs = self.model(**inputs)
        return outputs.last_hidden_state


if __name__ == "__main__":
    # Initialize LegalBert instance
    legal_bert = LegalBert()
    
    # Check max_position_embeddings after initialization
    print("Max Position Embeddings after Initialization:", legal_bert.model.config.max_position_embeddings)
    
    # Example input text (adjust length as needed for testing)
    input_text = "This is a sample input text. " * 4000  # Approximately 16,000 tokens
    
    try:
        # Tokenize the input text
        tokens = legal_bert.tokenizer(input_text, return_tensors='pt', truncation=True, padding=True, max_length=16000)
        print("Tokenization successful. Sequence length:", tokens['input_ids'].size(1))
    except Exception as e:
        print("Tokenization error:", str(e))

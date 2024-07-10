from transformers import AutoTokenizer, AutoModel
import torch

class LegalBert:
    def __init__(self):
        # Use the fine-tuned Legal BERT model
        self.tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
        self.model = AutoModel.from_pretrained("nlpaueb/legal-bert-base-uncased")
        
        # Extend the positional embeddings
        self.extend_positional_embeddings(self.model, new_max_position_embeddings=16384)

    def extend_positional_embeddings(self, model, new_max_position_embeddings):
        """
        Extends the positional embeddings of the model.

        Parameters: 
        model (transformers.PreTrainedModel): The model whose positional embeddings are to be extended.
        new_max_position_embeddings (int): The new maximum length for positional embeddings.
        """
        # Set the new max position embeddings in the model config
        model.config.max_position_embeddings = new_max_position_embeddings
        
        # Resize the position_ids and position_embeddings
        old_embeddings = model.embeddings.position_embeddings.weight
        old_num_embeddings, embedding_dim = old_embeddings.size()
        """
        Extends the positional embeddings of the model.

        Parameters: 
        model (transformers.PreTrainedModel): The model whose positional embeddings are to be extended.
        new_max_position_embeddings (int): The new maximum length for positional embeddings.
        """
        # Create new positional embeddings matrix
        new_embeddings = torch.nn.Embedding(new_max_position_embeddings, embedding_dim)
        
        # Initialize the new embeddings with the original values
        new_embeddings.weight.data[:old_num_embeddings, :] = old_embeddings.data

        # Initialize the remaining embeddings (if any) with a uniform distribution
        if new_max_position_embeddings > old_num_embeddings:
            new_embeddings.weight.data[old_num_embeddings:, :] = torch.nn.init.uniform_(torch.empty(new_max_position_embeddings - old_num_embeddings, embedding_dim))

        # Replace the model's position embeddings with the new extended ones
        model.embeddings.position_embeddings = new_embeddings
        
        # Resize position_ids to match the new max position embeddings
        model.embeddings.position_ids = torch.arange(new_max_position_embeddings).expand((1, -1))


    def get_context_vectors(self, text):
        """
        Tokenizes and encodes text using the Legal BERT model.

        Parameters: 
        text (str): The text to be tokenized and encoded.

        Returns: torch.Tensor
            The output hidden states from the model.
        """
        # Tokenize and encode text with the Legal BERT model
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=16384)
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
        tokens = legal_bert.tokenizer(input_text, return_tensors='pt', truncation=True, padding=True, max_length=16384)
        print("Tokenization successful. Sequence length:", tokens['input_ids'].size(1))
    except Exception as e:
        print("Tokenization error:", str(e))

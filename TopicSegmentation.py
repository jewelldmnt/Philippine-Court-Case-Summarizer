from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn as nn


class LegalBert:
    def __init__(self):
        # Use the fine-tuned Legal BERT model
        self.tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
        self.model = AutoModel.from_pretrained("nlpaueb/legal-bert-base-uncased")
        
        # Extend the positional embeddings
        self.extend_positional_embeddings(self.model, new_max_position_embeddings=4096)


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
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=4096)
        outputs = self.model(**inputs)
        return outputs.last_hidden_state

class CustomDecoder(nn.Module):
    def __init__(self, vocab_size, d_model, num_heads, num_layers, max_len=4096, dropout=0.1):
        super(CustomDecoder, self).__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.positional_encoding = self.create_positional_encoding(d_model, max_len)
        self.dropout = nn.Dropout(dropout)
        self.multihead_attn = nn.MultiheadAttention(d_model, num_heads, dropout=dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, 2048),
            nn.ReLU(),
            nn.Linear(2048, d_model)
        )
        self.norm3 = nn.LayerNorm(d_model)
        self.fc_out = nn.Linear(d_model, vocab_size)
        self.softmax = nn.Softmax(dim=-1)

    def create_positional_encoding(self, d_model, max_len):
        pos = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * -(torch.log(torch.tensor(10000.0)) / d_model))
        pos_encoding = torch.zeros(max_len, d_model)
        pos_encoding[:, 0::2] = torch.sin(pos * div_term)
        pos_encoding[:, 1::2] = torch.cos(pos * div_term)
        return pos_encoding.unsqueeze(0)  # Add batch dimension

    def forward(self, tgt, memory):
        seq_len, _ = tgt.size()
        pos_encoding = self.positional_encoding[:, :seq_len, :].to(tgt.device)
        
        tgt = self.embedding(tgt) + pos_encoding
        tgt = self.dropout(tgt)
        
        # Masked Multi-Head Attention
        tgt2 = self.multihead_attn(tgt, tgt, tgt)[0]
        tgt = tgt + self.dropout(tgt2)
        tgt = self.norm1(tgt)

        # Multi-Head Attention with encoder output
        tgt2 = self.multihead_attn(tgt, memory, memory)[0]
        tgt = tgt + self.dropout(tgt2)
        tgt = self.norm2(tgt)

        # Feed Forward Network
        tgt2 = self.ffn(tgt)
        tgt = tgt + self.dropout(tgt2)
        tgt = self.norm3(tgt)

        output = self.fc_out(tgt)
        return self.softmax(output)


if __name__ == "__main__":
    # Initialize LegalBert instance
    legal_bert = LegalBert()
    
    # Example input text (adjust length as needed for testing)
    input_text = "This is a sample input text. " * 4000  # Approximately 16,000 tokens
    
    try:
        # Tokenize the input text
        tokens = legal_bert.tokenizer(input_text, return_tensors='pt', truncation=True, padding=True, max_length=4096)
        print("Tokenization successful. Sequence length:", tokens['input_ids'].size(1))
        
        # Get context vectors from LegalBert
        context_vectors = legal_bert.get_context_vectors(input_text)
        
        # Example decoder usage
        decoder = CustomDecoder(vocab_size=legal_bert.tokenizer.vocab_size, d_model=768, num_heads=8, num_layers=6, max_len=4096)
        tgt = tokens['input_ids']  # Use input ids as target for this example
        output = decoder(tgt, context_vectors)
        
        print("Decoder output shape:", output.shape)
        
    except Exception as e:
        print("Error:", str(e))
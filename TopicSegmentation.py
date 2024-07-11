from transformers import AutoTokenizer, AutoModel
import torch
from transformers import AutoTokenizer, AutoModel
import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import (
    Embedding,
    Dropout,
    LayerNormalization,
    Dense,
    MultiHeadAttention,
)

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



class ModifiedStandardDecoder(tf.keras.layers.Layer):
    def __init__(self, vocab_size, embedding_dim, num_heads, ff_dim, dropout_rate=0.1, **kwargs):
        super(ModifiedStandardDecoder, self).__init__(**kwargs)
        self.embedding = Embedding(vocab_size, embedding_dim)
        self.dropout1 = Dropout(dropout_rate)
        self.positional_encoding = PositionalEncoding(embedding_dim)
        self.dropout2 = Dropout(dropout_rate)
        self.masked_self_attention = MultiHeadAttention(num_heads=num_heads, key_dim=embedding_dim, dropout=dropout_rate)
        self.layer_norm1 = LayerNormalization(epsilon=1e-6)
        self.multihead_attention = MultiHeadAttention(num_heads=num_heads, key_dim=embedding_dim, dropout=dropout_rate)
        self.layer_norm2 = LayerNormalization(epsilon=1e-6)
        self.ffn = tf.keras.Sequential([
            Dense(ff_dim, activation="relu"),
            Dropout(dropout_rate),
            Dense(embedding_dim)
        ])
        self.layer_norm3 = LayerNormalization(epsilon=1e-6)
        self.dropout3 = Dropout(dropout_rate)
        self.dense = Dense(vocab_size)
        self.softmax = tf.keras.activations.softmax

    def call(self, inputs, encoder_outputs, padding_mask=None):
        # Text embedding layer
        embedded = self.embedding(inputs)

        # Dropout
        embedded = self.dropout1(embedded)

        # Positional encoding
        embedded = self.positional_encoding(embedded)

        # Dropout
        embedded = self.dropout2(embedded)

        print(embedded)

        # Create look-ahead mask
        seq_len = tf.shape(inputs)[1]
        look_ahead_mask = self.create_look_ahead_mask(seq_len)
        look_ahead_mask = tf.convert_to_tensor(look_ahead_mask, dtype=tf.float32)
        look_ahead_mask = look_ahead_mask[tf.newaxis, tf.newaxis, :, :]  # Shape: (1, 1, seq_len, seq_len)

        # Masked multi-head self-attention
        attention_output = self.masked_self_attention(query=embedded, key=embedded, value=embedded, attention_mask=look_ahead_mask)

        # Layer normalization
        attention_output = self.layer_norm1(attention_output + embedded)

        # Multi-head attention with encoder output
        output = self.multihead_attention(query=attention_output, key=encoder_outputs, value=encoder_outputs, attention_mask=padding_mask)

        # Layer normalization
        output = self.layer_norm2(output + attention_output)

        # Feed-forward network
        ffn_output = self.ffn(output)

        # Layer normalization
        ffn_output = self.layer_norm3(ffn_output + output)

        # Dropout
        ffn_output = self.dropout3(ffn_output)

        # Dense layer
        logits = self.dense(ffn_output)

        # Softmax
        predictions = self.softmax(logits)

        return predictions

    def create_look_ahead_mask(self, size):
        mask = tf.linalg.band_part(tf.ones((size, size)), -1, 0)
        return mask

    def save(self,filename):
        self.model.save('bert_model_{}.h5'.format(filename))

    def get_config(self):
        config = super(ModifiedStandardDecoder, self).get_config()
        config.update({
            "vocab_size": self.embedding.input_dim,
            "embedding_dim": self.embedding.output_dim,
            "num_heads": self.masked_self_attention.num_heads,
            "ff_dim": self.ffn.layers[0].units,
            "dropout_rate": self.dropout1.rate,
        })
        return config

class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, d_model, max_len=512):
        super(PositionalEncoding, self).__init__()
        self.pos_encoding = self.positional_encoding(max_len, d_model)
        
    def positional_encoding(self, position, d_model):
        angle_rads = self.get_angles(np.arange(position)[:, np.newaxis], np.arange(d_model)[np.newaxis, :], d_model)
        # Apply sin to even positions and cos to odd positions
        angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
        angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])
        pos_encoding = angle_rads[np.newaxis, ...]
        return tf.cast(pos_encoding, dtype=tf.float32)

    def get_angles(self, pos, i, d_model):
        angle_rates = 1 / np.power(10000, (2 * (i // 2)) / np.float32(d_model))
        return pos * angle_rates

    def call(self, inputs):
        return inputs + self.pos_encoding[:, :tf.shape(inputs)[1], :]


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

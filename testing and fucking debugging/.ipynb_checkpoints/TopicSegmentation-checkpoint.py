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
        self.extend_positional_embeddings(self.model, new_max_position_embeddings=1024)

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


    def get_context_vectors(self, texts, batch_size=16):
        """
        Tokenizes and encodes text using the Legal BERT model in batches.

        Parameters: 
        texts (list of str): The list of texts to be tokenized and encoded.
        batch_size (int): The batch size for processing the texts.

        Returns: torch.Tensor
            The concatenated output hidden states from the model.
        """ 
        all_outputs = []
        # Process the text in batches to avoid memory issues
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            # Tokenize and encode text with the Legal BERT model
            inputs = self.tokenizer(batch_texts, return_tensors='pt', truncation=True, padding='do_not_pad', max_length=1024)
            with torch.no_grad():  # Disable gradient calculations
                outputs = self.model(**inputs)
            all_outputs.append(outputs.last_hidden_state)
        
        # Concatenate all the outputs along the batch dimension
        return torch.cat(all_outputs, dim=0)



class ModifiedStandardDecoder(tf.keras.layers.Layer):
    def __init__(self, vocab_size, embedding_dim, num_heads, ff_dim, dropout_rate=0.1, **kwargs):
        super(ModifiedStandardDecoder, self).__init__(**kwargs)
        # Converts words (or more generally tokens) into dense vectors of fixed size, known as embeddings.
        self.embedding = Embedding(vocab_size, embedding_dim)

        # Prevent overfitting by randomly dropping units during training
        self.dropout = Dropout(dropout_rate)

        # Keep the position information of the embeddings
        self.positional_encoding = PositionalEncoding(embedding_dim)
        
        # Attetion head that will creates an autoregressive manner in the decoder model
        self.masked_self_attention = MultiHeadAttention(num_heads=num_heads, key_dim=embedding_dim, dropout=dropout_rate)

        # Stabilize and accelerate training by normalizing the inputs across the features
        self.layer_norm = LayerNormalization(epsilon=1e-6)

        # Attention head that will accept the context vector
        self.multihead_attention = MultiHeadAttention(num_heads=num_heads, key_dim=embedding_dim, dropout=dropout_rate)

        # Feed Forward Network
        self.ffn = tf.keras.Sequential([
          Dense(ff_dim, activation="relu"),
          Dropout(dropout_rate),
          Dense(embedding_dim)
        ])

        self.dense = Dense(vocab_size)
        
        self.softmax = tf.keras.activations.softmax

    def call(self, inputs, encoder_outputs, padding_mask=None, training=False):
        """
        Parameters:
            inputs - refers to the current predicted tokens at each iterations. This is because its in an autoregressive manner that predicts one token at a  
                     time base on the context vector.
                     
            encoder_outputs - refers to the context vector passed in by the encoder.
        """
        # Text embedding layer
        embedded = self.embedding(inputs)

        # Dropout Layer
        embedded = self.dropout(embedded, training=training)

        # Positional encoding
        embedded = self.positional_encoding(embedded)

        # Dropout Layer
        embedded = self.dropout(embedded, training=training)

        # Create look-ahead mask
        seq_len = tf.shape(inputs)[1]
        look_ahead_mask = self.create_look_ahead_mask(seq_len)
        look_ahead_mask = tf.convert_to_tensor(look_ahead_mask, dtype=tf.float32)
        look_ahead_mask = look_ahead_mask[tf.newaxis, tf.newaxis, :, :]  # Shape: (1, 1, seq_len, seq_len)

        # Masked multi-head self-attention
        attention_output = self.masked_self_attention(query=embedded, key=embedded, value=embedded, attention_mask=look_ahead_mask, training=training)

        # Dropout Layer
        attention_output = self.dropout(attention_output, training=training)

        # Layer normalization Layer
        attention_output = self.layer_norm(attention_output + embedded)

        # MultiHead Attention Layer
        output = self.multihead_attention(query=attention_output, key=encoder_outputs, value=encoder_outputs, attention_mask=padding_mask, training=training)

        # Dropout Layer
        output = self.dropout(output, training=training)

        # Layer normalization Layer
        output = self.layer_norm(output + attention_output)

        # Feed-forward network 
        ffn_output = self.ffn(output, training=training)
    
        # Dropout Layer
        ffn_output = self.dropout(ffn_output, training=training)
    
        # Layer normalization Layer
        ffn_output = self.layer_norm(ffn_output + output)

        # Dense layer
        logits = self.dense(ffn_output)
    
        return logits

    def create_look_ahead_mask(self, size):
        mask = tf.linalg.band_part(tf.ones((size, size)), -1, 0)
        return mask

    def save(self, filename):
        self.model.save('bert_model_{}.h5'.format(filename))

    def get_config(self):
        config = super(ModifiedStandardDecoder, self).get_config()
        config.update({
            "vocab_size": self.embedding.input_dim,
            "embedding_dim": self.embedding.output_dim,
            "num_heads": self.masked_self_attention.num_heads,
            "ff_dim": self.ffn.layers[0].units,
            "dropout_rate": self.dropout.rate,
        })
        return config

class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, d_model, max_len=1024):
        super(PositionalEncoding, self).__init__()
        self.pos_encoding = self.positional_encoding(max_len, d_model)
        
    def positional_encoding(self, position, d_model):
        angle_rads = self.get_angles(np.arange(position)[:, np.newaxis], np.arange(d_model)[np.newaxis, :], d_model)
        angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
        angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])
        pos_encoding = angle_rads[np.newaxis, ...]
        return tf.cast(pos_encoding, dtype=tf.float32)

    def get_angles(self, pos, i, d_model):
        angle_rates = 1 / np.power(10000, (2 * (i // 2)) / np.float32(d_model))
        return pos * angle_rates

    def call(self, inputs):
        return inputs + self.pos_encoding[:, :tf.shape(inputs)[1], :]

"""class PaddingMaskLayer(tf.keras.layers.Layer):
    def __init__(self, num_heads, **kwargs):
        super(PaddingMaskLayer, self).__init__(**kwargs)
        self.num_heads = num_heads

    def call(self, inputs):
        # Create the padding mask
        padding_mask = tf.cast(tf.math.equal(inputs, 0), tf.float32)

        # Shape: (batch_size, 1, 1, sequence_length)
        padding_mask = padding_mask[:, tf.newaxis, tf.newaxis, :]

        # Tile the mask for each head. Adjust the '1' to the number of heads.
        padding_mask = tf.tile(padding_mask, [1, self.num_heads, 1, 1])

        return padding_mask"""

class PaddingMaskLayer(tf.keras.layers.Layer):
    def __init__(self, num_heads, **kwargs):
        super(PaddingMaskLayer, self).__init__(**kwargs)
        self.num_heads = num_heads

    def call(self, inputs, training=None):
        # Check if we're in training mode
        if training:
            padding_mask = tf.cast(tf.math.equal(inputs, 0), tf.float32)
            padding_mask = padding_mask[:, tf.newaxis, tf.newaxis, :]  # Shape: (batch_size, 1, 1, seq_len)

            # Dynamic query length, derived from the shape of the decoder input.
            batch_size = tf.shape(inputs)[0]
            query_length = tf.shape(inputs)[1]

            # Tile the mask for the number of heads and current query length.
            padding_mask = tf.tile(padding_mask, [1, self.num_heads, query_length, 1])
            
            return padding_mask
        else:
            # Return None if not in training mode, i.e., during inference
            return None
        
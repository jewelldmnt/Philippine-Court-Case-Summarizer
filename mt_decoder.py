#!/usr/bin/env python
# coding: utf-8

# In[6]:


import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import (
    Embedding,
    Dropout,
    LayerNormalization,
    Dense,
    MultiHeadAttention,
)
from Preprocessing import PreProcessor
from TopicSegmentation import LegalBert
import pandas as pd


# In[2]:


text = "John Doe, a lawyer at ABC Corporation, filed a lawsuit on January 5, 2022, in New York City."

# Initialize the preprocessor and legal BERT
preprocessor = PreProcessor()
legal_bert = LegalBert()

# Preprocess the text
preprocessed_result = preprocessor.preprocess(text)

# Display preprocessing results
#print("Tokens:", preprocessed_result['tokens'])
#print("Tokens without stopwords:", preprocessed_result['tokens_no_stopwords'])

# Get BERT encoding for the preprocessed text without stopwords
#bert_output = legal_bert.get_context_vectors(preprocessed_result['tokens_no_stopwords'])

# Display BERT output shape
#print("Legal BERT's context vector:", bert_output)
#print("Legal BERT's context vector shape:", bert_output.shape)


# In[3]:


class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, d_model, max_len=16000):
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


# In[4]:


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

# Example usage
vocab_size = 8000
embedding_dim = 128
num_heads = 8
ff_dim = 512
dropout_rate = 0.1

decoder = ModifiedStandardDecoder(vocab_size, embedding_dim, num_heads, ff_dim, dropout_rate)

inputs = tf.keras.Input(shape=(None,))
encoder_outputs = tf.keras.Input(shape=(None, embedding_dim))

padding_mask = None  # Add padding mask if necessary

outputs = decoder(inputs, encoder_outputs, padding_mask=padding_mask)
model = tf.keras.Model(inputs=[inputs, encoder_outputs], outputs=outputs)

model.summary()


# In[18]:


x = "John Doe, a lawyer at ABC Corporation, filed a lawsuit on January 5, 2022, in New York City."
segments = pd.DataFrame({
    'text': "John Doe, a lawyer at ABC Corporation, filed a lawsuit on January 5, 2022, in New York City.",
    'ruling': [['John', 'Doe', 'a', 'lawyer', 'at', 'ABC', 'Corporation']],
    'facts': [['filed', 'a', 'lawsuit', 'on', 'January']],
    'issues': [['in', 'New', 'York', 'City']]
})


# In[19]:


segments.head()


# In[14]:


# Tokenize the segments
tokenizer = Tokenizer(num_words=8000)  # Adjust num_words according to your vocabulary size
tokenizer.fit_on_texts(segments)
tokenized_segments = tokenizer.texts_to_sequences(segments)

# Get context vector of the whole document
bert_output = legal_bert.get_context_vectors(preprocessed_result['tokens_no_stopwords'])

# Pad the sequences to ensure uniform length
padded_segments = pad_sequences(tokenized_segments, padding='post')

# Convert to tensor
padded_segments = tf.convert_to_tensor(padded_segments)

print(bert_output.shape[0])
print(padded_segments.shape[1])

# Ensure xtrain and ytrain have the same batch size
assert bert_output.shape[0] == padded_segments.shape[1]

xtrain = bert_output
ytrain = padded_segments

# Compile the model
model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=1e-3), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train
model.fit(xtrain, ytrain, epochs=epochs)


# In[ ]:





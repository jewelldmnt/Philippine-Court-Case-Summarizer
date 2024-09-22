from TopicSegmentation import LegalBert, ModifiedStandardDecoder, PaddingMaskLayer
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
import re

# Model Configuration
vocab_size = 2500
embedding_dim = 1024
num_heads = 8
ff_dim = 1024
dropout_rate = 0.1

decoder = ModifiedStandardDecoder(vocab_size, embedding_dim, num_heads, ff_dim, dropout_rate)

# Inputs to the model
segment_inputs = tf.keras.Input(shape=(None,), name="Segment_Input_Layer") # refers to the tokens fed into one at a time
encoder_outputs = tf.keras.Input(shape=(None, embedding_dim), name="Context_Vector_Input_Layer")

padding_mask_layer = PaddingMaskLayer(name="Padding_Mask_Layer")
padding_mask = padding_mask_layer(segment_inputs)

outputs = decoder(segment_inputs, encoder_outputs, padding_mask=padding_mask)
model_issues = tf.keras.Model(inputs=[encoder_outputs, segment_inputs], outputs=outputs)

model_issues.summary()



def remove_newlines(strings):
  """Removes newline characters from a list of strings using regular expressions.

  Args:
    strings: A list of strings.

  Returns:
    A new list of strings without newline characters.
  """

  pattern = r"\n"
  return [re.sub(pattern, "", s) for s in strings]

df = pd.read_csv('new_court_cases.csv')

df.dropna(inplace=True)

court_cases = df['whole_text'].to_list()
court_cases = remove_newlines(court_cases)
issues = df['issues'].to_list()


# Initialize the preprocessor and legal BERT
legal_bert = LegalBert()

# Get context vectors in batches
bert_output = legal_bert.get_context_vectors(court_cases, batch_size=32)


bert_output.shape

tokenizer_issues = legal_bert.tokenizer

# Tokenize the issues segments using LegalBERT tokenizer
tokenized_segments_issues = [tokenizer_issues.encode(issue, add_special_tokens=True) for issue in issues]

# Max sequence length
max_seq_len = min(bert_output.shape[1], 1024)

# Pad the sequences to ensure uniform length
padded_segments_issues = pad_sequences(tokenized_segments_issues, padding='post', maxlen=max_seq_len)

# Shift the input sequences to the right by one position
shifted_segments_issues = np.zeros_like(padded_segments_issues)
shifted_segments_issues[:, 1:] = padded_segments_issues[:, :-1]  # Shift right
shifted_segments_issues[:, 0] = tokenizer_issues.cls_token_id  # Use BERT's [CLS] token ID as the start token

# Convert to tensor
shifted_segments_issues = tf.convert_to_tensor(shifted_segments_issues)
padded_segments_issues = tf.convert_to_tensor(padded_segments_issues)

# set the training data
xbert_train= bert_output.detach().numpy()
xtrain = tf.convert_to_tensor(xbert_train, dtype=tf.float32)
ytrain_issues = tf.convert_to_tensor(padded_segments_issues, dtype=tf.int32)
ytrain_shifted = tf.convert_to_tensor(shifted_segments_issues, dtype=tf.int32)

xtrain.shape


print("xtrain shape:", xtrain.shape)  # Should be (batch_size, seq_len, embedding_dim)
print("ytrain_shifted shape:", ytrain_shifted.shape)  # Should be (batch_size, seq_len)
print("ytrain_issues shape:", ytrain_issues.shape)  # Should be (batch_size, seq_len)

# Compile the models
model_issues.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=1e-4), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model_issues.fit([xtrain, ytrain_issues], ytrain_shifted, epochs=3)
model_issues.save('issues_seq_to_seq.keras')


class PrintPredictionsCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        # Prepare a sample input (tokenized and padded sequence)
        sample_court_case_input = ytrain_issues[:1]  # Shape: (1, sequence_length)
        sample_context_vector_input = xtrain[:1]  # Shape: (1, sequence_length, embedding_dim)
        
        # Make a prediction
        sample_output = self.model.predict([sample_court_case_input, sample_context_vector_input])
        
        # Decode the prediction
        decoded_output = tokenizer_issues.sequences_to_texts(sample_output.argmax(-1))
        
        print(f"\nSample Prediction after epoch {epoch+1}: {decoded_output}")

# Apply the callback during training
model_issues.fit([ytrain_issues, xtrain], ytrain_issues, epochs=3, callbacks=[PrintPredictionsCallback()])






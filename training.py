from TopicSegmentation import LegalBert, ModifiedStandardDecoder
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Example usage
vocab_size = 8000
embedding_dim = 768
num_heads = 8
ff_dim = 512
dropout_rate = 0.1

decoder = ModifiedStandardDecoder(vocab_size, embedding_dim, num_heads, ff_dim, dropout_rate)

annotated_inputs = tf.keras.Input(shape=(None,))
encoder_outputs = tf.keras.Input(shape=(None, embedding_dim))

padding_mask = None  # Add padding mask if necessary

outputs = decoder(annotated_inputs, encoder_outputs, padding_mask=padding_mask)
model = tf.keras.Model(inputs=[annotated_inputs, encoder_outputs], outputs=outputs)

model.summary()

df_text = ["John Doe a lawyer at ABC Corporation filed a lawsuit on January in New York City", 
           "Mama mo a dentist at DFC Corporation filed a lawsuit on January in New York City"]

ruling = ['John Doe a lawyer at ABC Corporation', 'Mama mo a dentist at DFC Corporation']
    
# Initialize the preprocessor and legal BERT
legal_bert = LegalBert()

bert_output = legal_bert.get_context_vectors(df_text)


# Tokenize the segments
tokenizer = Tokenizer(num_words=8000)  # Adjust num_words according to your vocabulary size
tokenizer.fit_on_texts(ruling)
tokenized_segments = tokenizer.texts_to_sequences(ruling)

max_seq_len = bert_output.shape[1]

# Pad the sequences to ensure uniform length
padded_segments = pad_sequences(tokenized_segments, padding='post', maxlen=max_seq_len)

# Convert to tensor
padded_segments = tf.convert_to_tensor(padded_segments)

print(f'Legal BERT shape: {bert_output.shape}')
print(f'Modified Decoder shape: {padded_segments.shape}')

# Ensure xtrain and ytrain have the same batch size
assert bert_output.shape[0] == padded_segments.shape[0]

xtrain = bert_output.detach().numpy()
ytrain = padded_segments

# Compile the model
model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=1e-3), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train
model.fit([ytrain, xtrain], ytrain, epochs=5)

model.save('seqtoseq.h5')


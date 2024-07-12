from TopicSegmentation import LegalBert, ModifiedStandardDecoder
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd

# Example usage
vocab_size = 5000
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

df = pd.read_csv('court.csv')

df = df.iloc[:,2:]

df.dropna(inplace=True)

court_case = df['court case'].to_list()
ruling = df['rulings'].to_list()
facts = df['facts'].to_list()
issues = df['issues'].to_list()
    
# Initialize the preprocessor and legal BERT
legal_bert = LegalBert()

bert_output = legal_bert.get_context_vectors(court_case)

# Tokenize the segments
tokenizer = Tokenizer(num_words=5000)  # Adjust num_words according to your vocabulary size
tokenizer.fit_on_texts(ruling)
tokenized_segments = tokenizer.texts_to_sequences(ruling)

max_seq_len = min(bert_output.shape[1], 512)

# Pad the sequences to ensure uniform length
padded_segments = pad_sequences(tokenized_segments, padding='post', maxlen=max_seq_len)

# Convert to tensor
padded_segments = tf.convert_to_tensor(padded_segments)

xtrain = bert_output.detach().numpy()
ytrain = padded_segments

# Compile the model
model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=1e-4), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train
model.fit([ytrain, xtrain], ytrain, epochs=3)

model.save('seqtoseq_model.keras')


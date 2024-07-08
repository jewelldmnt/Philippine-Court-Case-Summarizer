import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class PreProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.nlp = spacy.load('en_core_web_sm')

    def preprocess(self, text):
        # Step 1: Tokenization
        tokens = word_tokenize(text)
        
        # Step 2: Stopword Removal
        tokens_no_stopwords = [word for word in tokens if word.lower() not in self.stop_words]
        
        # Step 3: POS Tagging
        pos_tags = nltk.pos_tag(tokens_no_stopwords)
        
        # Convert tokens_no_stopwords list back to a single string for NER tagging
        text_no_stopwords = ' '.join(tokens_no_stopwords)
        
        # Step 4: NER Tagging
        doc = self.nlp(text_no_stopwords)
        entities = [(entity.text, entity.label_) for entity in doc.ents]
        
        return {
            'tokens': tokens,
            'tokens_no_stopwords': tokens_no_stopwords,
            'pos_tags': pos_tags,
            'entities': entities
        }

# Example usage
if __name__ == "__main__":
    text = "John Doe, a lawyer at ABC Corporation, filed a lawsuit on January 5, 2022, in New York City."
    processor = PreProcessor()
    result = processor.preprocess(text)
    
    print("Tokens:", result['tokens'])
    print("Tokens without stopwords:", result['tokens_no_stopwords'])
    print("POS Tags:", result['pos_tags'])
    print("Named Entities:", result['entities'])
    print(f"Stopwords: {processor.stop_words}")

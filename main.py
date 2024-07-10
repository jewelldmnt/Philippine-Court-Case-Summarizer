from Preprocessing import PreProcessor
from TopicSegmentation import LegalBert

def main():
    
    text = "John Doe, a lawyer at ABC Corporation, filed a lawsuit on January 5, 2022, in New York City."
    
    # Initialize the preprocessor and legal BERT
    preprocessor = PreProcessor()
    legal_bert = LegalBert()
    
    # Preprocess the text
    preprocessed_result = preprocessor.preprocess(text)
    
    # Display preprocessing results
    print("Tokens:", preprocessed_result['tokens'])
    print("Tokens without stopwords:", preprocessed_result['tokens_no_stopwords'])
 
    # Get BERT encoding for the preprocessed text without stopwords
    bert_output = legal_bert.get_context_vectors(preprocessed_result['tokens_no_stopwords'])
    
    # Display BERT output shape
    print("BERT Encoding Shape:", bert_output)
    
if __name__ == "__main__":
    main()

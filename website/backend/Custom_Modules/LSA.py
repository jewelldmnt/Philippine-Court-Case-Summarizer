import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


class LSA:
    def __init__(
        self, text_dict: dict, facts_pct=0.35, issues_pct=0.05, ruling_pct=0.60
    ):
        """
        Description:
        Initialize the LSA class with text data and percentage parameters for generating the summary.

        Parameters:
        - text_dict: A dictionary where the key is the sentence and the value is the corresponding label ('facts', 'issues', 'ruling').
        - facts_pct: The percentage of sentences to include in the 'facts' section of the summary.
        - issues_pct: The percentage of sentences to include in the 'issues' section of the summary.
        - ruling_pct: The percentage of sentences to include in the 'ruling' section of the summary.
        """
        self.text_dict = text_dict
        self.facts_pct = facts_pct
        self.issues_pct = issues_pct
        self.ruling_pct = ruling_pct
        self.labels = ["facts", "issues", "rulings"]

    def preprocess_text(self):
        """
        Description:
        Preprocess the text by splitting sentences and their associated labels in the order they appear.

        Parameters: None

        Return:
        - sentences: A list of sentences from the input text.
        - labels: A list of labels corresponding to each sentence ('facts', 'issues', 'ruling').
        """
        sentences = []
        labels = []

        for sentence, label in self.text_dict.items():
            sentences.append(sentence)
            labels.append(label)

        return sentences, labels

    def create_term_matrix(self, sentences):
        """
        Description:
        Create a term-sentence matrix using TF-IDF vectorization.

        Parameters:
        - sentences: List of sentences to be vectorized.

        Return:
        - term_matrix: The term-sentence matrix produced by the TF-IDF vectorizer.
        - vectorizer: The fitted TF-IDF vectorizer.
        """
        vectorizer = TfidfVectorizer(stop_words="english")
        term_matrix = vectorizer.fit_transform(sentences)
        return term_matrix, vectorizer

    def apply_svd(self, term_matrix, n_components=2):
        """
        Description:
        Apply Singular Value Decomposition (SVD) to reduce the dimensionality of the term-sentence matrix.

        Parameters:
        - term_matrix: The term-sentence matrix generated by TF-IDF vectorization.
        - n_components: The number of components to reduce the matrix to using SVD.

        Return:
        - svd_matrix: The reduced matrix obtained after applying SVD.
        """
        svd = TruncatedSVD(n_components=n_components)
        svd_matrix = svd.fit_transform(term_matrix)
        return svd_matrix

    def rank_sentences(self, svd_matrix):
        """
        Description:
        Rank the sentences based on their relevance scores from the SVD matrix.

        Parameters:
        - svd_matrix: The matrix from SVD containing sentence relevance scores.

        Return:
        - ranked_indices: A list of indices representing sentences ranked by relevance in descending order.
        """
        sentence_scores = np.sum(svd_matrix, axis=1)
        ranked_indices = np.argsort(sentence_scores)[
            ::-1
        ]  # Sort sentences by score in descending order
        return ranked_indices

    def select_top_sentences(self, ranked_indices, sentences, labels):
        """
        Description:
        Select the top sentences for each label (facts, issues, ruling) based on the ranking and percentage distribution.

        Parameters:
        - ranked_indices: The ranked indices of sentences based on relevance scores.
        - sentences: List of original sentences.
        - labels: List of labels corresponding to each sentence.

        Return:
        - summary: A dictionary containing selected top sentences categorized by 'facts', 'issues', and 'ruling'.
        """
        total_summary_sentences = int(
            len(sentences)
            * (self.facts_pct + self.issues_pct + self.ruling_pct)
        )
        print(f"Total summary sentences: {total_summary_sentences}")

        # Calculate how many sentences to include from each section based on the total summary length
        facts_count = int(self.facts_pct * total_summary_sentences)
        print(f"facts_count: {facts_count}")
        issues_count = int(self.issues_pct * total_summary_sentences)
        print(f"issues_count: {issues_count}")
        ruling_count = int(self.ruling_pct * total_summary_sentences)
        print(f"ruling_count: {ruling_count}")

        # Adjust issues_count to select all sentences if percentage is too small
        if issues_count == 0:
            issues_count = sum(1 for label in labels if label == "issues")

        # Ensure the total doesn't exceed total_summary_sentences
        remaining_count = total_summary_sentences - (
            facts_count + issues_count + ruling_count
        )
        print(f"remaining count: {remaining_count}")
        if remaining_count > 0:
            ruling_count += remaining_count  # Assign remaining to ruling as a default strategy

        summary = {"facts": [], "issues": [], "rulings": []}

        # Select top sentences based on ranking while maintaining original order
        ranked_sentences = [(sentences[i], labels[i]) for i in ranked_indices]
        for sentence, label in ranked_sentences:
            if label == "facts" and len(summary["facts"]) < facts_count:
                summary["facts"].append(sentence)
            elif label == "issues" and len(summary["issues"]) < issues_count:
                summary["issues"].append(sentence)
            elif label == "rulings" and len(summary["rulings"]) < ruling_count:
                summary["rulings"].append(sentence)

        return summary

    def create_summary(self):
        """
        Description:
        Create a summary based on LSA using sentence ranking, ensuring that the order is preserved from the original text.

        Parameters: None

        Return:
        - summary_output: A string containing the formatted summary with sections for FACTS, ISSUES, and RULING.
        """
        # Preprocess text
        sentences, labels = self.preprocess_text()

        # Create term-sentence matrix
        term_matrix, vectorizer = self.create_term_matrix(sentences)

        # Apply SVD to get relevance scores
        svd_matrix = self.apply_svd(term_matrix)

        # Rank sentences based on relevance scores
        ranked_indices = self.rank_sentences(svd_matrix)

        # Select top sentences for summary
        summary = self.select_top_sentences(ranked_indices, sentences, labels)

        # Construct the output in proper order for each section
        summary_output = "FACTS:\n"
        summary_output += (
            " ".join(
                [
                    sentence
                    for sentence in sentences
                    if sentence in summary["facts"]
                ]
            )
            + "\n\n"
        )
        summary_output += "ISSUES:\n"
        summary_output += (
            " ".join(
                [
                    sentence
                    for sentence in sentences
                    if sentence in summary["issues"]
                ]
            )
            + "\n\n"
        )
        summary_output += "RULINGS:\n"
        summary_output += " ".join(
            [
                sentence
                for sentence in sentences
                if sentence in summary["rulings"]
            ]
        )

        return summary_output


# Usage Example
if __name__ == "__main__":
    # Example dictionary input: key = sentence, value = label
    text_dict = {
        "The case involves a dispute over a contract.": "facts",
        "The main issue is whether the contract is valid.": "issues",
        "The court ruled that the contract was void.": "rulings",
        "Both parties agreed to the terms initially.": "facts",
        "However, one party later claimed a breach.": "facts",
        "The breach was contested in court.": "issues",
        "The final judgment favored the defendant.": "rulings",
        "Evidence presented during the trial was insufficient.": "facts",
    }

    lsa = LSA(text_dict)
    summary = lsa.create_summary()

    print("Summary:")
    print(summary)

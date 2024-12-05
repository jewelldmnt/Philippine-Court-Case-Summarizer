# =============================================================================
# Program Title: Latent Semantic Analysis (LSA)
# Programmers: Jewell Anne Diamante
# Date Written: September 10, 2024
# Date Revised: October 11, 2024
#
# Purpose:
#     This program processes legal texts by segmenting them into sections
#     (facts, issues, and rulings) and generates a concise summary using
#     Latent Semantic Analysis (LSA). The output summary allows legal
#     professionals and automated systems to quickly obtain an overview of
#     the case content.
#
#     The program supports efficient legal document analysis, enhancing
#     workflows by providing a structured summary of complex court cases.
#
# Where the program fits in the general system design:
#     The LSA-based Text Summarization module is a core component within a
#     legal document analysis system. It automates the extraction and
#     summarization of court case information, aiding in quick retrieval and
#     understanding of key case elements. This module contributes to downstream
#     system features like search, classification, and recommendation engines,
#     facilitating improved document management and analysis.
#
# Data Structures, Algorithms, and Control:
#     - Data Structures:
#         - **text_dict**: A dictionary holding segmented text data for
#           "facts," "issues," and "rulings".
#         - **summary**: A dictionary that stores the top-ranked sentences
#           for each section after processing.
#     - Algorithms:
#         - **TF-IDF Vectorization**: Transforms sentences into a
#           term-sentence matrix for feature extraction.
#         - **Singular Value Decomposition (SVD)**: Reduces dimensionality
#           of the term-sentence matrix, identifying the most relevant
#           sentences.
#         - **Sentence Ranking**: Sentences are ranked by relevance scores,
#           with the top-ranked sentences selected for inclusion in the
#           final summary.
#     - Control:
#         - The program follows a linear execution flow:
#           1. text preprocessing
#           2. topic segmentation
#           3. matrix creation
#           4. SVD application
#           5. sentence ranking
#           6. summary generation.
# =============================================================================


import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD



class LSA:
    def __init__(
        self, text_dict: dict, facts_pct=0.5, issues_pct=0.05, ruling_pct=0.45
    ):
        """
        Description:
        Initialize the LSA class with text data and percentage parameters for 
            generating the summary.

        Parameters:
        - text_dict: A dictionary where the keys are 'facts', 'issues', 
                            and 'rulings' and values are lists of tuples:
                            (sentence, probability).
        - facts_pct: The percentage of sentences to include in the 'facts' section 
                    of the summary.
        - issues_pct: The percentage of sentences to include in the 'issues' 
                    section of the summary.
        - ruling_pct: The percentage of sentences to include in the 'rulings' 
                    section of the summary.
        """
        self.text_dict = text_dict
        self.facts_pct = facts_pct
        self.issues_pct = issues_pct
        self.ruling_pct = ruling_pct
        self.labels = ["facts", "issues", "rulings"]

    def preprocess_text(self):
        """
        Description:
        Preprocess the text by concatenating sentences from each label category.

        Parameters: None

        Return:
        - sentences: A list of all sentences.
        - labels: A list of labels corresponding to each sentence ('facts', 
                    'issues', 'rulings').
        """
        sentences = []
        labels = []
        probabilities = []

        for label, sentence_list in self.text_dict.items():
            for sentence, probability in sentence_list:
                sentences.append(sentence)
                labels.append(label)
                probabilities.append(probability)

        return sentences, labels, probabilities

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

    def apply_svd(self, term_matrix, n_components=3):
        """
        Description:
        Apply Singular Value Decomposition (SVD) to reduce the dimensionality of 
            the term-sentence matrix.

        Parameters:
        - term_matrix: The term-sentence matrix generated by TF-IDF vectorization.
        - n_components: The number of components to reduce the matrix to using SVD.

        Return:
        - svd_matrix: The reduced matrix obtained after applying SVD.
        """
        # n_components=min(term_matrix.shape[0], term_matrix.shape[1])
        svd = TruncatedSVD(n_components=n_components)
        svd_matrix = svd.fit_transform(term_matrix)
        return svd_matrix

    def rank_sentences(self, svd_matrix, probabilities, labels):
        """
        Description:
        Rank the sentences based on their relevance scores from the SVD matrix.

        Parameters:
        - svd_matrix: The matrix from SVD containing sentence relevance scores.

        Return:
        - ranked_indices: A list of indices representing sentences ranked by 
                    relevance in descending order.
        """
        sentence_scores = np.array([
            np.sum(svd_matrix[i]) * probabilities[i] if labels[i] == "issues" else np.sum(svd_matrix[i])
            for i in range(len(labels))
        ])
        ranked_indices = np.argsort(sentence_scores)[::-1]  # Sort sentences by score in descending order
        return ranked_indices

    def select_top_sentences(self, ranked_indices, sentences, labels):
        """
        Description:
        Select the top sentences for each label (facts, issues, ruling) based on 
            the ranking and percentage distribution.

        Parameters:
        - ranked_indices: The ranked indices of sentences based on relevance scores.
        - sentences: List of original sentences.
        - labels: List of labels corresponding to each sentence.

        Return:
        - summary: A dictionary containing selected top sentences categorized by 
                    'facts', 'issues', and 'rulings'.
        """
        total_summary_sentences = int(
            len(sentences)
            * (self.facts_pct + self.issues_pct + self.ruling_pct)
        )

        # Calculate how many sentences to include from each section
        facts_count = int(self.facts_pct * total_summary_sentences)
        issues_count = int(self.issues_pct * total_summary_sentences)
        ruling_count = int(self.ruling_pct * total_summary_sentences)

        # Adjust issues_count to select all sentences if percentage is too small
        if issues_count == 0:
            issues_count = sum(1 for label in labels if label == "issues")

        # Ensure the total doesn't exceed total_summary_sentences
        remaining_count = total_summary_sentences - (
            facts_count + issues_count + ruling_count
        )
        if remaining_count > 0:
            ruling_count += remaining_count  # Assign remaining to ruling as a default strategy

        summary = {"facts": [], "issues": [], "rulings": []}

        # Select top sentences based on ranking while maintaining original order
        ranked_sentences = [(sentences[i], labels[i]) for i in ranked_indices]
        for sentence, label in ranked_sentences:
            if "." not in sentence:
                continue  # Skip sentences without a period
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
        Create a summary based on LSA using sentence ranking, ensuring that the 
            order is preserved from the original text.

        Parameters: None

        Return:
        - summary_output: A string containing the formatted summary with sections 
                    for FACTS, ISSUES, and RULING.
        """
        # Preprocess text
        sentences, labels, probabilities = self.preprocess_text()

        # Create term-sentence matrix
        term_matrix, vectorizer = self.create_term_matrix(sentences)

        # Apply SVD to get relevance scores
        svd_matrix = self.apply_svd(term_matrix)

        # Rank sentences based on relevance scores
        ranked_indices = self.rank_sentences(svd_matrix, probabilities, labels)

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
                sentence.replace("so ordered.", "").strip()
                for sentence in sentences
                if sentence in summary["rulings"] and sentence.lower() != "so ordered."]
        )

        return summary_output


# Usage Example
if __name__ == "__main__":
    # Example output from label_mapping function
    text_dict = {
        "facts": [
            ("The case concerns a property dispute between two families.", 0.8),
            ("The land in question was acquired through inheritance.", 0.7),
            ("One family claims rightful ownership due to ancestral rights.", 0.85),
            ("The other family presented a deed of sale as evidence.", 0.6),
            ("The dispute has been ongoing for over a decade.", 0.9),
        ],
        "issues": [
            ("The primary issue is the validity of the deed of sale.", 0.95),
            ("The question of whether ancestral rights override documentation was raised.", 0.9),
            ("The secondary issue is whether the deed of sale was fraudulently executed.", 0.8),
        ],
        "rulings": [
            ("The court held that the deed of sale was valid.", 0.85),
            ("The family claiming ancestral rights was ordered to vacate the property.", 0.8),
            ("The ruling emphasized the importance of documented ownership.", 0.75),
            ("Costs of the proceedings were awarded to the defendants.", 0.7),
        ],
    }


    lsa = LSA(text_dict)
    summary = lsa.create_summary()

    print("Summary:")
    print(summary)

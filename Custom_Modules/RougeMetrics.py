# =============================================================================
# Program Title: ROUGE Score Computation for Summarization Evaluation
# Programmer: Jewell Anne Diamante
# Date Written: October 9, 2024
# Date Revised: October 14, 2024
#
# Purpose:
#     This program is designed to compute the ROUGE (Recall-Oriented Understudy for Gisting Evaluation) scores 
#     between human-generated and AI-generated summaries. The ROUGE metric evaluates the quality of summaries by 
#     comparing n-grams, word sequences, and sentence-level structures between a reference (human) summary and 
#     the candidate (AI-generated) summary. It calculates three primary components: recall, precision, and F1 score 
#     for ROUGE-1 (unigram), ROUGE-2 (bigram), and ROUGE-L (longest common subsequence).
#
# Where the program fits in the general system design:
#     This program serves as part of an automated evaluation system for summarization tasks, specifically comparing 
#     AI-generated summaries against human references. It aids in assessing the quality of AI models and tuning them for 
#     better summarization performance, which is critical in NLP-based applications like legal document summarization, 
#     news summarization, and research paper summarization.
#
# Data Structures, Algorithms, and Control:
#     - Data Structures:
#         - **String (`human_summary`)**: The reference human-generated summary, read from a file.
#         - **String (`ai_summary`)**: The candidate AI-generated summary, read from a file.
#         - **Dictionary (`rouge_scores`)**: Contains ROUGE scores (recall, precision, and F1) for each ROUGE metric 
#           (ROUGE-1, ROUGE-2, ROUGE-L).
#     - Algorithms:
#         - **File Reading**: The `read_file` function reads the content of text files and returns it as a string. It raises 
#           a `FileNotFoundError` if the file does not exist.
#         - **ROUGE Scoring**: The `compute_rouge_scores` function utilizes the `rouge_scorer` from the `rouge_score` library 
#           to compute ROUGE scores (recall, precision, and F1) between a human summary and an AI summary. It computes the 
#           ROUGE-1 metric by default and can be extended to other ROUGE metrics.
#     - Control:
#         - The program follows a step-by-step procedure:
#           1. It reads the human summary and AI-generated summary from specified file paths.
#           2. It computes ROUGE scores by calling the `compute_rouge_scores` function.
#           3. It prints the computed ROUGE scores (recall, precision, F1) for each metric (ROUGE-1).
#         - Exception handling is implemented in the `read_file` function to ensure safe file access and prevent crashes 
#           if a file is missing.
# =============================================================================


from rouge_score import rouge_scorer
import os

def read_file(file_path):
    """
    Read the content of a file.

    :param file_path: Path to the file.
    :return: Content of the file as a string.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        return file.read()

def compute_rouge_scores(human_summary, ai_summary):
    """
    Compute ROUGE scores (recall, precision, F1) between human-generated and AI-generated summaries.

    :param human_summary: The reference summary (human-generated).
    :param ai_summary: The candidate summary (AI-generated).
    :return: A dictionary containing ROUGE-1, ROUGE-2, and ROUGE-L scores with recall, precision, and F1.
    """
    # Initialize the ROUGE scorer
    scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
    
    # Compute ROUGE scores
    scores = scorer.score(human_summary, ai_summary)
    
    # Convert scores to a dictionary format
    rouge_scores = {}
    for key in scores:
        rouge_scores[key] = {
            'recall': scores[key].recall,
            'precision': scores[key].precision,
            'f1': scores[key].fmeasure
        }
    
    return rouge_scores

if __name__ == "__main__":
    # Path to the human summary file
    human_summary_path = 'Summaries/Human/human_summary.txt'
    human_summary = read_file(human_summary_path)

    # Compute and print ROUGE scores for each AI-generated summary
    ai_summary_path = f'Summaries/AI/ai_summary.txt'
    ai_summary = read_file(ai_summary_path)
    
    # Compute ROUGE scores
    scores = compute_rouge_scores(human_summary, ai_summary)
    
    # Print the scores
    print(f"Scores for AI-generated summary 2:")
    for metric, values in scores.items():
        print(f"{metric.upper()} - Recall: {values['recall']:.4f}, Precision: {values['precision']:.4f}, F1: {values['f1']:.4f}")
    print()

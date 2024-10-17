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

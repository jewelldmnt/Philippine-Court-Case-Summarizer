# =============================================================================
# Program Title: ROUGE Score Computation for Summarization Evaluation
# Programmer: Jewell Anne Diamante
# Date Written: October 9, 2024
# Date Revised: November 18, 2024
#
# Purpose:
#     This program is designed to compute the ROUGE (Recall-Oriented Understudy
#     for Gisting Evaluation) scores between human-generated and AI-generated
#     summaries. The ROUGE metric evaluates the quality of summaries by comparing
#     n-grams, word sequences, and sentence-level structures between a reference
#     (human) summary and the candidate (AI-generated) summary. It calculates
#     three primary components: recall, precision, and F1 score for ROUGE-1
#     (unigram), ROUGE-2 (bigram), and ROUGE-L (longest common subsequence).
#
# Where the program fits in the general system design:
#     This program serves as part of an automated evaluation system for
#     summarization tasks, specifically comparing AI-generated summaries against
#     human references. It aids in assessing the quality of AI models and tuning
#     them for better summarization performance, which is critical in NLP-based
#     applications like legal document summarization, news summarization, and
#     research paper summarization.
#
# Data Structures, Algorithms, and Control:
#     - Data Structures:
#         - **String (`human_summary`)**: The reference human-generated summary,
#           read from a file.
#         - **String (`ai_summary`)**: The candidate AI-generated summary, read
#           from a file.
#         - **Dictionary (`rouge_scores`)**: Contains ROUGE scores (recall,
#           precision, and F1) for each ROUGE metric (ROUGE-1, ROUGE-2, ROUGE-L).
#     - Algorithms:
#         - **File Reading**: The `read_file` function reads the content of text
#           files and returns it as a string. It raises a `FileNotFoundError` if
#           the file does not exist.
#         - **ROUGE Scoring**: The `compute_rouge_scores` function utilizes the
#           `rouge_scorer` from the `rouge_score` library to compute ROUGE scores
#           (recall, precision, and F1) between a human summary and an AI summary.
#           It computes the ROUGE-1 metric by default and can be extended to other
#           ROUGE metrics.
#     - Control:
#         - The program follows a step-by-step procedure:
#           1. It reads the human summary and AI-generated summary from specified
#              file paths.
#           2. It computes ROUGE scores by calling the `compute_rouge_scores`
#              function.
#           3. It prints the computed ROUGE scores (recall, precision, F1) for each
#              metric (ROUGE-1).
#         - Exception handling is implemented in the `read_file` function to ensure
#           safe file access and prevent crashes if a file is missing.
# =============================================================================


from rouge_score import rouge_scorer
import os
import pandas as pd
from fpdf import FPDF

def read_file(file_path, encoding):
    """
    Reads the content of a file with the specified encoding.

    Args:
        file_path (str): The path to the file to be read.
        encoding (str): The encoding used to read the file.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist at the specified path.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r', encoding=encoding) as file:
        return file.read()

def compute_rouge_scores(human_summary, ai_summary):
    """
    Computes ROUGE-1 scores (recall, precision, F1-score) between two summaries.

    Args:
        human_summary (str): The reference summary written by a human.
        ai_summary (str): The AI-generated summary to be compared.

    Returns:
        dict: A dictionary containing recall, precision, and F1-score for ROUGE-1.
    """
    scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
    scores = scorer.score(human_summary, ai_summary)
    
    rouge_scores = {}
    for key in scores:
        rouge_scores[key] = {
            'recall': scores[key].recall,
            'precision': scores[key].precision,
            'f1': scores[key].fmeasure
        }
    
    return rouge_scores

def generate_pdf_report(df, output_path):
    """
    Generates a PDF report summarizing ROUGE scores for multiple case summaries.

    Args:
        df (pd.DataFrame): A DataFrame containing the case titles and their ROUGE scores.
            The DataFrame should have the columns: 'GR Title', 'Recall', 'Precision', 'F1'.
        output_path (str): The file path where the generated PDF report will be saved.

    Returns:
        None: The report is saved directly to the specified output path.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=9)
    
    pdf.cell(0, 10, "LSATP ROUGE Scores", ln=True, align='C')
    pdf.ln(10)
    
    column_widths = [60, 40, 40, 40]
    headers = ["GR Title", "Recall", "Precision", "F1"]
    for header, width in zip(headers, column_widths):
        pdf.cell(width, 10, header, border=1, align='C')
    pdf.ln()
    
    for _, row in df.iterrows():
        pdf.cell(column_widths[0], 10, row['GR Title'], border=1)
        pdf.cell(column_widths[1], 10, f"{row['Recall']:.4f}", border=1, align='C')
        pdf.cell(column_widths[2], 10, f"{row['Precision']:.4f}", border=1, align='C')
        pdf.cell(column_widths[3], 10, f"{row['F1']:.4f}", border=1, align='C')
        pdf.ln()
    
    pdf.cell(column_widths[0], 10, "Average", border=1)
    pdf.cell(column_widths[1], 10, f"{df['Recall'].mean():.4f}", border=1, align='C')
    pdf.cell(column_widths[2], 10, f"{df['Precision'].mean():.4f}", border=1, align='C')
    pdf.cell(column_widths[3], 10, f"{df['F1'].mean():.4f}", border=1, align='C')
    
    pdf.output(output_path)

if __name__ == "__main__":
    results = []

    main_folder = 'Evaluation/Court_Cases'

    for case_folder in os.listdir(main_folder):
        case_path = os.path.join(main_folder, case_folder)
        if os.path.isdir(case_path):
            human_summary_path = os.path.join(case_path, 'human summary.txt')
            ai_summary_path = os.path.join(case_path, 'LSATP_summary.txt')

            try:
                human_summary = read_file(human_summary_path, 'utf-8')
                ai_summary = read_file(ai_summary_path, 'iso-8859-1')
                
                scores = compute_rouge_scores(human_summary, ai_summary)
                
                results.append({
                    'GR Title': case_folder,
                    'Recall': scores['rouge1']['recall'],
                    'Precision': scores['rouge1']['precision'],
                    'F1': scores['rouge1']['f1']
                })

            except FileNotFoundError as e:
                print(f"Warning: {e}")
    
    # Debugging: Print out the results list to verify its contents
    print("Results:", results)
    
    # Create DataFrame from results if results is not empty
    if results:
        df = pd.DataFrame(results)
        generate_pdf_report(df, 'Evaluation/Rouge_Scores_PDF/LSATP_ROUGE_Scores.pdf')
        print("PDF report generated: LSATP_ROUGE_Scores.pdf")
    else:
        print("No results to process. Please check if the files are correctly named and located.")

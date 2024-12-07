# =============================================================================
# Program Title: ROUGE Score Comparison and Paired T-Test Analysis
# Programmer: Jewell Anne Diamante
# Date Written: November 15, 2024
# Date Revised: November 18, 2024
#
# Purpose:
#     This program extracts ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
#     scores from two PDF files and performs statistical analysis to compare the
#     performance of two summarization systems (e.g., LSATP and Summit). It uses
#     paired t-tests to evaluate the significance of the differences in Recall,
#     Precision, and F1 scores for the given systems.
#
# Where the program fits in the general system design:
#     This program is part of an evaluation pipeline for comparing summarization
#     performance between different AI systems or configurations. It is crucial in
#     identifying which approach yields better results, guiding the optimization and
#     fine-tuning of summarization models in applications such as legal document
#     summarization, news aggregation, and educational content generation.
#
# Data Structures, Algorithms, and Control:
#     - Data Structures:
#         - **Pandas DataFrame (`df1`, `df2`)**: Stores the extracted table data
#           for each system, including the metrics (Recall, Precision, F1).
#         - **Dictionary (`results`)**: Holds the t-test results, including the
#           t-statistic, p-value, and mean difference for each metric.
#     - Algorithms:
#         - **Table Extraction**: The `extract_table_from_pdf` function extracts
#           tabular data from PDF files and converts them into pandas DataFrames.
#         - **Data Alignment**: Ensures that the two DataFrames are aligned on the
#           `GR Title` column to allow valid paired t-tests.
#         - **Paired T-Test**: The `ttest_rel` function from the `scipy.stats` module
#           performs a statistical test for the paired samples.
#     - Control:
#         - The program follows these steps:
#           1. Extracts ROUGE scores from two PDF files into DataFrames.
#           2. Validates alignment of the data to ensure consistency in comparisons.
#           3. Computes paired t-tests for Recall, Precision, and F1 metrics.
#           4. Outputs the statistical results and their interpretations.
#         - Exception handling ensures data alignment before statistical analysis
#           and handles errors during numeric conversion.
# =============================================================================



import pdfplumber
import pandas as pd
from scipy.stats import ttest_rel, skew, kurtosis
from fpdf import FPDF


def extract_table_from_pdf(pdf_path):
    """
    Extracts tables from a PDF file and converts them into a pandas DataFrame.

    Args:
        pdf_path (str): The path to the PDF file containing the tables.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted data with columns:
                      ["GR Title", "Recall", "Precision", "F1"].
    """
    data = []
    columns = ["No.", "GR Title", "Recall", "Precision", "F1"]

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # Skip header rows
                    if row[1] == "GR Title":
                        continue
                    data.append(row)

    df = pd.DataFrame(data, columns=columns)

    # Convert numeric columns to float
    numeric_columns = ["Recall", "Precision", "F1"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


def generate_pdf_table(df1, df2, results, output_pdf):
    """
    Generates a PDF containing the paired t-test results in table format.

    Args:
        df1 (pd.DataFrame): DataFrame for the first system.
        df2 (pd.DataFrame): DataFrame for the second system.
        results (dict): Dictionary of paired t-test results.
        output_pdf (str): Path to the output PDF file.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Add title
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Paired T-Test Analysis of ROUGE Scores", ln=True, align="C")

    # Add table header
    pdf.set_font("Arial", size=10)
    pdf.cell(20, 10, "No.", 1, 0, "C")
    pdf.cell(80, 10, "G.R Title", 1, 0, "C")
    pdf.cell(30, 10, "LSATP FScore", 1, 0, "C")
    pdf.cell(30, 10, "Summit FScore", 1, 0, "C")
    pdf.cell(30, 10, "Difference", 1, 1, "C")

    # Populate table rows
    for index, row in df1.iterrows():
        diff = df2.loc[index, "F1"] - row["F1"]
        pdf.cell(20, 10, str(index + 1), 1, 0, "C")
        pdf.cell(80, 10, str(row["GR Title"]), 1, 0, "L")
        pdf.cell(30, 10, f"{df2.loc[index, 'F1']:.4f}", 1, 0, "C")
        pdf.cell(30, 10, f"{row['F1']:.4f}", 1, 0, "C")
        pdf.cell(30, 10, f"{diff:.4f}", 1, 1, "C")

    # Add statistics
    mean_diff = df2["F1"].mean() - df1["F1"].mean()
    std_diff = (df2["F1"] - df1["F1"]).std()
    skewness = skew(df2["F1"] - df1["F1"])
    kurt = kurtosis(df2["F1"] - df1["F1"])
    t_stat, p_value = ttest_rel(df2["F1"], df1["F1"])
    df = len(df1) - 1

    pdf.cell(200, 10, txt="", ln=True)  # Add a blank line

    # Add summary statistics
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(200, 10, txt="Summary Statistics", ln=True)

    pdf.set_font("Arial", size=10)
    pdf.cell(100, 10, "Mean Difference:", 1, 0)
    pdf.cell(100, 10, f"{mean_diff:.4f}", 1, 1)

    pdf.cell(100, 10, "Standard Deviation:", 1, 0)
    pdf.cell(100, 10, f"{std_diff:.4f}", 1, 1)

    pdf.cell(100, 10, "Calculated T-Value:", 1, 0)
    pdf.cell(100, 10, f"{t_stat:.4f}", 1, 1)

    pdf.cell(100, 10, "Skewness:", 1, 0)
    pdf.cell(100, 10, f"{skewness:.4f}", 1, 1)

    pdf.cell(100, 10, "Kurtosis:", 1, 0)
    pdf.cell(100, 10, f"{kurt:.4f}", 1, 1)

    pdf.cell(100, 10, "Degree of Freedom:", 1, 0)
    pdf.cell(100, 10, f"{df}", 1, 1)

    pdf.cell(100, 10, "P-Two Tail Value:", 1, 0)
    pdf.cell(100, 10, f"{p_value:.4f}", 1, 1)

    pdf.cell(100, 10, "T-Table Value (95% Confidence):", 1, 0)
    pdf.cell(100, 10, "1.96", 1, 1)  # Example value for 95% confidence

    conclusion = (
        "Significant Difference" if p_value < 0.05 else "No Significant Difference"
    )
    pdf.cell(100, 10, "Conclusion:", 1, 0)
    pdf.cell(100, 10, conclusion, 1, 1)

    # Save PDF
    pdf.output(output_pdf)


# Paths to the PDF files
summit_scores = "Evaluation/Rouge_Scores_PDF/Summit_ROUGE_Scores.pdf"
lsatp_scores = "Evaluation/Rouge_Scores_PDF/LSATP_ROUGE_Scores.pdf"

# Extract data from the PDFs
df1 = extract_table_from_pdf(summit_scores)
df2 = extract_table_from_pdf(lsatp_scores)

# Ensure both DataFrames are aligned
if not df1["GR Title"].equals(df2["GR Title"]):
    raise ValueError("GR Titles in the two PDFs do not match. Align data before proceeding.")

# Perform paired t-tests
metrics = ["Recall", "Precision", "F1"]
results = {}

for metric in metrics:
    # Perform t-test
    t_stat, p_value = ttest_rel(df2[metric], df1[metric])  # LSATP - Summit
    mean_difference = df2[metric].mean() - df1[metric].mean()

    # Store results
    results[metric] = {
        "t-statistic": t_stat,
        "p-value": p_value,
        "mean difference": mean_difference,
    }

# Generate PDF table
output_pdf = "Evaluation/Rouge_Scores_PDF/Paired_T_Test_Results.pdf"
generate_pdf_table(df1, df2, results, output_pdf)
print(f"Results saved to {output_pdf}")

# Display results
for metric, result in results.items():
    print(f"{metric}:")
    print(f"  Mean Difference = {result['mean difference']:.4f}")
    print(f"  t-statistic = {result['t-statistic']:.4f}")
    print(f"  p-value = {result['p-value']:.4f}")
    
    # Interpretation
    if result["p-value"] < 0.05:
        if result["mean difference"] > 0:
            print(f"  Positive significant difference: LSATP is better in {metric}.")
        else:
            print(f"  Negative significant difference: Summit is better in {metric}.")
    else:
        print(f"  No significant difference in {metric}.")
import os
from fpdf import FPDF
from rouge_score import rouge_scorer
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pdfplumber



def extract_sections(file_path):
    """
    Extracts 'FACTS:', 'ISSUES:', and 'RULINGS:' sections from a text file.
    """
    sections = {'FACTS': '', 'ISSUES': '', 'RULINGS': ''}
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        for section in sections.keys():
            if section + ":" in content:
                start = content.index(section + ":") + len(section) + 1
                end = content.find("\n\n", start)
                sections[section] = content[start:end].strip()
    return sections


def compute_rouge_scores(reference, candidate):
    """
    Computes ROUGE scores (Precision, Recall, F1-score) for a reference and candidate text.
    """
    scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
    scores = scorer.score(reference, candidate)
    return {
        'precision': scores['rouge1'].precision,
        'recall': scores['rouge1'].recall,
        'f1': scores['rouge1'].fmeasure
    }


def generate_pdf_report(df, output_path):
    """
    Generates a PDF report summarizing ROUGE scores for all cases.
    """
    pdf = FPDF(orientation='L', unit='mm', format='A4')  # Set to landscape
    pdf.add_page()
    pdf.set_font("Arial", size=9)

    # Title
    pdf.set_font("Arial", size=14, style="B")
    pdf.cell(0, 10, "LSATP ROUGE Score per Sections for both STRUCTURED and UNSTRUCTURED", ln=True, align="C")
    pdf.ln(10)

    # Header for the main columns
    pdf.set_font("Arial", size=10, style="B")
    pdf.cell(10, 10, "No.", border=1, align="C")
    pdf.cell(60, 10, "GR Title", border=1, align="C")

    # Merge cells for FACTS, ISSUES, and RULINGS headers
    pdf.cell(60, 10, "FACTS", border=1, align="C")
    pdf.cell(60, 10, "ISSUES", border=1, align="C")
    pdf.cell(60, 10, "RULINGS", border=1, align="C")
    pdf.ln()

    # Sub-columns for Recall, Precision, and F1 Score
    pdf.set_font("Arial", size=9, style="B")
    pdf.cell(10, 10, "", border=1)  # Placeholder for "No."
    pdf.cell(60, 10, "", border=1)  # Placeholder for "GR Title"
    for _ in range(3):  # Repeat for FACTS, ISSUES, RULINGS
        pdf.cell(20, 10, "Recall", border=1, align="C")
        pdf.cell(20, 10, "Precision", border=1, align="C")
        pdf.cell(20, 10, "F1 Score", border=1, align="C")
    pdf.ln()

    # Table rows
    pdf.set_font("Arial", size=9)
    for idx, row in df.iterrows():
        # Row number
        pdf.cell(10, 10, str(idx + 1), border=1, align="C")

        # GR Title column
        pdf.cell(60, 10, row['GR Title'], border=1, align="C")

        # FACTS columns (Recall, Precision, F1)
        pdf.cell(20, 10, f"{row['FACTS Recall']:.5f}", border=1, align="C")
        pdf.cell(20, 10, f"{row['FACTS Precision']:.5f}", border=1, align="C")
        pdf.cell(20, 10, f"{row['FACTS F1']:.5f}", border=1, align="C")

        # ISSUES columns (Recall, Precision, F1)
        pdf.cell(20, 10, f"{row['ISSUES Recall']:.5f}", border=1, align="C")
        pdf.cell(20, 10, f"{row['ISSUES Precision']:.5f}", border=1, align="C")
        pdf.cell(20, 10, f"{row['ISSUES F1']:.5f}", border=1, align="C")

        # RULINGS columns (Recall, Precision, F1)
        pdf.cell(20, 10, f"{row['RULINGS Recall']:.5f}", border=1, align="C")
        pdf.cell(20, 10, f"{row['RULINGS Precision']:.5f}", border=1, align="C")
        pdf.cell(20, 10, f"{row['RULINGS F1']:.5f}", border=1, align="C")

        pdf.ln()

    # Calculate averages for FACTS, ISSUES, and RULINGS
    avg_row = {
        'GR Title': 'Average',
        'FACTS Recall': df['FACTS Recall'].mean(),
        'FACTS Precision': df['FACTS Precision'].mean(),
        'FACTS F1': df['FACTS F1'].mean(),
        'ISSUES Recall': df['ISSUES Recall'].mean(),
        'ISSUES Precision': df['ISSUES Precision'].mean(),
        'ISSUES F1': df['ISSUES F1'].mean(),
        'RULINGS Recall': df['RULINGS Recall'].mean(),
        'RULINGS Precision': df['RULINGS Precision'].mean(),
        'RULINGS F1': df['RULINGS F1'].mean(),
    }
    # Highlight the average row
    pdf.set_fill_color(230, 230, 230)  # Light gray background for average row
    pdf.set_font("Arial", style='B', size=9)  # Bold font
    
    # Add average row
    pdf.set_font("Arial", size=9, style="B")
    pdf.cell(10, 10, "", border=1, align="C", fill=True)  # Blank cell for No.
    pdf.cell(60, 10, avg_row['GR Title'], border=1, align="C", fill=True)

    # FACTS columns
    pdf.cell(20, 10, f"{avg_row['FACTS Recall']:.5f}", border=1, align="C", fill=True)
    pdf.cell(20, 10, f"{avg_row['FACTS Precision']:.5f}", border=1, align="C", fill=True)
    pdf.cell(20, 10, f"{avg_row['FACTS F1']:.5f}", border=1, align="C", fill=True)

    # ISSUES columns
    pdf.cell(20, 10, f"{avg_row['ISSUES Recall']:.5f}", border=1, align="C", fill=True)
    pdf.cell(20, 10, f"{avg_row['ISSUES Precision']:.5f}", border=1, align="C", fill=True)
    pdf.cell(20, 10, f"{avg_row['ISSUES F1']:.5f}", border=1, align="C", fill=True)

    # RULINGS columns
    pdf.cell(20, 10, f"{avg_row['RULINGS Recall']:.5f}", border=1, align="C", fill=True)
    pdf.cell(20, 10, f"{avg_row['RULINGS Precision']:.5f}", border=1, align="C", fill=True)
    pdf.cell(20, 10, f"{avg_row['RULINGS F1']:.5f}", border=1, align="C", fill=True)


    # Output the PDF to file
    pdf.output(output_path)

def extract_table_from_pdf(pdf_path):
    """
    Extracts tabular data from the specified PDF file and returns it as a DataFrame.

    Parameters:
    pdf_path (str): Path to the PDF file.

    Returns:
    pd.DataFrame: DataFrame containing the extracted data.
    """
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract tables from the page
            tables = page.extract_tables()
            for table in tables:
                # Convert the table into rows
                for row in table:
                    # Append each row to the data
                    data.append(row)
    
    # Create a DataFrame from the extracted data
    if data:
        df = pd.DataFrame(data)
        return df
    else:
        print("No table data found in the PDF.")
        return pd.DataFrame()


def generate_bar_graphs(df, file_path):
    """
    Generates a bar graph comparing the LSA and SUMMIT
    """
    # Plot labels
    labels = ['Recall', 'Precision', 'F1']
    try:
        summit_df = extract_table_from_pdf('Evaluation\Rouge_Scores_PDF\Section\SUMMIT_Rouge_Sections.pdf')
        lsatp_df = extract_table_from_pdf('Evaluation\Rouge_Scores_PDF\Section\LSATP_Rouge_Sections.pdf')

        # Data extraction for LSATP
        lsatp = {
            'Facts': [lsatp_df[2].iloc[-1], lsatp_df[3].iloc[-1], lsatp_df[4].iloc[-1]],
            'Issues': [lsatp_df[5].iloc[-1], lsatp_df[6].iloc[-1], lsatp_df[7].iloc[-1]],
            'Ruling': [lsatp_df[8].iloc[-1], lsatp_df[9].iloc[-1], lsatp_df[10].iloc[-1]],
        }
        print(lsatp)

        # Data extraction for SUMMIT
        summit = {
            'Facts': [summit_df[2].iloc[-1], summit_df[3].iloc[-1], summit_df[4].iloc[-1]],
            'Issues': [summit_df[5].iloc[-1], summit_df[6].iloc[-1], summit_df[7].iloc[-1]],
            'Ruling': [summit_df[8].iloc[-1], summit_df[9].iloc[-1], summit_df[10].iloc[-1]],
        }
        print(summit)
        
        # Width and position of bar
        x = np.arange(len(labels))
        width = 0.35

        # Convert string values to floats
        for key in lsatp.keys():
            lsatp[key] = list(map(float, lsatp[key]))
            summit[key] = list(map(float, summit[key]))

        # Create a comparison plot
        for court_label in ['Facts', 'Issues', 'Ruling']:
            fig, ax = plt.subplots(figsize=(8, 6))
            lsatp_bar = ax.bar(x - width / 2, lsatp[court_label], width, label='LSATP', color='#AE445A')
            summit_bar = ax.bar(x + width / 2, summit[court_label], width, label='SUMMIT', color='#432E54')

            ax.set_ylabel('Scores')
            ax.set_title(f'Comparison of "{court_label}" Court Case Label of LSATP and SUMMIT')
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            ax.legend()

            plt.tight_layout()
            plt.savefig(f'{file_path}{court_label}_comparison.png')
            
        # Create LSATP court case plot
        fig, ax = plt.subplots(figsize=(8, 6))
        width = 0.25
        ax.bar(x - width, lsatp['Facts'], width, label='Facts', color='#AE445A')
        ax.bar(x, lsatp['Issues'], width, label='Issues', color='#4B4376')
        ax.bar(x + width, lsatp['Ruling'], width, label='Rulings', color='#432E54')

        ax.set_ylabel('Scores')
        ax.set_title('Court Case Label of LSATP')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        plt.tight_layout()
        plt.savefig(os.path.join(file_path, 'Court_case_labels_LSATP.png'))
        print(f'Saved images to {file_path}.')

    except FileNotFoundError as e:
        print("File not found. Check if the specified file paths are correct.")
        print(e)

    except KeyError as e:
        print("Dataframe does not have the required columns. Please check the data structure.")
        print(e)

    except Exception as e:
        print("An unexpected error occurred.")
        print(e)


if __name__ == "__main__":
    results = []
    main_folder = 'Evaluation/Court_Cases'

    for idx, case_folder in enumerate(os.listdir(main_folder), start=1):
        case_path = os.path.join(main_folder, case_folder)
        if os.path.isdir(case_path):
            human_summary_path = os.path.join(case_path, 'human summary.txt')
            ai_summary_path = os.path.join(case_path, 'LSATP_summary.txt')

            try:
                human_sections = extract_sections(human_summary_path)
                ai_sections = extract_sections(ai_summary_path)

                row = {"GR Title": case_folder}
                for section in ['FACTS', 'ISSUES', 'RULINGS']:
                    scores = compute_rouge_scores(human_sections[section], ai_sections[section])
                    row[f"{section} Precision"] = scores['precision']
                    row[f"{section} Recall"] = scores['recall']
                    row[f"{section} F1"] = scores['f1']
                results.append(row)

            except FileNotFoundError as e:
                print(f"Warning: {e}")

    # Generate a DataFrame
    if results:
        df = pd.DataFrame(results)

        # Generate the PDF report
        pdf_path = 'Evaluation/Rouge_Scores_PDF/Section/LSATP_Rouge_Sections.pdf'
        image_path = 'Evaluation/Bar_Graph/'
        generate_pdf_report(df, pdf_path)
        generate_bar_graphs(df, image_path)
        print(f"PDF report generated at: {pdf_path}")
    else:
        print("No results to process. Please check if the files are correctly named and located.")

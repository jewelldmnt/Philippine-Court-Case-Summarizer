# =============================================================================
# Program Title: Segmentation Evaluation Using WindowDiff and Pk Score
# Programmer: Jewell Anne Diamante
# Date Written: October 17, 2024
# Date Revised: October 17, 2024
#
# Purpose:
#     This program is designed to evaluate the performance of an AI-based text
#     segmentation system by comparing its segmentation output against a reference
#     (human) segmentation. The evaluation is performed using two metrics:
#     WindowDiff and Pk score. The segmentation is based on boundaries marked by
#     labels such as 'FACTS:', 'ISSUES:', and 'RULINGS:', which are used to define
#     the segments in the text.
#
# Where the program fits in the general system design:
#     This program is part of a larger system aimed at evaluating AI-generated
#     segmentations in natural language processing (NLP) tasks. It processes
#     segmentation results, compares them to reference segmentations, and computes
#     relevant metrics to measure the accuracy of AI segmentation models. It is
#     useful in applications like legal document segmentation, where structured
#     text categories are important for further analysis.
#
# Data Structures, Algorithms, and Control:
#     - Data Structures:
#         - **List (`segmentation`)**: Stores the segmentation boundaries (0 or 1),
#           where 1 indicates a segmentation boundary and 0 indicates no boundary.
#           The list is generated based on the presence of specific labels in the input.
#         - **List (`reference_boundaries`, `hypothesis_boundaries`)**: The boundaries
#           are grouped into segments of consecutive 0s or 1s. These lists represent
#           the reference and predicted segment lengths.
#     - Algorithms:
#         - **Segmentation Loading**: The `load_segmentation_with_labels` function loads
#           segmentation data from a file and identifies boundaries using specific
#           labels ('FACTS:', 'ISSUES:', 'RULINGS:').
#         - **Segmentation Evaluation**: The `evaluate_segmentation` function calculates
#           the WindowDiff and Pk scores using the `segeval` library, which compares
#           the reference segmentation against the AI's segmentation.
#     - Control:
#         - The program follows a clear step-by-step process:
#           1. It loads the segmentation data for both the human reference and AI
#              predictions from text files.
#           2. It computes the segmentation evaluation metrics using the
#              `evaluate_segmentation` function.
#           3. It outputs the WindowDiff and Pk scores, which help assess the quality
#              of the AI-generated segmentation.
# =============================================================================


import segeval
from itertools import groupby


def load_segmentation_with_labels(file_path, encoding="utf-8"):
    """
    Load segmentation boundaries based on the labels 'FACTS:', 'ISSUES:', and 
        'RULINGS:'.

    :param file_path: Path to the segmentation file.
    :param encoding: Encoding format used to read the file.
    :return: A list of 0s and 1s indicating segmentation boundaries.
    """
    segmentation = []

    # Define the labels that indicate segment boundaries
    boundary_labels = {"FACTS:", "ISSUES:", "RULINGS:"}

    # Open the file with the specified encoding
    with open(file_path, "r", encoding=encoding, errors="replace") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace

            if line in boundary_labels:
                # If the line is a boundary label, append a 1 (boundary)
                segmentation.append(1)
            else:
                # Otherwise, append a 0 (no boundary)
                segmentation.append(0)

    return segmentation


def evaluate_segmentation(reference, hypothesis):
    """
    Evaluate the segmentation using WindowDiff and Pk score.

    :param reference: List of 0s and 1s, where 1 indicates a true segmentation boundary.
    :param hypothesis: List of 0s and 1s, where 1 indicates a predicted segmentation boundary.
    :return: A tuple with WindowDiff and Pk score.
    """
    # Convert to a format that segeval expects (list of segment lengths)
    reference_boundaries = [len(list(g)) for k, g in groupby(reference)]
    hypothesis_boundaries = [len(list(g)) for k, g in groupby(hypothesis)]

    # Calculate WindowDiff and Pk scores
    wd_score = segeval.window_diff(reference_boundaries, hypothesis_boundaries)
    pk_score = segeval.pk(reference_boundaries, hypothesis_boundaries)

    return wd_score, pk_score


# Load human and AI segmentation with labels, specifying encoding if needed
human_segmentation = load_segmentation_with_labels(
    "Segmentation/Human/human_segmentation.txt", encoding="utf-8"
)
ai_segmentation = load_segmentation_with_labels(
    "Segmentation/AI/ai_segmentation.txt", encoding="ISO-8859-1"
)

# Evaluate the AI segmentation against the human segmentation
wd, pk = evaluate_segmentation(human_segmentation, ai_segmentation)

# Print the results
print(f"WindowDiff: {wd}, Pk Score: {pk}")

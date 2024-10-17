import segeval
from itertools import groupby

def load_segmentation_with_labels(file_path, encoding='utf-8'):
    """
    Load segmentation boundaries based on the labels 'FACTS:', 'ISSUES:', and 'RULINGS:'.
    
    :param file_path: Path to the segmentation file.
    :param encoding: Encoding format used to read the file.
    :return: A list of 0s and 1s indicating segmentation boundaries.
    """
    segmentation = []
    
    # Define the labels that indicate segment boundaries
    boundary_labels = {'FACTS:', 'ISSUES:', 'RULINGS:'}
    
    # Open the file with the specified encoding
    with open(file_path, 'r', encoding=encoding, errors='replace') as file:
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
human_segmentation = load_segmentation_with_labels('Segmentation/Human/human_segmentation.txt', encoding='utf-8')
ai_segmentation = load_segmentation_with_labels('Segmentation/AI/ai_segmentation.txt', encoding='ISO-8859-1')

# Evaluate the AI segmentation against the human segmentation
wd, pk = evaluate_segmentation(human_segmentation, ai_segmentation)

# Print the results
print(f"WindowDiff: {wd}, Pk Score: {pk}")

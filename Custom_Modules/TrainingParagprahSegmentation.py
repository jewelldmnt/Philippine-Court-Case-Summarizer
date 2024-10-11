import pandas as pd
import re

    
# Function to extract text line by line, handling NaN values
def get_lines(text):
    """
    Description:
        Extracts lines from the input text after preprocessing.

        This function checks if the input text is NaN (not a number). If it is NaN,
        an empty list is returned. If the text is valid, it is converted to lowercase,
        preprocessed using the `preprocess_text` function, and then split into individual
        lines. The resulting lines are returned as a list.

    Parameters:
        text (str or NaN): The input text to be processed, which may be a string or NaN.

    Returns:
        list: A list of lines extracted from the preprocessed text. Returns an empty list
        if the input text is NaN.
    """
    if pd.isna(text):  # Check if the text is NaN
        return []
    # Preprocess the text before splitting into lines
    text = text.lower()  # Convert text to lowercase and preprocess
    return str(text).splitlines()  # Ensure text is a string before splitting into lines

# Load the CSV file
df = pd.read_csv('full_court_cases.csv')

# Create lists to store the headings (lines) and labels
headings = []
labels = []

# Loop through each row in the dataframe
for index, row in df.iterrows():

    # Extract lines for each section (facts, issues, ruling)
    facts_lines = get_lines(row['facts'])
    issues_lines = get_lines(row['issues'])
    ruling_lines = get_lines(row['ruling'])

    # Add the lines and corresponding labels to the lists
    for line in facts_lines:
        if line.strip() and line not in headings:  # Avoid empty lines and duplicates
            headings.append(line)
            labels.append("facts")

    for line in issues_lines:
        if line.strip() and line not in headings:  # Avoid empty lines and duplicates
            headings.append(line)
            labels.append("issues")

    for line in ruling_lines:
        if line.strip() and line not in headings:  # Avoid empty lines and duplicates
            headings.append(line)
            labels.append("ruling")

# Create a new dataframe with the headings (lines) and labels
new_df = pd.DataFrame({
    'heading': headings,
    'label': labels
})

# Save the new dataset to a CSV file
new_df.to_csv('court_cases_headings_labels.csv', index=False)

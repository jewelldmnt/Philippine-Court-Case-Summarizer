import pandas as pd
import re

'''   
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
new_df.to_csv('court_cases_headings_labels.csv', index=False)'''

class paragraph_segmentation:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.headings = []
        self.labels = []

        # Convert the paragraphs into lines
        self.extract_lines()

    def output_segmented_csv(self):
        self.new_df.to_csv('court_cases_headings_labels.csv', index=False)

    def extract_lines(self):
        # Loop through each row in the dataframe
        for index, row in self.df.iterrows():
            # Extract lines for each section (facts, issues, ruling) and pre-clean the data
            facts_lines = self.get_lines(self.pre_clean(row['facts']))
            issues_lines = self.get_lines(self.pre_clean(row['issues']))
            ruling_lines = self.get_lines(self.pre_clean(row['ruling']))

            # Add the lines and corresponding labels to the lists
            for line in facts_lines:
                if line.strip() and line not in self.headings:
                    self.headings.append(line)
                    self.labels.append("facts")

            for line in issues_lines:
                if line.strip() and line not in self.headings:
                    self.headings.append(line)
                    self.labels.append("issues")

            for line in ruling_lines:
                if line.strip() and line not in self.headings:
                    self.headings.append(line)
                    self.labels.append("ruling")

        # Create a new dataframe with the headings (lines) and labels
        self.new_df = pd.DataFrame({
            'heading': self.headings,
            'label': self.labels
        })
        
    def get_lines(self, text):
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

    def pre_clean(self, text):
        """
        Cleans up the text by removing or replacing specific patterns (e.g., punctuation, abbreviations) to
        standardize the input.

        Parameters:
            text (str): The raw input text.

        Returns:
            text (str): The cleaned and standardized text.
        """
        try:
            # Remove all phrases that start with "(emphasis" or "(citations", and end with a closing parenthesis.
            text = re.sub(r"\(emphasis[^\)]*\)", "", text)
            text = re.sub(r"\(emphases[^\)]*\)", "", text)
            text = re.sub(r"\(citations[^\)]*\)", "", text)
            text = re.sub(r"emphasis in the original\.", "", text)

            # Replaces the Unicode double prime symbol (″) with a space.
            text = re.sub(r"\u2033", '"', text)

            # Replaces the Unicode prime symbol (′) with a space.
            text = re.sub(r"\u2032", "'", text)

            # Replace possessive forms like "person's" or "persons'"
            cleaned_text = re.sub(r"(\w+)'s", r'\1', text)  # Handles "person's" -> "person"
            cleaned_text = re.sub(r"(\w+)s'", r'\1', cleaned_text)  # Handles "peoples'" -> "people"

            # Replaces instances of 'section 1.' (or any number) with 'section 1', removing the dot after the number.
            text = re.sub(r"section (\d+)\.", r"section \1", text)

            # Replaces 'sec.' with 'sec', removing the period after 'sec'.
            text = re.sub(r"sec\.", r"sec", text)

            # Replaces 'p.d.' with 'pd', removing the periods.
            text = re.sub(r"p\.d\.", r"pd", text)

            # Replaces 'no.' with 'number', changing the abbreviation to the full word.
            text = re.sub(r"\bno\.\b", r"number", text)

            # Replaces the abbreviation 'rtc' with 'regional trial court'.
            text = re.sub(r"\brtc\b", "regional trial court", text)

            # Removes any of the following punctuation characters: ( ) , ' " ’ ” [ ].
            text = re.sub(r"[(),'\"’”\[\]]", " ", text)

            # Removes the special characters “ and ” (different types of quotation marks).
            text = re.sub(r"[“”]", " ", text)

            # Replaces standalone 'g' with a space (possibly targeting abbreviations like 'G').
            text = re.sub(r"\bg\b", " ", text)

            # Replaces standalone 'r' with a space (possibly targeting abbreviations like 'R').
            text = re.sub(r"\br\b", " ", text)

            # Replaces multiple spaces (except for newlines) with a single space.
            text = re.sub(r"([^\S\n]+)", " ", text)
            
            # Remove single letters or numbers followed by punctuation like a) or 1.
            text = re.sub(r"\b[a-zA-Z0-9]\)\s?", "", text)  # Matches single letters or digits followed by ')'
            text = re.sub(r"\b[a-zA-Z0-9]\.\s?", "", text)  # Matches single letters or digits followed by '.'

            # Remove any kind of leading or trailing invisible characters (including non-breaking spaces)
            text = re.sub(r'^[\s\u200b\u00a0]+|[\s\u200b\u00a0]+$', '', text, flags=re.MULTILINE)

            # Removes leading and trailing spaces from the text.
            return text.strip()
        except Exception as e:
            return ''
import re


class Preprocessing:
    def __init__(self):
        pass

    def clean_text(self, text: str) -> str:
        """
        Description:
            Cleans up text by removing or replacing certain characters and patterns.

        Parameters:
            text (str): The text to clean up.
        Returns:
            str: The cleaned text.
        """
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

        # Replaces the Unicode double prime symbol (″) with a space.
        text = re.sub(r"\u2033", " ", text)

        # Replaces the Unicode prime symbol (′) with a space.
        text = re.sub(r"\u2032", " ", text)

        # Replaces standalone 'g' with a space (possibly targeting abbreviations like 'G').
        text = re.sub(r"\bg\b", " ", text)

        # Replaces standalone 'r' with a space (possibly targeting abbreviations like 'R').
        text = re.sub(r"\br\b", " ", text)

        # Replaces multiple spaces (except for newlines) with a single space.
        text = re.sub(r"([^\S\n]+)", " ", text)

        # Removes leading and trailing spaces from the text.
        return text.strip()

    def tokenize_by_paragraph(self, text: str) -> list:
        """
        Description:
            Tokenizes the text into a list of paragraphs.

        Parameters:
            text (str): The text to tokenize into paragraphs.

        Returns:
            list: A list of paragraphs.
        """
        # Split the text into paragraphs based on empty lines
        paragraphs = text.split("\n")

        # Filter out empty paragraphs and trim any extra spaces
        paragraph_list = [
            paragraph.strip() for paragraph in paragraphs if paragraph.strip()
        ]

        return paragraph_list

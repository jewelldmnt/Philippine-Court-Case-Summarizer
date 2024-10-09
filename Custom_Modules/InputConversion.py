class InputConversion:
    def convert_to_txt(self, input_string, file_name="output.txt"):
        """    
        Description:
            This function takes an input string and writes it into a .txt file.
            It creates a file with the specified name, or defaults to "output.txt"
            if no name is provided.

        Parameters:
            input_string (str): The string content to be written to the file.
            file_name (str): The name of the output .txt file (default is "output.txt").

        Returns:
            None: Writes the content to a file and prints a success message.
        """
        try:
            with open(file_name, 'w') as file:
                file.write(input_string)
            print(f"Text successfully written to {file_name}")
        except Exception as e:
            print(f"Error writing to file: {e}")
    
    def remove_reference(self, text):
        """    
        Description:
            This function finds the last occurrence of the phrase "SO ORDERED" in the 
            input text. It truncates the text right after this phrase, removing 
            any content that follows. If the phrase is not found, the function 
            returns the text unchanged.

        Parameters:
            text (str): The input text string that may contain the "SO ORDERED" phrase.

        Returns:
            str: The truncated text up to and including the last occurrence of "SO ORDERED",
                or the original text if the phrase is not found.
        """
        stop_pos = text.rfind("SO ORDERED")
        return text[:stop_pos + 11] if stop_pos != -1 else text

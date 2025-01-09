from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np

class WordCloudGenerator:
    def __init__(self, width=800, height=400, background_color='white', colormap='copper'):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.colormap = colormap

    def create_wordcloud(self, text, output_file="wordcloud.jpg"):
        """

        :param text: The input text for the word cloud.
        :param output_file: The output file name (default is 'wordcloud.jpg').
        """

        # Generate the word cloud
        wordcloud = WordCloud(
            stopwords=STOPWORDS,
            width=self.width,
            height=self.height,
            background_color=self.background_color,
            colormap=self.colormap,
        ).generate(text)

        # Save the word cloud as an image file
        wordcloud.to_file(output_file)

        # Display the word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        print(f"Word cloud saved as {output_file}")
        
# Example usage
if __name__ == "__main__":
    generator = WordCloudGenerator()
    sample_text = """
    Python is a powerful programming language that is widely used in various fields including data science, web development,
    machine learning, artificial intelligence, and more. It is known for its simplicity and readability, making it an excellent
    choice for beginners and professionals alike.
    """
    generator.create_wordcloud(sample_text, "./website/public/images/wordcloud.jpg")

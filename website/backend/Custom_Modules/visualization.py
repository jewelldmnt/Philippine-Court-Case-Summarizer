import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from wordcloud import WordCloud
from preprocessing_v3 import *
import collections


class visualization:
    def __init__(self):
        pass

    def wordcloud(lists_of_tokens):
        """
        Plot the wordcloud based on a list of lists of tokens.

        Args:
        lists_of_tokens: A list of lists of tokens.
        """

        # Flatten the list of lists into a single list and count token occurrences
        all_tokens = [token for sublist in lists_of_tokens for token in sublist]
        token_counts = collections.Counter(all_tokens)

        # Generate wordcloud using the token counts dictionary
        wordcloud = WordCloud().generate_from_frequencies(token_counts)

        # Display the wordcloud
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    def plot_top_tokens(lists_of_tokens, n=7):
        """
        Plots the top n tokens with highest count from a list of lists.

        Args:
        lists_of_tokens: A list of lists of tokens.
        n: The number of top tokens to plot.
        """

        # Flatten the list of lists into a single list
        all_tokens = [token for sublist in lists_of_tokens for token in sublist]

        token_counts = collections.Counter(all_tokens)
        top_tokens = token_counts.most_common(n)

        labels, counts = zip(*top_tokens)
        plt.bar(labels, counts)
        plt.xlabel("Token")
        plt.ylabel("Count")
        plt.title("Top {} Tokens".format(n))
        plt.show()

    def plot_token_counts(list1, list2, list3):
        """
        Plots the token counts for three lists of lists.

        Args:
        list1: The first list of lists of tokens.
        list2: The second list of lists of tokens.
        list3: The third list of lists of tokens.
        """

        counts1 = sum(len(sublist) for sublist in list1)
        counts2 = sum(len(sublist) for sublist in list2)
        counts3 = sum(len(sublist) for sublist in list3)

        labels = ["List 1", "List 2", "List 3"]
        counts = [counts1, counts2, counts3]

        plt.bar(labels, counts)
        plt.xlabel("List")
        plt.ylabel("Token Count")
        plt.title("Token Counts for Three Lists")
        plt.show()

    def print_average(list1, list2, list3):
        """
        Prints the token counts and percentages for three lists of lists.

        Args:
        list1: The first list of lists of tokens.
        list2: The second list of lists of tokens.
        list3: The third list of lists of tokens.
        """

        # Calculate total token count
        total_count = (
            sum(len(sublist) for sublist in list1)
            + sum(len(sublist) for sublist in list2)
            + sum(len(sublist) for sublist in list3)
        )

        # Calculate individual list percentages
        if total_count == 0:
            percentages = [0, 0, 0]  # Handle division by zero
        else:
            percentages = [
                (sum(len(sublist) for sublist in list1) / total_count) * 100,
                (sum(len(sublist) for sublist in list2) / total_count) * 100,
                (sum(len(sublist) for sublist in list3) / total_count) * 100,
            ]

        # Print the results
        print("List 1: {:.2f}%".format(percentages[0]))
        print("List 2: {:.2f}%".format(percentages[1]))
        print("List 3: {:.2f}%".format(percentages[2]))

    def average_token_length(lists_of_tokens):
        """
        Calculates the average, highest, and lowest length of tokens within a list of lists.

        Args:
        lists_of_tokens: A list of lists of tokens.

        Returns:
        A tuple containing the average, highest, and lowest length of tokens.
        """

        total_length = 0
        total_tokens = 0
        highest_length = 0
        lowest_length = float("inf")

        for tokens in lists_of_tokens:
            token_length = len(tokens)
            total_length += token_length
            total_tokens += 1
            highest_length = max(highest_length, token_length)
            lowest_length = min(lowest_length, token_length)

        if total_tokens == 0:
            print("No length")

        average_length = total_length / total_tokens
        print("average court case length: ", average_length)
        print("highest court case length: ", highest_length)
        print("lowest court case length: ", lowest_length)

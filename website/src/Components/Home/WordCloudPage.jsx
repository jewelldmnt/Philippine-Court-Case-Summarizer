/**
 * Program Title: Court Case Summarizer - WordCloud Component
 *
 * Programmer: Nicholas Dela Torre, Jewell Anne Diamante
 * Date Written: October 12, 2024
 * Date Revised: January 23, 2025
 *
 * Purpose:
 *    This component is part of the Court Case Summarizer project. It visually
 *    represents word frequency data in a word cloud format, displaying the
 *    prominence of words based on their frequency.
 *
 * Where the Program Fits in the General System Design:
 *    The WordCloud component serves as a visual data representation tool in the
 *    frontend, illustrating frequently occurring words or phrases from court
 *    case documents. It complements the summarizer's data analysis by providing
 *    insights into key terms in a concise graphical format.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering word cloud elements dynamically.
 *    - Tailwind CSS classes: Used for styling and layout adjustments.
 *
 * Control Flow and Logic:
 *    1. `getFontSize`: Calculates the font size of each word based on its frequency,
 *       with scaling to accommodate varying frequency ranges.
 *    2. `map`: Iterates over `stats` array to generate positioned and sized words
 *       for the word cloud.
 *    3. Conditional Rendering: Displays a message if `stats` data is unavailable.
 *
 * Key Variables:
 *    - `stats`: Array of word frequency data, where each entry contains a frequency,
 *      unigram or bigram, and rank to identify and display the term appropriately.
 *    - `getFontSize`: Helper function that returns a size for each word based on
 *      the min-max frequency range.
 */
import "d3-transition";
import { select } from "d3-selection";
import WordCloud from "react-wordcloud";
import { removeStopwords } from "stopword"; // Import stopword module
import { useContext } from "react";
import { ThemeContext } from "../../ThemeContext";

import "tippy.js/dist/tippy.css";
import "tippy.js/animations/scale.css";

const WordCloudPage = ({ file_text }) => {
  /**
   * WordCloud component that generates and renders a word cloud
   * based on the frequencies of words in the given text,
   * excluding stopwords, numbers, and words with fewer than 3 letters.
   *
   * @param {string} file_text - The text content to process for the word cloud.
   *
   * @returns {JSX.Element}
   */

  const getWordCounts = (str) => {
    // Handle edge cases for invalid input

    if (!str || typeof str !== "string") return [];

    // Process text: convert to lowercase, remove punctuation, split into words
    const words = str
      .toLowerCase()
      .replace(/[^\w\s]/g, "") // Remove punctuation
      .split(/\s+/); // Split by spaces

    // Remove stopwords, numbers, and words with fewer than 3 letters
    const filteredWords = removeStopwords(words).filter(
      (word) => isNaN(word) && word.length > 3 // Exclude numbers and short words
    );

    // Count word occurrences using reduce
    return Object.entries(
      filteredWords.reduce((counts, word) => {
        counts[word] = (counts[word] || 0) + 1;
        return counts;
      }, {})
    ).map(([word, count]) => ({ text: word, value: count }));
  };

  const words = file_text ? getWordCounts(file_text) : [];
  console.log("words:", words);
  const { isDarkMode } = useContext(ThemeContext);

  if (!words || words.length === 0) {
    return <div>No words to display</div>;
  }

  const options = {
    rotations: 2,
    rotationAngles: [0, -90],
    padding: 1,
    fontSizes: [24, 84],
    fontFamily: "Montserrat, sans-serif",
    colors: isDarkMode
      ? // ? ["#a7bac6", "#3a83b7", "#739bb7"] // Word colors for dark mode option 1
        // ["#bfd5e3", "#3a83b7", "#f26881"] // Word colors for dark mode option 2
        ["#bfd5e3", "#e09f95", "#d66636", "#e89572"]
      : // : ["#09324d", "#3a83b7", "#f26881"], // Word colors for light mode 1
        ["#222224", "#b37159", "#b04e2b", "#f09b67"], // Word colors for light mode option2
  };

  const getCallback = (callback) => (word, event) => {
    if (!word || !event) return;
    const isActive = callback !== "onWordMouseOut";
    select(event.target)
      .on("click", () => {
        if (isActive) {
          window.open(`https://duckduckgo.com/?q=${word.text}`, "_blank");
        }
      })
      .transition()
      .attr("background", "white")
      .attr("text-decoration", isActive ? "underline" : "none");
  };
  const callbacks = {
    getWordTooltip: (word) =>
      `The word "${word.text}" appears ${word.value} times.`,
    onWordClick: getCallback("onWordClick"),
    onWordMouseOut: getCallback("onWordMouseOut"),
    onWordMouseOver: getCallback("onWordMouseOver"),
  };
  return (
    <div className="h-full w-full flex justify-center items-center overflow-hidden p-5 m-0">
      <WordCloud callbacks={callbacks} words={words} options={options} />
    </div>
  );
};

export default WordCloudPage;

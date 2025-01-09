/**
 * Program Title: Court Case Summarizer - WordCloud Component
 *
 * Programmer: Nicholas Dela Torre, Jewell Anne Diamante
 * Date Written: October 12, 2024
 * Date Revised: January 9, 2025
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
import { useEffect, useState } from "react";
const WordCloud = ({ file_id }) => {
  /**
   * WordCloud component that renders a pre-generated word cloud image
   * based on the type of word (unigram or bigram).
   *
   * @param {string} file_id - The ID of the selected file.
   *
   * @returns {JSX.Element}
   */

  useEffect(() => {
    if (file_id) {
      console.log("File ID for WordCloud: ", file_id);
      // Fetch or process data related to the word cloud using file_id
      // Example: Fetch word cloud image or generate word cloud
    }
  }, [file_id]);

  return (
    <div className="flex items-center justify-center w-full h-full bg-white pb-4">
      <img
        src={`public/images/${file_id}_wordcloud.jpg`} // Use dynamic image path
        alt="Word Cloud"
        className="max-w-full max-h-full object-contain"
      />
    </div>
  );
};

export default WordCloud;

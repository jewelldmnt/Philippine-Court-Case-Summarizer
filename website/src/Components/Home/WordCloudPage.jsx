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

const WordCloud = ({ stats }) => {
  /**
   * WordCloud component that renders a pre-generated word cloud image
   * based on the type of word (unigram or bigram).
   *
   * @param {Object} stats - Array of word frequency statistics.
   *   - stats: An array of objects where each object contains:
   *     - `rank`: The rank of the word (unique identifier).
   *     - `unigram`: The unigram (single word) in the word cloud.
   *     - `bigram`: The bigram (two words) in the word cloud.
   *     - `frequency`: The frequency of the unigram or bigram.
   *
   * @returns {JSX.Element} A div element that contains the word cloud image,
   *              or a message if the image cannot be loaded.
   */
  const getImagePath = (word) => {
    if (word.unigram) {
      return "public/images/uni_wordcloud.jpg"; // Image for unigram
    } else if (word.bigram) {
      return "public/images/bi_wordcloud.jpg"; // Image for bigram
    }
    return null;
  };

  if (!stats || stats.length === 0) {
    return <p>No word cloud data available.</p>;
  }

  const imagePath = getImagePath(stats[0]); // Selects the image based on the first word's type (unigram or bigram)

  return (
    <div className="flex items-center justify-center w-full h-full bg-white pb-4">
      {imagePath ? (
        <img
          src={imagePath} // Use dynamic image path
          alt="Word Cloud"
          className="max-w-full max-h-full object-contain"
        />
      ) : (
        <p>No valid word cloud image found.</p>
      )}
    </div>
  );
};

export default WordCloud;

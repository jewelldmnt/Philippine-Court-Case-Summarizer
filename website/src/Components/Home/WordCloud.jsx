/**
 * Program Title: Court Case Summarizer - WordCloud Component
 *
 * Programmer: Nicholas Dela Torre
 * Date Written: October 12, 2024
 * Date Revised: October 12, 2024
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
   * WordCloud component that renders a dynamic word cloud based on provided 
   * statistics. It calculates font sizes for words based on their frequency and 
   * positions them randomly within a container.
   *
   * @param {Object} stats - Array of word frequency statistics.
   *   - stats: An array of objects where each object contains:
   *     - `rank`: The rank of the word (unique identifier).
   *     - `unigram`: The unigram (single word) in the word cloud.
   *     - `bigram`: The bigram (two words) in the word cloud.
   *     - `frequency`: The frequency of the unigram or bigram.
   *
   * @returns {JSX.Element} A div element that contains the generated word cloud, 
   *              or a message if no data is available.
   */
  const getFontSize = (frequency) => {
    /**
     * Calculates the font size for a given word based on its frequency.
     * The font size is proportionally scaled between a minimum and maximum frequency.
     *
     * @param {number} frequency - The frequency of the word.
     *
     * @returns {string} The font size for the word in pixels (e.g., '24px').
     */
    const maxFrequency = Math.max(...stats.map((stat) => stat.frequency));
    const minFrequency = Math.min(...stats.map((stat) => stat.frequency));

    // Handle case where all frequencies are the same
    if (maxFrequency === minFrequency) {
      return "20px"; // Default font size when there's no frequency range
    }

    const fontSize =
      12 + ((frequency - minFrequency) / (maxFrequency - minFrequency)) * 40;
    return `${fontSize}px`;
  };

  if (!stats || stats.length === 0) {
    return <p>No word cloud data available.</p>;
  }

  return (
    <div
      className="relative w-full h-full overflow-hidden"
      // Adjust height for the container
      style={{ position: "relative", maxWidth: "100%", maxHeight: "100%" }}
    >
      {stats.map((stat) => (
        <div
          key={stat.rank}
          className="absolute font-sans font-bold"
          style={{
            fontSize: getFontSize(stat.frequency),
            // Keeps word within 10%-90% height of container
            top: `${Math.random() * 80 + 10}%`,
            // Keeps word within 10%-90% width of container
            left: `${Math.random() * 80 + 10}%`,
            transform: "translate(-50%, -50%)",
            whiteSpace: "nowrap",
            pointerEvents: "none", // Prevents interaction interference
          }}
        >
          {stat.unigram ? stat.unigram : stat.bigram}
        </div>
      ))}
    </div>
  );
};

export default WordCloud;

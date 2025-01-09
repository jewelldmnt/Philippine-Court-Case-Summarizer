/**
 * Program Title: Court Case Summarizer - Statistics Component
 *
 * Programmers: Nicholas Dela Torre, Jino Llamado
 * Date Written: October 12, 2024
 * Date Revised: October 12, 2024
 *
 * Purpose:
 *    This component is part of the Court Case Summarizer project and is designed
 *    to analyze and display word statistics and frequency visualizations (unigrams
 *    and bigrams) for selected court case files. It enables users to understand
 *    key terms and phrase patterns within each case file.
 *
 * Where the Program Fits in the General System Design:
 *    The Statistics component is part of the frontend user interface, connecting
 *    to a backend API to retrieve court case files. It computes word and bigram
 *    frequencies, displaying them as tables and word clouds. This component supports
 *    the Summarizer's goal of enhancing readability and comprehension of lengthy
 *    legal documents.
 *
 * Dependencies and Resources:
 *    - React: Functional component structure for rendering and managing state.
 *    - Axios: For HTTP requests to fetch court case data from the backend API.
 *    - WordCloud (Custom Component): For visualizing word and bigram frequency
 *      as word clouds.
 *    - CSS (WordCloud Styling): Custom styles are imported from
 *      "assets/wordcloud.css" for word cloud visuals.
 *    - Tailwind CSS classes: Used extensively for styling the layout and components.
 *
 * Control Flow and Logic:
 *    1. `calculateWordFrequencies`: Processes court case text, removes stopwords,
 *       and calculates unigram frequencies.
 *    2. `calculateBigramFrequencies`: Processes text to generate and calculate
 *       bigram frequencies.
 *    3. `handleFileClick`: Sets the active file and computes unigram and bigram
 *       statistics for the selected file.
 *    4. `useEffect`: Fetches the list of available files from the backend API
 *       when the component mounts.
 *
 * Key Variables:
 *    - `existingFiles`: Stores the list of court case files retrieved from the
 *      backend.
 *    - `activeFile`: Tracks the currently selected court case file.
 *    - `courtCaseValue`: Holds the text of the active court case for analysis.
 *    - `wordStatsList`: Contains the top 10 unigrams based on frequency for the
 *      active file.
 *    - `bigramStatsList`: Contains the top 10 bigrams based on frequency for the
 *      active file.
 *    - `stopwords`: An array of common words to exclude from frequency calculations
 *      to enhance relevance.
 */

import NavBar from "../Navigation/NavBar";
import WordCloudPage from "./WordCloudPage";
import { useEffect, useState } from "react";
import axios from "axios";
import "../../assets/wordcloud.css";

const Statistics = () => {
  /**
   * Description:
   * A functional React component that displays statistics about court case summaries.
   * It includes a list of court cases, their unigram and bigram word frequency
   * statistics, and word clouds for both unigrams and bigrams. The component
   * fetches available court case files from the server and, when a file is clicked,
   * it displays detailed statistics about the file's text (unigrams, bigrams).
   *
   * Parameters:
   * None
   *
   * Returns:
   * {JSX.Element} - The rendered UI for the statistics page, including:
   *   - A list of court case files.
   *   - Tables showing unigram and bigram frequency statistics.
   *   - Word clouds for both unigrams and bigrams.
   */

  const [existingFiles, setExistingFiles] = useState([]);
  const [activeFile, setActiveFile] = useState(null);
  const [courtCaseValue, setCourtCaseValue] = useState("");
  const [wordStatsList, setWordStatsList] = useState([]);
  const [bigramStatsList, setBigramStatsList] = useState([]);

  const stopwords = [
    "the",
    "and",
    "a",
    "is",
    "in",
    "it",
    "of",
    "to",
    "that",
    "this",
    "with",
    "for",
    "on",
    "at",
    "by",
    "an",
    "as",
    "be",
    "are",
    "from",
    "or",
    "was",
    "which",
    "but",
    "if",
    "not",
    "all",
    "can",
    "has",
    "had",
    "have",
    "he",
    "her",
    "his",
    "i",
    "me",
    "my",
    "you",
    "we",
    "they",
    "their",
    "our",
    "us",
    "will",
    "would",
    "there",
    "what",
    "so",
    "when",
    "where",
    "who",
    "why",
    "how",
    "up",
    "down",
    "out",
    "about",
    "into",
    "over",
    "then",
    "than",
    "too",
    "also",
    "only",
    "just",
    "even",
    "did",
    "does",
    "do",
    "no",
    "yes",
    "more",
    "now",
    "very",
    "here",
    "some",
    "such",
    "could",
    "should",
    "must",
    "being",
    "were",
    "before",
    "after",
    "through",
    "between",
    "under",
    "again",
    "both",
    "any",
    "each",
    "because",
    "during",
    "once",
    "few",
    "many",
    "most",
    "other",
    "these",
    "those",
  ];

  const calculateWordFrequencies = (text) => {
    /**
     * Description:
     * Calculates the frequency of unigrams (single words) in a given text,
     * excluding stopwords, and returns the top 10 most frequent words.
     *
     * Parameter:
     * @param {string} text - The input text to calculate word frequencies.
     *
     * Returns:
     * {Array} - An array of objects representing the top 10 unigrams, each containing:
     *   - `rank` (number): The rank of the word.
     *   - `frequency` (number): The frequency of the word.
     *   - `unigram` (string): The word itself.
     */

    const words = text
      .toLowerCase()
      .replace(/[^\w\s]/g, "")
      .split(/\s+/)
      .filter((word) => !stopwords.includes(word)); // Remove stopwords

    const frequencyMap = words.reduce((map, word) => {
      map[word] = (map[word] || 0) + 1;
      return map;
    }, {});

    const sortedWords = Object.entries(frequencyMap).sort(
      (a, b) => b[1] - a[1]
    );

    return sortedWords.map(([word, frequency], index) => ({
      frequency,
      unigram: word,
    }));
  };

  const calculateBigramFrequencies = (text) => {
    /**
     * Description:
     * Calculates the frequency of bigrams (pairs of consecutive words) in a
     * given text, excluding stopwords, and returns the top 10 most frequent bigrams.
     *
     * Parameter:
     * @param {string} text - The input text to calculate bigram frequencies.
     *
     * Returns:
     * {Array} - An array of objects representing the top 10 bigrams, each containing:
     *   - `rank` (number): The rank of the bigram.
     *   - `frequency` (number): The frequency of the bigram.
     *   - `bigram` (string): The bigram itself.
     */

    const words = text
      .toLowerCase()
      .replace(/[^\w\s]/g, "")
      .split(/\s+/)
      .filter((word) => !stopwords.includes(word)); // Remove stopwords

    const bigrams = [];
    for (let i = 0; i < words.length - 1; i++) {
      bigrams.push(`${words[i]} ${words[i + 1]}`);
    }

    const frequencyMap = bigrams.reduce((map, bigram) => {
      map[bigram] = (map[bigram] || 0) + 1;
      return map;
    }, {});

    const sortedBigrams = Object.entries(frequencyMap).sort(
      (a, b) => b[1] - a[1]
    );

    return sortedBigrams.map(([bigram, frequency], index) => ({
      frequency,
      bigram,
    }));
  };

  const handleFileClick = (file) => {
    /**
     * Description:
     * Handles the click event for a file from the list of court cases. Sets the
     * active file, displays its text, and calculates the word and bigram frequencies.
     *
     * Parameter:
     * @param {Object} file - The selected file object containing the file's details.
     *
     * Returns:
     * {void} - No return value, but updates the state with word and bigram statistics.
     */

    setActiveFile(file);
    setCourtCaseValue(file.file_text);

    const wordStats = calculateWordFrequencies(file.file_text);
    console.log("Word Stats: ", wordStats);
    setWordStatsList(wordStats);

    const bigramStats = calculateBigramFrequencies(file.file_text);
    console.log("Bigram Stats: ", bigramStats);
    setBigramStatsList(bigramStats);
  };

  useEffect(() => {
    /**
     * Description:
     * Fetches the list of available files from the server when the component is
     * mounted and sets the state with the list of files.
     *
     * Parameter:
     * None
     *
     * Returns:
     * {void} - No return value, updates the component's state with the list of
     *          files.
     */

    axios
      .get("http://127.0.0.1:5000/get-files")
      .then((res) => {
        setExistingFiles(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <>
      <div className="bg-customGray text-black h-screen">
        <NavBar activePage="Statistics" />
        <div className="grid grid-cols-[1fr,2fr,2fr] gap-x-10 h-fit m-8">
          <div>
            <p className="font-bold font-sans text-[15px] ml-4 mb-4">
              LIST OF COURT CASES
            </p>
            <div
              className="font-sans text-sm bg-customRbox rounded-xl py-6 
            h-[450px] overflow-y-auto custom-scrollbar"
            >
              <ol className="list-decimal list-inside">
                {existingFiles.length > 0 ? (
                  existingFiles.map((file, index) => (
                    <li
                      key={index}
                      className={`hover:bg-wordCount w-full px-4 
                        cursor-pointer mb-2 ${
                          activeFile?.id === file.id ? "bg-active" : ""
                        }`}
                      onClick={() => handleFileClick(file)}
                    >
                      {file.file_name.length > 35
                        ? `${file.file_name.slice(0, 35)}...`
                        : file.file_name}
                    </li>
                  ))
                ) : (
                  <p className="ml-4">No files uploaded yet.</p>
                )}
              </ol>
            </div>
          </div>

          <div className="grid grid-rows-[auto,1fr,1fr] gap-y-4">
            <p className="font-bold font-sans text-[15px] ml-4 flex items-center">
              STATISTICS OF THE ORIGINAL COURT CASE
            </p>

            {/* Unigram Statistics Table */}
            <div
              className="bg-customRbox rounded-xl py-6 w-full h-full 
            max-h-[240px] overflow-y-auto custom-scrollbar"
            >
              <table className="table-fixed w-full">
                <thead>
                  <tr>
                    <th className="font-bold font-sans">Frequency</th>
                    <th className="font-bold font-sans">Unigram</th>
                  </tr>
                </thead>
                <tbody>
                  {wordStatsList.length > 0 ? (
                    wordStatsList.map((stat) => (
                      <tr key={stat.rank}>
                        <td className="text-sm text-center font-sans">
                          {stat.frequency}
                        </td>
                        <td className="text-sm text-center font-sans">
                          {stat.unigram}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="3" className="text-sm text-center font-sans">
                        No data available
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Bigram Statistics Table */}
            <div
              className="bg-customRbox rounded-xl py-6 pb-10 h-full 
            max-h-[240px] w-full overflow-y-auto custom-scrollbar"
            >
              <table className="table-fixed w-full">
                <thead>
                  <tr>
                    <th className="font-bold font-sans">Frequency</th>
                    <th className="font-bold font-sans">Bigram</th>
                  </tr>
                </thead>
                <tbody>
                  {bigramStatsList.length > 0 ? (
                    bigramStatsList.map((stat) => (
                      <tr key={stat.rank}>
                        <td className="text-sm text-center font-sans">
                          {stat.frequency}
                        </td>
                        <td className="text-sm text-center font-sans">
                          {stat.bigram}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="3" className="text-sm text-center font-sans">
                        No data available
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className="flex flex-col space-y-6">
            <p className="font-bold font-sans text-[15px] ml-4 flex items-center">
              STATISTICS OF THE ORIGINAL COURT CASE
            </p>
            {/* Unigram Word Cloud */}
            <div
              className="bg-customRbox rounded-xl py-6 w-full h-full 
            max-h-[300px] p-4 wordcloud-container"
            >
              <p className="font-bold text-[15px] ml-4 mb-2">
                Unigram Word Cloud
              </p>
              <div className="relative w-full h-full flex justify-center">
                <WordCloudPage stats={wordStatsList} />
              </div>
            </div>

            {/* Bigram Word Cloud */}
            <div
              className="bg-customRbox rounded-xl py-6 w-full h-full 
            max-h-[300px] p-4 wordcloud-container"
            >
              <p className="font-bold text-[15px] ml-4 mb-2">
                Bigram Word Cloud
              </p>
              <div className="relative w-full h-full flex justify-center">
                <WordCloudPage stats={bigramStatsList} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Statistics;

/**
 * Program Title: Court Case Summarizer - Statistics Component
 *
 * Programmers: Nicholas Dela Torre, Jino Llamado, Jewell Anne Diamante
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
import { useEffect, useState, useContext } from "react";
import axios from "axios";
import "../../assets/wordcloud.css";
import { unigramStopwords, bigramStopwords } from "../Constants/stopwords";
import { ThemeContext } from "../../ThemeContext";

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
  const [loading, setLoading] = useState(false);
  const { isDarkMode } = useContext(ThemeContext);

  const handleFileClick = (file) => {
    /**
     * Description:
     * Handles the selection of a file, processes its content to calculate unigrams and bigrams,
     * and updates the component's state with the computed statistics.
     *
     * Parameter:
     * {object} file - The selected file object containing `file_text` and `id` properties.
     *
     * Returns:
     * {void} - No return value, updates the component's state with unigrams and bigrams.
     */
    setActiveFile(file);
    setCourtCaseValue(file.file_text);
    console.log("Selected File ID: ", file.id);

    // Preprocess the text
    const text = file.file_text.toLowerCase().replace(/[^a-z\s]/g, "");

    // Tokenize the text into words
    const words = text.split(/\s+/);

    // Calculate unigrams (filtering out unigram stopwords and short words)
    const filteredUnigrams = words.filter(
      (word) => !unigramStopwords.includes(word) && word.length > 3
    );
    const unigrams = calculateUnigrams(filteredUnigrams);

    // Calculate bigrams (filtering out bigram stopwords)
    const filteredBigrams = [];
    for (let i = 0; i < filteredUnigrams.length - 1; i++) {
      const bigram = `${filteredUnigrams[i]} ${filteredUnigrams[i + 1]}`;
      if (!bigramStopwords.includes(bigram)) {
        filteredBigrams.push(bigram);
      }
    }
    const bigrams = calculateBigrams(filteredBigrams);

    // Update state with the results
    setWordStatsList(unigrams);
    setBigramStatsList(bigrams);
  };

  // Function to calculate unigrams
  const calculateUnigrams = (words) => {
    /**
     * Description:
     * Computes the frequency of each unigram (word) from the input array of words
     * and returns the top 10 unigrams sorted by frequency in descending order.
     *
     * Parameter:
     * {string[]} words - An array of words filtered for unigrams.
     *
     * Returns:
     * {object[]} - An array of objects where each object contains a `unigram` (string) and its `frequency` (number).
     */
    const freqMap = {};
    words.forEach((word) => {
      freqMap[word] = (freqMap[word] || 0) + 1;
    });
    const unigrams = Object.entries(freqMap).map(([unigram, frequency]) => ({
      unigram,
      frequency,
    }));
    return unigrams.sort((a, b) => b.frequency - a.frequency).slice(0, 10);
  };

  // Function to calculate bigrams
  const calculateBigrams = (bigrams) => {
    /**
     * Description:
     * Computes the frequency of each bigram (two-word phrase) from the input array
     * of bigrams and returns the top 10 bigrams sorted by frequency in descending order.
     *
     * Parameter:
     * {string[]} bigrams - An array of bigram strings.
     *
     * Returns:
     * {object[]} - An array of objects where each object contains a `bigram` (string) and its `frequency` (number).
     */
    const freqMap = {};
    bigrams.forEach((bigram) => {
      freqMap[bigram] = (freqMap[bigram] || 0) + 1;
    });
    const bigramStats = Object.entries(freqMap).map(([bigram, frequency]) => ({
      bigram,
      frequency,
    }));
    return bigramStats.sort((a, b) => b.frequency - a.frequency).slice(0, 10);
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
    <div
      className={`h-screen ${
        isDarkMode ? "bg-darkPrimary text-white" : "bg-customGray text-black"
      }`}
    >
      <NavBar activePage="Statistics" />
      <div className="grid grid-cols-[1fr,2fr,2fr] gap-x-10 h-[80vh] m-8">
        <div className="h-[80vh] overflow-y-auto">
          <p className="font-bold font-sans text-[15px] ml-4 mb-4">
            LIST OF COURT CASES
          </p>
          <div
            className={`font-sans text-sm rounded-xl py-0 h-[73vh] overflow-y-auto custom-scrollbar ${
              isDarkMode
                ? "bg-darkSecondary text-white"
                : "bg-customRbox text-black"
            }`}
          >
            <ol className="list-none">
              {existingFiles.length > 0 ? (
                existingFiles.map((file, index) => (
                  <li
                    key={index}
                    className={`w-full px-4 py-2 cursor-${
                      loading ? "not-allowed" : "pointer"
                    } flex items-center border-b-[0.3px] ${
                      activeFile?.id === file.id
                        ? isDarkMode
                          ? "bg-darkTertiary text-white border-b-gray-600" // Active file in dark mode
                          : "bg-customHoverC text-black border-b-gray-300" // Active file in light mode
                        : isDarkMode
                        ? "bg-darkSecondary text-white hover:bg-darkTertiary border-b-gray-600" // Default dark mode styles
                        : "bg-white text-black hover:bg-customHoverC border-b-gray-300" // Default light mode styles
                    }`}
                    onClick={!loading ? () => handleFileClick(file) : null}
                  >
                    <div className="flex items-center">
                      <span title={file.file_name || "Untitled"}>
                        {index + 1}.{" "}
                        {file.file_name && file.file_name.length > 20
                          ? `${file.file_name.slice(0, 20)}...`
                          : file.file_name || "Untitled"}
                      </span>
                    </div>
                  </li>
                ))
              ) : (
                <p className="ml-4 text-gray-600">No files uploaded yet.</p>
              )}
            </ol>
          </div>
        </div>

        <div className="grid grid-rows-[auto,1fr] gap-y-4">
          <p className="font-bold font-sans text-[15px] ml-4 flex items-center">
            STATISTICS OF THE ORIGINAL COURT CASE
          </p>

          <div className="flex flex-col justify-between h-[73vh]">
            {/* Unigram Statistics Table */}
            <div
              className={`rounded-xl py-6 pb-10 w-full h-[35vh] overflow-y-auto custom-scrollbar ${
                isDarkMode
                  ? "bg-darkSecondary text-white"
                  : "bg-customRbox text-black"
              }`}
              style={{ overflow: wordStatsList.length < 1 ? "hidden" : "" }}
            >
              <table className="table-fixed w-full">
                <thead>
                  <tr>
                    <th className="font-bold font-sans text-lg  px-4 py-1">
                      Frequency
                    </th>
                    <th className="font-bold font-sans text-lg  px-4 py-1">
                      Unigram
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan="2" className="h-[140px]">
                        <div className="flex items-center justify-center h-full">
                          <p>Loading...</p>
                        </div>
                      </td>
                    </tr>
                  ) : wordStatsList.length > 0 ? (
                    wordStatsList.map((stat) => (
                      <tr key={stat.rank}>
                        <td className="text-m text-center font-sans px-4 ">
                          {stat.frequency}
                        </td>
                        <td className="text-m text-center font-sans px-4 ">
                          {stat.unigram}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="2" className="h-[140px]">
                        <div className="flex items-center justify-center h-full">
                          <p>No File Selected</p>
                        </div>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Bigram Statistics Table */}
            <div
              className={`rounded-xl py-6 pb-10 w-full h-[35vh] overflow-y-auto custom-scrollbar ${
                isDarkMode
                  ? "bg-darkSecondary text-white"
                  : "bg-customRbox text-black"
              }`}
              style={{
                paddingBottom: "2.5rem",
                fontSize: "1rem",
                fontFamily: "'Roboto', sans-serif",
                whiteSpace: "pre-line", // Keeps \n formatting
                lineHeight: "1.5rem", // Increases line height for multiline
                overflow: wordStatsList.length < 1 ? "hidden" : "",
              }}
            >
              <table className="table-fixed w-full">
                <thead>
                  <tr>
                    <th className="font-bold font-sans text-lg  px-4 py-1">
                      Frequency
                    </th>
                    <th className="font-bold font-sans text-lg  px-4 py-1">
                      Bigram
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan="2" className="h-[140px]">
                        <div className="flex items-center justify-center h-full">
                          <p>Loading...</p>
                        </div>
                      </td>
                    </tr>
                  ) : bigramStatsList.length > 0 ? (
                    bigramStatsList.map((stat) => (
                      <tr key={stat.rank}>
                        <td className="text-m text-center font-sans px-4">
                          {stat.frequency}
                        </td>
                        <td className="text-m text-center font-sans px-4">
                          {stat.bigram}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="2" className="h-[140px]">
                        <div className="flex items-center justify-center h-full">
                          <p>No File Selected</p>
                        </div>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div className="flex flex-col h-[80vh] overflow-y-auto">
          <p className="font-bold font-sans text-[15px] ml-4 mb-4 flex items-center">
            WORD CLOUD OF THE ORIGINAL COURT CASE
          </p>
          {/* Word Cloud */}
          <div
            className={`rounded-xl w-full h-[73vh] overflow-y-auto ${
              isDarkMode
                ? "bg-darkSecondary text-white"
                : "bg-customRbox text-black"
            }`}
          >
            {loading ? (
              <div className="flex items-center justify-center h-full">
                <p>Loading...</p>
              </div>
            ) : activeFile && activeFile.id ? (
              <WordCloudPage file_id={activeFile.id} />
            ) : (
              <div className="flex items-center justify-center h-full">
                No File selected
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Statistics;

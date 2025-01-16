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
import { unigramStopwords, bigramStopwords } from "../Constants/stopwords";

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

  const calculateWordFrequencies = async (text, id) => {
    try {
      const preprocess_res = await axios.post(
        `http://127.0.0.1:5000/get-preprocess/${id}`,
        {},
        { headers: { "Content-Type": "application/json" } }
      );

      const words = preprocess_res.data.preprocess
        .toLowerCase()
        .replace(/[^\w\s]/g, "") // Remove punctuation
        .replace(/[a-zA-Z]+\d+[a-zA-Z]*|\d+[a-zA-Z]+/g, "") // Remove mixed sequences of letters and numbers
        .split(/\s+/) // Split into words
        .filter((word) => !unigramStopwords.includes(word)) // Remove stopwords
        .filter((word) => word.length > 2); // Remove short words (length <= 2)

      const frequencyMap = words.reduce((map, word) => {
        map[word] = (map[word] || 0) + 1;
        return map;
      }, {});

      const filteredWords = Object.entries(frequencyMap).filter(
        ([word, freq]) => freq > 2
      );

      const sortedWords = filteredWords.sort((a, b) => b[1] - a[1]);

      return sortedWords.map(([word, frequency], index) => ({
        rank: index + 1,
        frequency,
        unigram: word,
      }));
    } catch (error) {
      console.error("Error fetching or processing data:", error);
      return [];
    }
  };

  const calculateBigramFrequencies = async (text, id) => {
    try {
      const preprocess_res = await axios.post(
        `http://127.0.0.1:5000/get-preprocess/${id}`,
        {},
        { headers: { "Content-Type": "application/json" } }
      );

      const words = preprocess_res.data.preprocess
        .toLowerCase()
        .replace(/[^\w\s]/g, "")
        .replace(/[a-zA-Z]+\d+[a-zA-Z]*|\d+[a-zA-Z]+/g, "")
        .split(/\s+/)
        .filter((word) => !bigramStopwords.includes(word));

      const bigrams = [];
      for (let i = 0; i < words.length - 1; i++) {
        bigrams.push(`${words[i]} ${words[i + 1]}`);
      }

      const frequencyMap = bigrams.reduce((map, bigram) => {
        map[bigram] = (map[bigram] || 0) + 1;
        return map;
      }, {});

      const sortedBigrams = Object.entries(frequencyMap)
        .filter(([_, frequency]) => frequency > 1) // Include only bigrams with frequency > 1
        .sort((a, b) => b[1] - a[1]);

      return sortedBigrams.map(([bigram, frequency], index) => ({
        frequency,
        bigram,
      }));
    } catch (error) {
      console.error("Error fetching or processing data:", error);
      return [];
    }
  };

  const handleFileClick = async (file) => {
    setLoading(true);
    setActiveFile(file);
    setCourtCaseValue(file.file_text);

    try {
      const wordStats = await calculateWordFrequencies(file.file_text, file.id);
      setWordStatsList(wordStats);

      const bigramStats = await calculateBigramFrequencies(
        file.file_text,
        file.id
      );
      setBigramStatsList(bigramStats);

      // After everything is loaded, set loading to false
    } catch (error) {
      console.error("Error handling file click:", error);
    } finally {
      setLoading(false);
    }
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
    <div className="bg-customGray text-black h-screen">
      <NavBar activePage="Statistics" />
      <div className="grid grid-cols-[1fr,2fr,2fr] gap-x-10 h-[80vh] m-8">
        <div className="h-[80vh] overflow-y-auto">
          <p className="font-bold font-sans text-[15px] ml-4 mb-4">
            LIST OF COURT CASES
          </p>
          <div
            className="font-sans text-sm bg-customRbox rounded-xl py-6
            h-[73vh] overflow-y-auto"
          >
            <ol className="list-decimal list-inside">
              {existingFiles.length > 0 ? (
                existingFiles.map((file, index) => (
                  <li
                    key={index}
                    className={`hover:bg-customHoverC w-full px-4 cursor-${
                      loading ? "not-allowed" : "pointer"
                    } mb-2 ${
                      activeFile?.id === file.id ? "bg-customHoverC" : ""
                    }`}
                    onClick={!loading ? () => handleFileClick(file) : null}
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
          <div className="bg-customRbox rounded-xl py-6 w-full h-[35vh]  overflow-y-auto custom-scrollbar">
            <table className="table-fixed w-full">
              <thead>
                <tr>
                  <th className="font-bold font-sans">Frequency</th>
                  <th className="font-bold font-sans">Unigram</th>
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
          <div className="bg-customRbox rounded-xl py-6 pb-10 w-full h-[35vh] overflow-y-auto custom-scrollbar">
            <table className="table-fixed w-full">
              <thead>
                <tr>
                  <th className="font-bold font-sans">Frequency</th>
                  <th className="font-bold font-sans">Bigram</th>
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

        <div className="flex flex-col space-y-6 h-[80vh] overflow-y-auto">
          <p className="font-bold font-sans text-[15px] ml-4 flex items-center">
            WORD CLOUD OF THE ORIGINAL COURT CASE
          </p>
          {/* Word Cloud */}
          <div className="bg-customRbox rounded-xl w-full h-[72vh]  overflow-y-auto">
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

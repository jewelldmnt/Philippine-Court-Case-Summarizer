import NavBar from "../Navigation/NavBar";
import WordCloud from "./WordCloud";
import { useEffect, useState } from "react";
import axios from "axios";
import "../../assets/wordcloud.css";

const Statistics = () => {
  const [existingFiles, setExistingFiles] = useState([]);
  const [activeFile, setActiveFile] = useState(null);
  const [courtCaseValue, setCourtCaseValue] = useState("");
  const [wordStatsList, setWordStatsList] = useState([]); // Store top 10 word frequency and rank objects
  const [bigramStatsList, setBigramStatsList] = useState([]); // Store top 10 bigram frequency and rank objects

  const calculateWordFrequencies = (text) => {
    const words = text
      .toLowerCase()
      .replace(/[^\w\s]/g, "")
      .split(/\s+/); // Remove punctuation and split text into words

    const frequencyMap = words.reduce((map, word) => {
      map[word] = (map[word] || 0) + 1;
      return map;
    }, {});

    // Convert the frequency map to an array and sort by frequency in descending order
    const sortedWords = Object.entries(frequencyMap).sort(
      (a, b) => b[1] - a[1]
    );

    // Get only the top 10 words
    const top10Words = sortedWords.slice(0, 10);

    // Map sorted words to a list of dictionaries with rank, frequency, and unigram
    return top10Words.map(([word, frequency], index) => ({
      rank: index + 1,
      frequency,
      unigram: word,
    }));
  };

  const calculateBigramFrequencies = (text) => {
    const words = text
      .toLowerCase()
      .replace(/[^\w\s]/g, "")
      .split(/\s+/); // Remove punctuation and split text into words

    const bigrams = [];
    for (let i = 0; i < words.length - 1; i++) {
      bigrams.push(`${words[i]} ${words[i + 1]}`);
    }

    const frequencyMap = bigrams.reduce((map, bigram) => {
      map[bigram] = (map[bigram] || 0) + 1;
      return map;
    }, {});

    // Convert the frequency map to an array and sort by frequency in descending order
    const sortedBigrams = Object.entries(frequencyMap).sort(
      (a, b) => b[1] - a[1]
    );

    // Get only the top 10 bigrams
    const top10Bigrams = sortedBigrams.slice(0, 10);

    // Map sorted bigrams to a list of dictionaries with rank, frequency, and bigram
    return top10Bigrams.map(([bigram, frequency], index) => ({
      rank: index + 1,
      frequency,
      bigram,
    }));
  };

  const handleFileClick = (file) => {
    setActiveFile(file);
    setCourtCaseValue(file.file_text);

    const wordStats = calculateWordFrequencies(file.file_text);
    console.log("Word Stats: ", wordStats); // Debug log
    setWordStatsList(wordStats);

    const bigramStats = calculateBigramFrequencies(file.file_text);
    console.log("Bigram Stats: ", bigramStats); // Debug log
    setBigramStatsList(bigramStats);
  };

  useEffect(() => {
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
      <div className="bg-background text-white h-screen">
        <NavBar activePage="Statistics" />
        <div className="grid grid-cols-[1fr,2fr,2fr] gap-x-10 h-fit m-8">
          <div>
            <p className="font-bold font-sans text-[15px] ml-4 mb-4">
              LIST OF COURT CASES
            </p>
            <div className="font-sans text-sm bg-box rounded-xl py-6 h-[450px] overflow-y-auto custom-scrollbar">
              <ol className="list-decimal list-inside">
                {existingFiles.length > 0 ? (
                  existingFiles.map((file, index) => (
                    <li
                      key={index}
                      className={`hover:bg-wordCount w-full px-4 cursor-pointer mb-2 ${
                        activeFile?.id === file.id ? "bg-active" : ""
                      }`}
                      onClick={() => handleFileClick(file)}
                    >
                      {file.file_name}
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
              STATISTICS OF THE PRODUCED SUMMARY
            </p>

            {/* Unigram Statistics Table */}
            <div className="bg-box rounded-xl py-6 w-full h-full max-h-[240px] overflow-y-auto custom-scrollbar">
              <table className="table-fixed w-full">
                <thead>
                  <tr>
                    <th className="font-bold font-sans">Rank</th>
                    <th className="font-bold font-sans">Frequency</th>
                    <th className="font-bold font-sans">Unigram</th>
                  </tr>
                </thead>
                <tbody>
                  {wordStatsList.length > 0 ? (
                    wordStatsList.map((stat) => (
                      <tr key={stat.rank}>
                        <td className="text-sm text-center font-sans">
                          {stat.rank}
                        </td>
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
            <div className="bg-box rounded-xl py-6 pb-10 h-full max-h-[240px] w-full overflow-y-auto custom-scrollbar">
              <table className="table-fixed w-full">
                <thead>
                  <tr>
                    <th className="font-bold font-sans">Rank</th>
                    <th className="font-bold font-sans">Frequency</th>
                    <th className="font-bold font-sans">Bigram</th>
                  </tr>
                </thead>
                <tbody>
                  {bigramStatsList.length > 0 ? (
                    bigramStatsList.map((stat) => (
                      <tr key={stat.rank}>
                        <td className="text-sm text-center font-sans">
                          {stat.rank}
                        </td>
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

          {/* WordClouds Section */}
          {/* WordClouds Section */}
          <div className="flex flex-col space-y-6">
            <div className="bg-box rounded-xl py-6 w-full h-full max-h-[300px] p-4 wordcloud-container">
              <p className="font-bold text-[15px] ml-4 mb-2">
                Unigram Word Cloud
              </p>
              <div className="flex justify-center">
                <WordCloud stats={wordStatsList} />
              </div>
            </div>
            <div className="bg-box rounded-xl py-6 w-full h-full max-h-[300px] p-4 wordcloud-container">
              <p className="font-bold text-[15px] ml-4 mb-2">
                Bigram Word Cloud
              </p>
              <div className="flex justify-center">
                <WordCloud stats={bigramStatsList} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Statistics;

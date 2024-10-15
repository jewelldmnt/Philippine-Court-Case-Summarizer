import NavBar from "../Navigation/NavBar";
import Delete from "../Modals/Delete";
import Cancel from "../Modals/Cancel";
import { PiArrowLineDownBold } from "react-icons/pi";
import { FaTrash } from "react-icons/fa6";
import { ImCloudDownload } from "react-icons/im";
import { useState, useEffect } from "react";
import axios from "axios";
import { BiSolidEditAlt } from "react-icons/bi";
import { FaCirclePlus, FaCircleMinus } from "react-icons/fa6";
import { HiMiniLockOpen, HiMiniLockClosed } from "react-icons/hi2";
import AddCaseModal from "../Modals/AddCaseFile";
import "../../assets/spinner.css";
import CircularProgress from "@mui/material/CircularProgress";

const Summarizer = () => {
  const [editCase, setEditCase] = useState(false);
  const [courtCaseValue, setCourtCaseValue] = useState("");
  const [deleteCase, setDeleteCase] = useState(false);
  const [cancelEdit, setCancelEdit] = useState(false);
  const [activeFile, setActiveFile] = useState("");
  const [existingFiles, setExistingFiles] = useState([]);
  const [summarizedCase, setSummarizedCase] = useState("No Summary yet");
  const [courtCaseLink, setCourtCaseLink] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [loadingText, setLoadingText] = useState("");
  const [progress, setProgress] = useState(0); // Track the progress percentage
  const [isFadingOut, setIsFadingOut] = useState(false);

  const [input, setInput] = useState({
    text: "no case is selected yet",
  });

  // useEffect(() => {
  //   const incrementProgress = async (start, end, duration) => {
  //     const step = (end - start) / (duration / 50); // Calculate the step size
  //     let currentProgress = start;

  //     return new Promise((resolve) => {
  //       const intervalId = setInterval(() => {
  //         currentProgress += step;

  //         // Only update progress if the value is greater
  //         setProgress((prevProgress) => {
  //           if (currentProgress > prevProgress) {
  //             return currentProgress;
  //           }
  //           return prevProgress;
  //         });

  //         if (currentProgress >= end) {
  //           clearInterval(intervalId);
  //           resolve();
  //         }
  //       }, 50); // Update every 50ms for smooth animation
  //     });
  //   };

  //   const runProgressUpdate = async () => {
  //     await incrementProgress(0, 25, 10000);
  //     await incrementProgress(26, 50, 50000);
  //     await incrementProgress(51, 80, 100000);
  //     await incrementProgress(81, 100, 10000);
  //   };

  //   runProgressUpdate(); // Call the async function inside useEffect
  // }, [loading]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/get-files")
      .then((res) => {
        console.log("file text: ", res.data);
        setExistingFiles(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [activeFile]);

  useEffect(() => {
    if (cancelEdit && activeFile) {
      setCourtCaseValue(activeFile.file_text);
    }
  }, [cancelEdit, activeFile]);

  useEffect(() => {
    const tasks = ["Pre-processing..", "Segmenting..", "Summarizing.."];
    let taskIndex = 0;

    // Set initial loading text
    setLoadingText(tasks[taskIndex]);

    // Track fading state
    let fadeOutTimeout;

    const updateText = () => {
      // After the fade-out completes, show the new text
      fadeOutTimeout = setTimeout(() => {
        taskIndex = (taskIndex + 1) % tasks.length; // Increment index and loop back to 0 if it exceeds array length
        setLoadingText(tasks[taskIndex]);
      }, 1000); // 1 second for fade-out duration
    };

    // Set an interval to update loading text every 5 seconds
    const intervalId = setInterval(() => {
      setIsFadingOut(true); // Start fading out
      updateText();
      setIsFadingOut(false); // Reset fade state
    }, 5000); // 5 seconds

    // Clean up interval and timeout when component unmounts or when the effect is re-executed
    return () => {
      clearInterval(intervalId);
      clearTimeout(fadeOutTimeout);
    };
  }, [loading]);

  const handleFileClick = (file) => {
    setActiveFile(file);
    setCourtCaseValue(file.file_text);
  };

  const handleCancelEdit = () => {
    setCancelEdit(false);
    setEditCase(false);
    setCourtCaseValue(activeFile.file_text);
  };

  const handleSaveEdit = async () => {
    const newFile = {
      file_name: activeFile.file_name,
      file_text: courtCaseValue,
      file_content: activeFile.file_content,
    };

    await axios
      .patch(`http://127.0.0.1:5000/update-file/${activeFile.id}`, newFile)
      .then((res) => {
        console.log(res.data);

        setExistingFiles((prev) =>
          prev.map((file) =>
            file.id === activeFile.id
              ? { ...file, file_text: courtCaseValue }
              : file
          )
        );
      })
      .catch((err) => {
        console.log(err);
      });

    setCancelEdit(false);
    setEditCase(false);
  };

  const handleFileAdd = async () => {
    console.log(courtCaseLink);
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/send-file", {
        link: courtCaseLink,
      });

      console.log("response: ", response.data);

      if (Array.isArray(response.data)) {
        setExistingFiles((prev) => [...prev, ...response.data]);
      } else if (response.data && typeof response.data === "object") {
        setExistingFiles((prev) => [...prev, response.data]);
      } else {
        console.error("Unexpected response format:", response.data);
      }

      const updatedFiles = await axios.get("http://127.0.0.1:5000/get-files");
      setExistingFiles(updatedFiles.data);
    } catch (error) {
      console.error("Error adding file:", error);
    } finally {
      setLoading(false);
      setIsModalOpen(false);
    }

    setCourtCaseLink("");
  };

  const handleFileDelete = async () => {
    if (!activeFile) return;

    await axios
      .delete(`http://127.0.0.1:5000/delete-file/${activeFile.id}`)
      .then((res) => {
        console.log("response: ", res);
        setExistingFiles((prevFiles) =>
          prevFiles.filter((file) => file.id !== activeFile.id)
        );
        setActiveFile(null);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const handleTextDownload = () => {
    if (activeFile) {
      const blob = new Blob([summarizedCase], {
        type: "text/plain",
      });
      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = `${activeFile.file_name}.txt`;
      a.style.display = "none";
      document.body.appendChild(a);
      a.click();
      a.remove();

      URL.revokeObjectURL(url);
    } else {
      console.error("No active file to download.");
    }
  };

  const handleSummarizedCase = async () => {
    setLoading(true);
    setProgress(0); // Reset progress at the beginning of the process

    // Function to slowly increment progress over time

    try {
      const preprocess_res = await axios.post(
        `http://127.0.0.1:5000/get-preprocessed/${activeFile.id}`,
        {},
        { headers: { "Content-Type": "application/json" } }
      );

      const segmented_res = await axios.post(
        `http://127.0.0.1:5000/get-segmented`,
        { cleaned_text: preprocess_res.data.cleaned_text },
        { headers: { "Content-Type": "application/json" } }
      );

      const summarized_res = await axios.post(
        `http://127.0.0.1:5000/get-summarized/${activeFile.id}`,
        { segmented_case: segmented_res.data.segmented_case },
        { headers: { "Content-Type": "application/json" } }
      );

      setSummarizedCase(summarized_res.data.summary);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Delete
        open={deleteCase}
        del={() => setDeleteCase(false)}
        cancel={() => setDeleteCase(false)}
      />
      <Cancel
        open={cancelEdit}
        edit={() => setCancelEdit(false)}
        cancel={handleCancelEdit}
      />

      <AddCaseModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        courtCaseLink={courtCaseLink}
        setCourtCaseLink={setCourtCaseLink}
        handleFileAdd={handleFileAdd}
        loading={loading}
      />

      <div className="bg-background text-white h-screen">
        <NavBar activePage="Summarizer" />
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
            <div className="mt-4 flex justify-between px-2">
              <label
                className="flex items-center cursor-pointer"
                onClick={() => setIsModalOpen(true)}
              >
                <FaCirclePlus className="size-6 text-icon-10" />
                <p className="font-bold font-sans text-[14px] ml-2">Add Case</p>
              </label>
              <button onClick={handleFileDelete} className="flex items-center">
                <FaCircleMinus className="size-6 text-icon-20" />
                <p className="font-bold font-sans text-[14px] ml-2 ">
                  Delete Case
                </p>
              </button>
            </div>
          </div>

          <div>
            <p className="font-bold font-sans text-[15px] ml-4 mb-4 flex items-center">
              ORIGINAL COURT CASE
              {editCase ? (
                <>
                  <HiMiniLockOpen className="ml-2 size-6 text-primary" />
                </>
              ) : (
                <>
                  <HiMiniLockClosed className="ml-2 size-6 text-primary" />
                </>
              )}
            </p>
            <div className="relative">
              <textarea
                className="bg-box rounded-xl px-4 py-6 pb-10 h-[450px] w-full overflow-y-auto custom-scrollbar"
                value={courtCaseValue}
                onChange={(e) => setCourtCaseValue(e.target.value)}
                readOnly={!editCase}
                style={{ paddingBottom: "2.5rem" }}
              />
              <div className="gap-2 flex items-center font-sans font-bold text-xs absolute left-0 right-0 bottom-0 h-10 bg-wordCount rounded-bl-xl rounded-br-xl p-4 z-10">
                <p>Word Count:</p>
                <p className="text-active">
                  {courtCaseValue.split(/\s+/).filter(Boolean).length}
                </p>
                <label
                  className="flex items-center cursor-pointer h-6 bg-summarize justify-center rounded-xl shadow-xl"
                  onClick={() => {
                    handleSummarizedCase();
                  }}
                >
                  <p className="font-bold font-sans text-xs m-2">Summarize</p>
                  <input type="button" className="hidden" />
                </label>
              </div>
            </div>
            {editCase ? (
              <div className="mt-4 flex justify-between px-2">
                <button className="flex items-center" onClick={handleSaveEdit}>
                  <PiArrowLineDownBold className="size-6 text-icon-10" />
                  <p className="font-bold font-sans text-[14px] ml-2">
                    Save Case
                  </p>
                </button>
                <button
                  className="flex items-center"
                  onClick={() => setCancelEdit(true)}
                >
                  <FaTrash className="size-6 text-icon-20" />
                  <p className="font-bold font-sans text-[14px] ml-2">
                    Cancel Edit
                  </p>
                </button>
              </div>
            ) : (
              <div className="mt-4 flex justify-center px-2">
                <button
                  className="flex items-center"
                  onClick={() => setEditCase(true)}
                >
                  <BiSolidEditAlt className="text-icon-10 size-6" />
                  <p className="font-bold font-sans text-[14px] ml-2">
                    Edit Case
                  </p>
                </button>
              </div>
            )}
          </div>

          <div>
            <p className="font-bold font-sans text-[15px] ml-4 mb-4">
              SUMMARIZED COURT CASE
            </p>
            <div className="relative">
              {loading ? (
                <div className="bg-box rounded-xl px-4 py-6 pb-10 h-[450px] w-full overflow-y-auto custom-scrollbar flex flex-col justify-center items-center">
                  <p
                    className={`loading-text fade-text ${
                      isFadingOut ? "hidden" : ""
                    }`}
                  >
                    {loadingText}
                  </p>
                  <div className="spinner"></div>
                </div>
              ) : (
                <textarea
                  className="bg-box rounded-xl px-4 py-6 pb-10 h-[450px] w-full overflow-y-auto custom-scrollbar"
                  readOnly
                  value={summarizedCase}
                  style={{ paddingBottom: "2.5rem" }}
                />
              )}

              <div className="gap-2 flex items-center font-sans font-bold text-xs absolute left-0 right-0 bottom-0 h-10 bg-wordCount rounded-bl-xl rounded-br-xl p-4 z-10">
                <p>Word Count:</p>
                <p className="text-active">
                  {loading
                    ? ""
                    : summarizedCase.split(/\s+/).filter(Boolean).length}
                </p>
              </div>
            </div>

            <div className="mt-4 flex justify-center px-2">
              <button
                className="flex items-center"
                onClick={handleTextDownload}
              >
                <ImCloudDownload className="text-icon-30 size-6" />
                <p className="font-bold font-sans text-[14px] ml-2">
                  Download Summarized Case as txt
                </p>
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Summarizer;

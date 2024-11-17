/**
 * Program Title: Court Case Summarizer - Summarizer Component
 *
 * Programmer: Nicholas Dela Torre, Jino Llamado
 * Date Written: October 12, 2024
 * Date Revised: October 12, 2024
 *
 * Purpose:
 *    This component is part of the Court Case Summarizer project. It provides a
 *    user interface for uploading court case documents, allowing users to select
 *    files, validate formats, and initiate uploads for backend analysis.
 *
 * Where the Program Fits in the General System Design:
 *    The Summarizer component is a key entry point for data in the frontend.
 *    It connects to the backend API to send and store files for processing,
 *    enabling new court case files to enter the system for summarization.
 *
 * Dependencies and Resources:
 *    - React: Functional component for handling user inputs and managing state.
 *    - Axios: For sending HTTP requests to upload files to the backend.
 *    - Tailwind CSS classes: Used extensively for layout and responsive styling.
 *
 * Control Flow and Logic:
 *    1. `handleFileChange`: Validates the selected file format and updates state.
 *    2. `handleUpload`: Sends the selected file to the backend API for storage.
 *    3. `useEffect`: Logs the success or failure of the upload, handling errors.
 *
 * Key Variables:
 *    - `selectedFile`: Tracks the currently chosen file to be uploaded.
 *    - `uploadStatus`: Stores the current upload status ('pending', 'success', etc.).
 *    - `allowedFormats`: Array of acceptable file formats (e.g., .pdf, .docx).
 */

import NavBar from "../Navigation/NavBar";
import Delete from "../Modals/Delete";
import Cancel from "../Modals/Cancel";
import ConfirmDelete from "../Modals/ConfirmDelete";
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
  const [progress, setProgress] = useState(0);
  const [isFadingOut, setIsFadingOut] = useState(false);
  const [loadingModal, setLoadingModal] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);

  const [input, setInput] = useState({
    text: "no case is selected yet",
  });

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
    const tasks = ["Pre-processing..", "Segmenting..", "Summarizing.."];
    let taskIndex = 0;

    // Set initial loading text
    setLoadingText(tasks[taskIndex]);

    // Track fading state
    let fadeOutTimeout;

    const updateText = () => {
      // After the fade-out completes, show the new text
      fadeOutTimeout = setTimeout(() => {
        // Increment index and loop back to 0 if it exceeds array length
        taskIndex = (taskIndex + 1) % tasks.length;
        setLoadingText(tasks[taskIndex]);
      }, 1000);
    };

    // Set an interval to update loading text every 5 seconds
    const intervalId = setInterval(() => {
      setIsFadingOut(true); // Start fading out
      updateText();
      setIsFadingOut(false); // Reset fade state
    }, 5000); // 5 seconds

    // Clean up interval and timeout when component unmounts
    return () => {
      clearInterval(intervalId);
      clearTimeout(fadeOutTimeout);
    };
  }, [loading]);

  const handleFileClick = (file) => {
    /**
     * Handles the click event for selecting a file. Sets the active file and updates the court case text.
     *
     * @param {Object} file - The selected file object containing file details.
     *   - file: Object representing the file containing file name, file content, and file text.
     *
     * @returns {void}
     */
    setActiveFile(file);
    setCourtCaseValue(file.file_text);
  };

  const handleSaveEdit = async () => {
    /**
     * Saves the edited case by sending a PATCH request to the backend to update the file.
     * Updates the local state to reflect the changes made to the case.
     *
     * @returns {void}
     */
    const newFile = {
      file_name: activeFile.file_name,
      file_text: courtCaseValue,
      file_content: activeFile.file_content,
    };

    try {
      // Update the file on the backend
      await axios.patch(
        `http://127.0.0.1:5000/update-file/${activeFile.id}`,
        newFile
      );

      // Update the existing files in the state
      setExistingFiles((prev) =>
        prev.map((file) =>
          file.id === activeFile.id
            ? { ...file, file_text: courtCaseValue }
            : file
        )
      );
      setEditCase(false); // Exit edit mode after saving
      setCancelEdit(false); // Reset cancel state
    } catch (err) {
      console.error(err);
    }
  };

  const handleCancelEdit = () => {
    /**
     * Cancels the editing of a case. Resets the editing state and restores the original case text.
     *
     * @returns {void}
     */
    setCancelEdit(false);
    setEditCase(false); // Exit edit mode
    setCourtCaseValue(activeFile.file_text); // Reset the text area to its original state
  };

  const handleFileAdd = async () => {
    /**
     * Handles the adding of a new case file by sending a POST request with the file link.
     * If successful, updates the list of existing files and closes the modal.
     *
     * @returns {void}
     */
    console.log(courtCaseLink);
    setLoadingModal(true);
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
      setLoadingModal(false);
      setIsModalOpen(false);
    }

    setCourtCaseLink("");
  };

  const handleFileDelete = async () => {
    /**
     * Handles the deletion of a selected case file. Sends a DELETE request to the backend and updates the state.
     *
     * @returns {void}
     */
    if (!activeFile) return;

    try {
      await axios.delete(`http://127.0.0.1:5000/delete-file/${activeFile.id}`);
      setExistingFiles((prevFiles) =>
        prevFiles.filter((file) => file.id !== activeFile.id)
      );
      setActiveFile(null);
    } catch (err) {
      console.error(err);
    }
  };

  const handleTextDownload = () => {
    /**
     * Initiates the download of the summarized case as a `.txt` file.
     * Creates a downloadable blob with the summarized case text.
     *
     * @returns {void}
     */
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
    /**
     * Summarizes the case by performing a series of steps: pre-processing, segmenting, and summarizing.
     * Updates the summarized case text in the state after the process is complete.
     *
     * @returns {void}
     */
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
        { segmented_paragraph: preprocess_res.data.segmented_paragraph },
        { headers: { "Content-Type": "application/json" } }
      );

      const summarized_res = await axios.post(
        `http://127.0.0.1:5000/get-summarized/${activeFile.id}`,
        { segmentation_output: segmented_res.data.segmentation_output },
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
        loading={loadingModal}
      />

      <ConfirmDelete
        isOpen={showConfirmation}
        onClose={() => setShowConfirmation(false)}
        onConfirm={handleFileDelete}
      />

      <div className="bg-customGray text-black h-screen">
        <NavBar activePage="Summarizer" />
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
                      className={`hover:bg-customHoverC w-full px-4 cursor-pointer mb-2 ${
                        activeFile?.id === file.id ? "bg-customHoverC" : ""
                      }`}
                      onClick={() => handleFileClick(file)}
                    >
                      {file.file_name && file.file_name.length > 35
                        ? `${file.file_name.slice(0, 35)}...`
                        : file.file_name || "Untitled"}
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
                <FaCirclePlus className="size-6 text-icon-40" />
                <p className="font-bold font-sans text-[14px] ml-2">Add Case</p>
              </label>
              <button
                onClick={() => setShowConfirmation(true)}
                className="flex items-center"
              >
                <FaCircleMinus className="size-6 text-icon-20" />
                <p className="font-bold font-sans text-[14px] ml-2">
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
                  <HiMiniLockOpen className="ml-2 size-6 text-customLock" />
                </>
              ) : (
                <>
                  <HiMiniLockClosed className="ml-2 size-6 text-customLock" />
                </>
              )}
            </p>
            <div className="relative">
              <textarea
                className="bg-customRbox rounded-xl px-4 py-6 pb-10 h-[450px] 
                w-full overflow-y-auto custom-scrollbar"
                value={courtCaseValue ? courtCaseValue : "No case selected"}
                onChange={(e) => setCourtCaseValue(e.target.value)}
                readOnly={!editCase}
                style={{ paddingBottom: "2.5rem" }}
              />
              <div
                className="gap-2 flex items-center font-sans font-bold text-xs 
              absolute left-0 right-0 bottom-0 h-10 bg-wordCount rounded-bl-xl 
              rounded-br-xl p-4 z-10"
              >
                <p className="text-white">Word Count:</p>
                <p className="text-customWC">
                  {courtCaseValue.split(/\s+/).filter(Boolean).length}
                </p>
                <label
                  className="flex items-center cursor-pointer h-8 bg-summarize 
                  justify-center rounded-xl shadow-xl"
                  onClick={() => {
                    handleSummarizedCase();
                  }}
                >
                  <p className="font-bold font-sans text-xs m-3">Summarize</p>
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
                <div
                  className="bg-customRbox rounded-xl px-4 py-6 pb-10 h-[450px] 
                w-full overflow-y-auto custom-scrollbar flex flex-col justify-center items-center"
                >
                  <p
                    className={`loading-text fade-text ${
                      isFadingOut ? "hidden" : ""
                    }`}
                    style={{ color: "black" }}
                  >
                    {loadingText}
                  </p>
                  <div className="spinner"></div>
                </div>
              ) : (
                <textarea
                  className="bg-customRbox rounded-xl px-4 py-6 pb-10 h-[450px] 
                  w-full overflow-y-auto custom-scrollbar"
                  readOnly
                  value={summarizedCase}
                  style={{ paddingBottom: "2.5rem" }}
                />
              )}

              <div
                className="gap-2 flex items-center font-sans font-bold text-xs 
              absolute left-0 right-0 bottom-0 h-10 bg-wordCount rounded-bl-xl 
              rounded-br-xl p-4 z-10"
              >
                <p className="text-white">Word Count:</p>
                <p className="text-customWC">
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
                <p className="font-bold font-sans text-[14px] ml-2">Download</p>
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Summarizer;

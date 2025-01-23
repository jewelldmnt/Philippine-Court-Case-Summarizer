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
import { useState, useEffect, useContext } from "react";
import axios from "axios";
import { BiSolidEditAlt } from "react-icons/bi";
import { FaCirclePlus, FaCircleMinus } from "react-icons/fa6";
import { HiMiniLockOpen, HiMiniLockClosed } from "react-icons/hi2";
import AddCaseModal from "../Modals/AddCaseFile";
import "../../assets/spinner.css";
import CircularProgress from "@mui/material/CircularProgress";
import SavingModal from "../Modals/SavingModal";
import { ThemeContext } from "../../ThemeContext";
import ConfirmSave from "../Modals/ConfirmSave";

const Summarizer = () => {
  const [editCase, setEditCase] = useState(false);
  const [courtCaseValue, setCourtCaseValue] = useState("");
  const [deleteCase, setDeleteCase] = useState(false);
  const [cancelEdit, setCancelEdit] = useState(false);
  const [isSaveModalOpen, setIsSaveModalOpen] = useState(false);
  const [activeFile, setActiveFile] = useState("");
  const [existingFiles, setExistingFiles] = useState([]);
  const [summarizedCase, setSummarizedCase] = useState("No Summary yet");
  const [courtCaseLink, setCourtCaseLink] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loadingText, setLoadingText] = useState("");
  const [progress, setProgress] = useState(0);
  const [isFadingOut, setIsFadingOut] = useState(false);
  const [loadingModal, setLoadingModal] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [isSummaryLoading, setIsSummaryLoading] = useState(false); // for summary loading state
  const [isEditLoading, setIsEditLoading] = useState(false); // for edit case loading state
  const [showAddedPopup, setShowAddedPopup] = useState(false);
  const [showDeletePopup, setShowDeletePopup] = useState(false);
  const [revertPopup, setRevertPopup] = useState(false);
  const [summaryPopup, setSummaryPopup] = useState(false);
  const [hasSummaryPopup, setHasSummaryPopup] = useState(false);
  const { isDarkMode } = useContext(ThemeContext);

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
  }, [isSummaryLoading]);

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

    // Check if any of the summary-related properties exist and show
    if (file.file_facts || file.file_issues || file.file_rulings) {
      setSummarizedCase({
        title: file.file_name,
        facts: file.file_facts || "No facts available",
        issues: file.file_issues || "No issues available",
        rulings: file.file_rulings || "No rulings available",
      });
    } else {
      setSummarizedCase("No Summary yet");
    }
  };

  const handleSaveEdit = async () => {
    /**
     * Saves the edited case by sending a PATCH request to the backend to update the file.
     * Updates the local state to reflect the changes made to the case.
     *
     * @returns {void}
     */
    setIsEditLoading(true);
    const newFile = {
      ...activeFile,
      file_text: courtCaseValue,
      file_summary: 0,
    };

    try {
      // Update the file on the backend
      await axios.patch(
        `http://127.0.0.1:5000/update-file/${activeFile.id}`,
        newFile
      );

      // Update the existing files in the state
      setActiveFile(newFile); // Update the active file state
      setExistingFiles((prev) =>
        prev.map((file) => (file.id === activeFile.id ? newFile : file))
      );
      setEditCase(false); // Exit edit mode after saving
      setCancelEdit(false); // Reset cancel state
    } catch (err) {
      console.error(err);
    } finally {
      setIsEditLoading(false);
    }
  };

  const handleRevertCase = async () => {
    /**
     * Saves the edited case by sending a PATCH request to the backend to update the file.
     * Updates the local state to reflect the changes made to the case.
     *
     * @returns {void}
     */
    setIsEditLoading(true);
    const newFile = {
      ...activeFile,
      file_text: activeFile.file_orig_text,
      file_summary: 0,
    };

    try {
      // Update the file on the backend
      await axios.patch(
        `http://127.0.0.1:5000/update-file/${activeFile.id}`,
        newFile
      );

      setActiveFile(newFile);
      setCourtCaseValue(activeFile.file_orig_text);

      // Update the existing files in the state
      setExistingFiles((prev) =>
        prev.map((file) =>
          file.id === activeFile.id
            ? { ...file, file_text: courtCaseValue }
            : file
        )
      );
      console.log("summ:", activeFile.file_summary);
      setEditCase(false); // Exit edit mode after saving
      setCancelEdit(false); // Reset cancel state
    } catch (err) {
      console.error(err);
    } finally {
      setIsEditLoading(false);
      setRevertPopup(true); // Show the popup
      setTimeout(() => setRevertPopup(false), 3000);
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

  const handleSave = () => {
    // Logic to save the case (e.g., making an API call to update the database)
    console.log("Changes saved:", caseData);
  };

  const handleFileAdd = async (event, resetFileName) => {
    const file = event.target.files[0];

    const reader = new FileReader();
    reader.onload = async (e) => {
      const fileContent = e.target.result;
      const fileTitle = file.name;

      setLoadingModal(true);

      try {
        await axios.post("http://127.0.0.1:5000/send-file", {
          content: fileContent,
          title: fileTitle,
          link: courtCaseLink, // Include link in request payload
        });

        if (resetFileName) resetFileName();
        setCourtCaseLink(""); // Reset link input after submission
        setIsModalOpen(false); // Close modal

        const updatedFiles = await axios.get("http://127.0.0.1:5000/get-files");
        setExistingFiles(updatedFiles.data);

        setShowAddedPopup(true); // Show the popup
        setTimeout(() => setShowAddedPopup(false), 3000); // Hide popup after 3 seconds
      } catch (err) {
        console.error("Error uploading file:", err);
      } finally {
        setLoadingModal(false);
      }
    };
    reader.readAsText(file);
  };

  const handleFileLink = async (event, courtCaseLink, resetFileName) => {
    /**
     * Handles the file upload along with a provided link from a text box in the modal.
     *
     * @param {Object} event - The event triggered by the file input change.
     * @param {string} courtCaseLink - The user-provided link from the text box.
     * @param {Function} resetFileName - Function to reset the file input field after submission.
     *
     * @returns {void}
     */

    setLoadingModal(true); // Indicate loading state

    try {
      // Send the file and link to the backend
      await axios.post("http://127.0.0.1:5000/send-file-link", {
        link: courtCaseLink.trim(), // Include the trimmed user-provided link
      });

      if (resetFileName) resetFileName(); // Clear the file input
      setIsModalOpen(false); // Close the modal

      // Refresh the list of files after upload
      const updatedFiles = await axios.get("http://127.0.0.1:5000/get-files");
      setExistingFiles(updatedFiles.data);

      setShowAddedPopup(true); // Show the popup
      setTimeout(() => setShowAddedPopup(false), 3000);
    } catch (err) {
      console.error("Error uploading file with link:", err);
    } finally {
      setLoadingModal(false); // End loading state
    }
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
      setCourtCaseValue(""); // Clear the displayed court case text

      setShowDeletePopup(true);
      setTimeout(() => setShowDeletePopup(false), 3000);
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
    if (activeFile.file_summary === 1) {
      setHasSummaryPopup(true); // Show the popup
      setTimeout(() => setHasSummaryPopup(false), 3000); // Hide popup after 3 seconds
      return;
    }
    setIsSummaryLoading(true);
    console.log("has summary", activeFile.file_summary);
    setProgress(0); // Reset progress at the beginning of the process

    // Function to slowly increment progress over time

    try {
      const summarize_res = await axios.post(
        `http://127.0.0.1:5000/get-summarized/${activeFile.id}`,
        {},
        { headers: { "Content-Type": "application/json" } }
      );

      const summarizedFile = {
        ...activeFile,
        file_summary: 1,
        file_facts: summarize_res.data.facts,
        file_issues: summarize_res.data.issues,
        file_rulings: summarize_res.data.rulings,
      };

      console.log("summarize", summarize_res.data);

      setActiveFile(summarizedFile);
      setSummarizedCase(summarize_res.data);

      setExistingFiles((prev) =>
        prev.map((file) =>
          file.id === activeFile.id
            ? { ...file, file_text: courtCaseValue }
            : file
        )
      );
    } catch (err) {
      console.error(err);
    } finally {
      setIsSummaryLoading(false);
      setSummaryPopup(true); // Show the popup
      setTimeout(() => setSummaryPopup(false), 3000);
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
        handleFileLink={handleFileLink}
        loading={loadingModal}
      />

      <ConfirmDelete
        isOpen={showConfirmation}
        onClose={() => setShowConfirmation(false)}
        onConfirm={handleFileDelete}
      />

      <ConfirmSave
        isOpen={isSaveModalOpen}
        onClose={() => setIsSaveModalOpen(false)}
        onSave={handleSaveEdit}
      />

      <SavingModal open={isEditLoading} text="Saving changes, please wait..." />

      {showAddedPopup && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-green-500 text-white font-bold py-2 px-4 rounded shadow-lg z-50">
          Case has been added successfully!
        </div>
      )}

      {showDeletePopup && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-red-500 text-white font-bold py-2 px-4 rounded shadow-lg z-50">
          File has been deleted!
        </div>
      )}

      {summaryPopup && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-green-500 text-white font-bold py-2 px-4 rounded shadow-lg z-50">
          Summary Created!
        </div>
      )}

      {revertPopup && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-green-500 text-white font-bold py-2 px-4 rounded shadow-lg z-50">
          Reverted to original case!
        </div>
      )}

      {hasSummaryPopup && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-blue-500 text-white font-bold py-2 px-4 rounded shadow-lg z-50">
          Case already has summary!
        </div>
      )}

      <div
        className={`${
          isDarkMode ? "bg-darkPrimary text-white" : "bg-customGray text-black"
        } h-screen`}
      >
        {" "}
        <NavBar activePage="Summarizer" />
        <div className="grid grid-cols-[1fr,2fr,2fr] gap-x-10 h-[80vh] m-8">
          <div className="h-[80vh]">
            <p className="font-bold font-sans text-[15px] ml-4 mb-4">
              LIST OF COURT CASES
            </p>
            <div
              className={`${
                isDarkMode ? "bg-darkSecondary" : "bg-customRbox"
              } font-sans text-sm rounded-xl py-0 h-[73vh] overflow-y-auto custom-scrollbar`}
              style={{
                height: "calc(100vh - 200px)",
                overflow: existingFiles.length < 1 ? "hidden" : "",
              }}
            >
              <ol className="list-none">
                {existingFiles.length > 0 ? (
                  existingFiles.map((file, index) => (
                    <li
                      key={index}
                      className={`w-full px-4 py-2 cursor-${
                        isSummaryLoading || editCase ? "not-allowed" : "pointer"
                      } ${
                        activeFile?.id === file.id
                          ? `${
                              isDarkMode ? "bg-darkTertiary" : "bg-customHoverC"
                            }` // Active file background in dark or light mode
                          : ""
                      } flex items-center border-b-[0.3px] ${
                        isDarkMode ? "border-gray-600" : "border-gray-300" // No border in dark mode
                      } ${
                        isDarkMode
                          ? "hover:bg-darkTertiary" // Dark mode hover effect
                          : "hover:bg-customHoverC" // Light mode hover effect
                      }`}
                      onClick={
                        !isSummaryLoading && !editCase
                          ? () => handleFileClick(file)
                          : null
                      }
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
                  <div className="flex items-center justify-center h-[30rem]">
                    <p className="text-gray-600">No files uploaded yet.</p>
                  </div>
                )}
              </ol>
            </div>
            <div className="mt-4 flex justify-between px-2">
              <button
                className={`flex items-center px-3 py-2 rounded-md ${
                  isSummaryLoading
                    ? "opacity-50 cursor-not-allowed"
                    : "hover:shadow-md hover:shadow-black/50 transition-shadow duration-300"
                }`}
                disabled={isSummaryLoading}
                onClick={() => setIsModalOpen(true)}
              >
                <FaCirclePlus className="size-6 text-icon-40" />
                <p className="font-bold font-sans text-[14px] ml-2">Add Case</p>
              </button>
              <button
                onClick={() => setShowConfirmation(true)}
                className={`flex items-center px-3 py-2 rounded-md ${
                  !activeFile || isSummaryLoading || editCase
                    ? "opacity-50 cursor-not-allowed"
                    : "hover:shadow-md hover:shadow-black/50 transition-shadow duration-300"
                }`}
                disabled={!activeFile || isSummaryLoading || editCase}
              >
                <FaCircleMinus className="size-6 text-icon-20" />
                <p className="font-bold font-sans text-[14px] ml-2">
                  Delete Case
                </p>
              </button>
            </div>
          </div>

          <div className="w-full h-[73vh]">
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
            <div className="relative" style={{ height: "calc(100vh - 200px)" }}>
              <textarea
                className={`bg-customRbox rounded-xl px-4 py-6 h-[450px] w-full overflow-y-auto custom-scrollbar flex items-center justify-center ${
                  isDarkMode
                    ? "bg-darkSecondary text-gray-300"
                    : "bg-customRbox text-black"
                } ${courtCaseValue ? "" : "text-center"}`}
                value={courtCaseValue ? courtCaseValue : ""}
                onChange={(e) => setCourtCaseValue(e.target.value)}
                readOnly={!editCase}
                style={{
                  paddingBottom: "2.5rem",
                  fontSize: "1rem",
                  fontFamily: "'Roboto', sans-serif",
                  whiteSpace: "pre-line", // Keeps \n formatting
                  lineHeight: "1.5rem", // Increases line height for multiline
                  height: "calc(100vh - 200px)",
                }}
              />
              {!courtCaseValue && (
                <p
                  className={`absolute inset-0 flex items-center justify-center pointer-events-none ${
                    isDarkMode ? "text-gray-300" : "text-black"
                  }`}
                  style={{
                    fontSize: "1rem",
                    fontFamily: "'Roboto', sans-serif",
                    lineHeight: "1.5rem", // Increases line height for multiline
                    height: "calc(100vh - 200px)",
                  }}
                >
                  No court case is selected yet
                </p>
              )}

              <div
                className={`gap-2 flex items-center font-sans font-bold text-xs absolute left-0 right-0 bottom-0 h-10 p-4 z-10 ${
                  isDarkMode
                    ? "bg-darkTertiary text-white rounded-bl-xl rounded-br-xl"
                    : "bg-wordCount text-black rounded-bl-xl rounded-br-xl"
                }`}
              >
                <p className="text-white">Word Count:</p>
                <p className="text-customWC">
                  {courtCaseValue.split(/\s+/).filter(Boolean).length}
                </p>
                <button
                  className={`btn flex items-center h-8 justify-center shadow-xl ${
                    isDarkMode
                      ? "bg-darkSummarize text-white"
                      : "bg-summarize text-black"
                  } ${
                    !activeFile || isSummaryLoading || editCase
                      ? "opacity-50 cursor-not-allowed"
                      : "hover:shadow-md hover:shadow-black/50 transition-shadow duration-300"
                  }`}
                  onClick={() => {
                    handleSummarizedCase();
                  }}
                  disabled={!activeFile || isSummaryLoading || editCase}
                >
                  <p className="font-bold font-sans text-xs m-3">Summarize</p>
                  <input type="button" className="hidden " />
                </button>
                <button
                  className={`btn flex items-center h-8 justify-center shadow-xl ${
                    isDarkMode
                      ? "bg-darkSummarize text-white"
                      : "bg-summarize text-black"
                  } ${
                    !activeFile || isSummaryLoading || editCase
                      ? "opacity-50 cursor-not-allowed"
                      : "hover:shadow-md hover:shadow-black/50 transition-shadow duration-300"
                  }`}
                  onClick={() => {
                    handleRevertCase();
                  }}
                  disabled={!activeFile || isSummaryLoading || editCase}
                >
                  <p className="font-bold font-sans text-xs m-3">
                    Revert to original
                  </p>
                  <input type="button" className="hidden " />
                </button>
              </div>
            </div>
            {editCase ? (
              <div className="mt-4 flex justify-between px-2">
                <button
                  className={`flex items-center px-3 py-2 rounded-md ${
                    isEditLoading || !activeFile || isSummaryLoading
                      ? "opacity-50 cursor-not-allowed"
                      : "hover:shadow-md hover:shadow-black/50 transition-shadow duration-300"
                  }`}
                  onClick={() => setIsSaveModalOpen(true)}
                  disabled={isEditLoading || !activeFile || isSummaryLoading}
                >
                  <PiArrowLineDownBold className="size-6 text-icon-10" />
                  <p className="font-bold font-sans text-[14px] ml-2">
                    Save Case
                  </p>
                </button>
                <button
                  className={`flex items-center px-3 py-2 rounded-md ${
                    isEditLoading || !activeFile || isSummaryLoading
                      ? "opacity-50 cursor-not-allowed"
                      : "hover:shadow-md hover:shadow-black/50 transition-shadow duration-300"
                  }`}
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
                  onClick={() => setEditCase(true)}
                  disabled={!activeFile || isSummaryLoading} // Disable the button while summarizing
                  className={`flex items-center px-3 py-2 rounded-md ${
                    !activeFile || isSummaryLoading
                      ? "opacity-50 cursor-not-allowed"
                      : "hover:shadow-md hover:shadow-black/50 transition-shadow duration-300"
                  }`}
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
            <div
              className="relative h-[73vh]"
              style={{ height: "calc(100vh - 200px)" }}
            >
              {isSummaryLoading ? (
                <div
                  className={`rounded-xl px-4 py-6 pb-10 h-[73vh] w-full overflow-y-auto custom-scrollbar flex flex-col justify-center items-center ${
                    isDarkMode
                      ? "bg-darkSecondary text-white"
                      : "bg-customRbox text-black"
                  }`}
                  style={{ height: "calc(100vh - 200px)" }}
                >
                  <p
                    className={`loading-text fade-text ${
                      isFadingOut ? "hidden" : ""
                    } ${
                      isDarkMode
                        ? "bg-darkSecondary text-white"
                        : "bg-customRbox text-black"
                    }`}
                  >
                    {loadingText}
                  </p>
                  <div className="spinner"></div>
                </div>
              ) : (
                <div
                  className={`${
                    isDarkMode
                      ? "bg-darkSecondary text-gray-300"
                      : "bg-customRbox text-black"
                  } rounded-xl px-4 py-6 pb-10 h-[73vh] w-full overflow-y-auto custom-scrollbar flex ${
                    summarizedCase === "No Summary yet"
                      ? "justify-center items-center text-center"
                      : "flex-col justify-start items-start"
                  }`}
                  style={{
                    paddingBottom: "2.5rem",
                    fontSize: "1rem", // Slightly larger font for readability
                    fontFamily: "'Roboto', sans-serif", // Readable sans-serif font
                    whiteSpace: "pre-line", // Keeps \n formatting
                    lineHeight: "1.5rem",
                    overflowY: "auto", // Enables scrolling on the outer div
                    boxSizing: "border-box", // Includes padding in height calculations
                    height: "calc(100vh - 200px)",
                  }}
                >
                  <div
                    className="whitespace-pre-wrap w-full"
                    style={{
                      maxWidth: "100%", // Prevents content from exceeding container width
                      wordWrap: "break-word", // Ensures long words or links break properly
                      textAlign:
                        summarizedCase === "No Summary yet"
                          ? "center"
                          : "justify", // Justifies text for a clean look
                    }}
                  >
                    {summarizedCase.title ? (
                      <div>
                        <div className="mb-12">
                          <p className="font-semibold">TITLE:</p>
                          <p>{summarizedCase["title"]}</p>
                        </div>
                        <div className="mb-12">
                          <p className="font-semibold">FACTS:</p>
                          <p>{summarizedCase["facts"]}</p>
                        </div>
                        <div className="mb-12">
                          <p className="font-semibold">ISSUES:</p>
                          <p>{summarizedCase["issues"]}</p>
                        </div>
                        <div className="mb-12">
                          <p className="font-semibold">RULINGS:</p>
                          <p>{summarizedCase["rulings"]}</p>
                        </div>
                      </div>
                    ) : (
                      "No Summary Yet"
                    )}
                  </div>
                </div>
              )}

              <div
                className={`gap-2 flex items-center font-sans font-bold text-xs absolute left-0 right-0 bottom-0 h-10 rounded-bl-xl rounded-br-xl p-4 z-10 ${
                  isDarkMode
                    ? "bg-darkTertiary text-white"
                    : "bg-wordCount text-black"
                }`}
              >
                <p className="text-white">Word Count:</p>
                <p className="text-customWC">
                  {!isSummaryLoading &&
                  (summarizedCase?.facts ||
                    summarizedCase?.issues ||
                    summarizedCase?.ruling)
                    ? summarizedCase["facts"].split(/\s+/).filter(Boolean)
                        .length +
                      summarizedCase["issues"].split(/\s+/).filter(Boolean)
                        .length +
                      summarizedCase["rulings"].split(/\s+/).filter(Boolean)
                        .length
                    : ""}
                </p>
              </div>
            </div>

            <div className="mt-4 flex justify-center px-2">
              <button
                className={`flex items-center px-3 py-2 rounded-md ${
                  summarizedCase === "No Summary yet" || isSummaryLoading
                    ? "opacity-50 cursor-not-allowed"
                    : "hover:shadow-md hover:shadow-black/50 transition-shadow duration-300"
                }`}
                disabled={
                  summarizedCase === "No Summary yet" || isSummaryLoading
                }
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

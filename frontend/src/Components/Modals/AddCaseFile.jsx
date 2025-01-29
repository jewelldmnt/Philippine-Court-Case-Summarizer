/**
 * Program Title: Court Case Summarizer - Add Case Modal Component
 *
 * Programmer: Nicholas dela Torre
 * Date Written: January 22, 2025
 * Date Revised: January 22, 2025
 *
 * Purpose:
 *    This component renders a modal for adding a court case by uploading a file
 *    or entering a link to a case document. It provides file validation, URL validation,
 *    drag-and-drop support, and dynamic styling for light and dark themes.
 *
 * Where the Program Fits in the General System Design:
 *    The Add Case Modal fits into the court case management workflow. It allows users
 *    to add court cases to the system by providing files or links, ensuring that valid
 *    inputs are processed and added seamlessly.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering and handling state.
 *    - react-icons: Used for the upload icon (FaUpload).
 *    - Tailwind CSS: For styling modal elements, inputs, and buttons.
 *    - ThemeContext: Provides dynamic styling for light and dark modes.
 *
 * Control Flow and Logic:
 *    1. `open`: Controls the visibility of the modal. If `open` is false, the modal
 *       is not rendered.
 *    2. `handleFileAdd`: Handles the addition of a valid uploaded file.
 *    3. `handleLinkAdd`: Handles the addition of a valid URL link.
 *    4. `handleFileLink`: Combines file handling and link validation with a reset callback.
 *    5. Validation:
 *       - Files: Only accepts `.txt` files with type `text/plain`.
 *       - Links: Validates URLs using a regex specific to batas.org.
 *    6. User feedback:
 *       - Displays error messages for invalid file types or URLs.
 *       - Shows a spinner and disables inputs when `loading` is true.
 *    7. Drag-and-Drop: Users can drag and drop a file, which triggers validation
 *       and file handling logic.
 *
 * Key Variables:
 *    - `fileName`: Stores the name of the selected file for display.
 *    - `link`: Tracks the entered link to a case document.
 *    - `isDragOver`: Boolean value for the drag-and-drop hover state.
 *    - `hasFile`: Boolean indicating if a valid file has been uploaded.
 *    - `hasLink`: Boolean indicating if a valid link has been entered.
 */

import { useState, useContext } from "react";
import { FaUpload } from "react-icons/fa";
import "../../assets/spinner.css";
import { ThemeContext } from "../../ThemeContext";

const AddCaseModal = ({
  open,
  onClose,
  handleFileAdd,
  handleLinkAdd,
  loading,
  handleFileLink,
}) => {
  const [fileName, setFileName] = useState(""); // State to store the selected file name
  const [link, setLink] = useState(""); // State to store the entered link
  const [isDragOver, setIsDragOver] = useState(false); // Drag-and-drop state
  const { isDarkMode } = useContext(ThemeContext);
  const [hasLink, setHasLink] = useState(true);
  const [hasFile, setHasFile] = useState(true);

  if (!open) return null;

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "text/plain") {
      setFileName(file.name); // Update the file name on selection
      console.log("valid file");
      handleFileAdd(event, resetFileName); // Pass the reset callback
      setHasFile(true);
    } else {
      console.log("invalid file");
      setHasFile(false);
      return;
    }
  };

  const handleFileChangeLink = (event) => {
    console.log("valid url:", validateURL(link.trim()));
    console.log("link url:", JSON.stringify(link));
    console.log("word count:", link.length);

    if (link.length < 1) {
      console.log("rejected: empty link");
      setHasLink(false);
      return;
    }

    if (!validateURL(link.trim())) {
      console.log("rejected: invalid URL");
      setHasLink(false);
      return;
    }

    setHasLink(true);

    handleFileLink(event, link, resetFileName); // Pass the reset callback
    setLink("");
  };

  const validateURL = (input) => {
    const regex =
      /^https:\/\/batas\.org\/(\d{4})\/(\d{2})\/(\d{2})\/(g-r-no-(l-)?\d+(-[a-z]+-\d{2}-\d{4})?|administrative-matter-no-\d{2}-\d{1,3}-\d{1,3}-sc)\/?$/;
    return regex.test(input);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragOver(false);
    const file = event.dataTransfer.files[0];
    if (file && file.type === "text/plain") {
      setFileName(file.name); // Update the file name on selection
      handleFileAdd(event, resetFileName); // Pass the reset callback
      setHasFile(true);
    } else {
      setHasFile(false);
      return;
    }
  };

  const resetFileName = () => {
    setFileName(""); // Reset the file name
  };

  return (
    <div
      className={`fixed inset-0 flex items-center justify-center z-50 ${
        isDarkMode
          ? "bg-black bg-opacity-50" // Dark mode: darker backdrop
          : "bg-gray-800 bg-opacity-50" // Light mode: lighter backdrop
      }`}
      aria-label="Add Case Modal"
    >
      <div
        className={`rounded-lg shadow-lg w-96 p-6 ${
          isDarkMode ? "bg-gray-700 text-white" : "bg-white text-black"
        }`}
      >
        <h2 className="text-xl font-semibold mb-6 text-center">
          Add Case File or Link
        </h2>
        {/* File Upload Input */}
        <div
          className={`border-2 ${
            isDragOver
              ? "border-blue-500 bg-blue-50"
              : isDarkMode
              ? "border-gray-600 bg-gray-700" // Dark mode styles
              : "border-gray-300 bg-white" // Light mode styles
          } border-dashed rounded-lg p-4 text-center transition`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="case-file"
            accept=".txt,.pdf,.docx"
            onChange={handleFileChange}
            className="hidden" // Hide the default input
            disabled={loading}
            aria-label="Upload Case File"
          />
          <label
            htmlFor="case-file"
            className={`cursor-pointer flex flex-col items-center ${
              isDarkMode ? "text-white" : "text-gray-600" // Dark mode vs light mode text color
            }`}
          >
            <FaUpload className="text-3xl mb-2" />
            <span
              className={`text-sm ${fileName ? "text-white" : "text-gray-400"}`}
            >
              {fileName || "Click to upload or drag and drop a file here"}
            </span>
          </label>
        </div>
        {!hasFile && (
          <p className="text-center" style={{ color: "red" }}>
            upload valid file type (.txt)
          </p>
        )}

        {/* Separator Line */}
        <div className="flex items-center my-4">
          <hr className="flex-grow border-gray-300" />
          <div
            className={`mx-2 px-2 text-sm font-semibold ${
              isDarkMode ? "text-gray-300" : "text-gray-500"
            }`}
          >
            OR
          </div>
          <hr className="flex-grow border-gray-300" />
        </div>
        {/* Link Input */}
        <div className="mt-4">
          <input
            type="text"
            className={`w-full border rounded p-2 text-sm placeholder-gray-400 ${
              isDarkMode
                ? "bg-gray-700 text-white border-gray-600" // Dark mode styles
                : "bg-white text-black border-gray-300" // Light mode styles
            }`}
            placeholder="Enter a link to a case document"
            onChange={(e) => setLink(e.target.value)}
            disabled={loading}
            aria-label="Enter Case Link"
          />

          <p
            className={`text-center p-2
                ${
                  hasLink
                    ? `${isDarkMode ? "text-gray-700" : "text-white"}`
                    : `${isDarkMode ? "text-red-400" : "text-red-500"}`
                }`}
          >
            Enter a valid URL from batas.org
          </p>

          <button
            className={`flex items-center justify-center w-full bg-blue-500 text-white px-4 pb-2 rounded hover:bg-blue-600 transition ${
              loading ? "opacity-50 cursor-not-allowed" : ""
            } ${isDarkMode ? "bg-blue-600 hover:bg-blue-800" : ""}`}
            onClick={handleFileChangeLink}
            disabled={loading}
            aria-label="Add Link"
          >
            Add Link
          </button>
        </div>
        {/* Loading State */}
        {loading && (
          <div className="flex items-center mt-4">
            <div className="spinner border-t-4 border-blue-500 rounded-full w-6 h-6 animate-spin"></div>
            <p
              className={`ml-2 ${isDarkMode ? "text-white" : "text-gray-600"}`}
            >
              Processing...
            </p>
          </div>
        )}
        {/* Action Buttons */}
        <div className="flex justify-end items-center mt-6">
          <button
            className={`bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition ${
              loading ? "opacity-50 cursor-not-allowed" : ""
            }`}
            onClick={() => {
              resetFileName(); // Reset the file name on cancel
              setLink(""); // Reset the link input field
              setHasFile(true);
              setHasLink(true);
              onClose();
            }}
            disabled={loading}
            aria-label="Cancel"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddCaseModal;

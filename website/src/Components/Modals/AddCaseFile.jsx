import React, { useState } from "react";
import { FaUpload } from "react-icons/fa";
import "../../assets/spinner.css";

const AddCaseModal = ({ open, onClose, handleFileAdd, loading }) => {
  const [fileName, setFileName] = useState(""); // State to store the selected file name
  const [isDragOver, setIsDragOver] = useState(false); // Drag-and-drop state

  if (!open) return null;

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFileName(file.name); // Update the file name on selection
      handleFileAdd(event, resetFileName); // Pass the reset callback
    }
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
    if (file) {
      setFileName(file.name); // Update the file name on drop
      handleFileAdd({ target: { files: [file] } }, resetFileName); // Pass the reset callback
    }
  };

  const resetFileName = () => {
    setFileName(""); // Reset the file name
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      aria-label="Add Case Modal"
    >
      <div className="bg-white rounded-lg shadow-lg w-96 p-6">
        <h2 className="text-xl font-semibold mb-6 text-center">
          Add Case File
        </h2>

        {/* File Upload Input */}
        <div
          className={`border-2 ${
            isDragOver ? "border-blue-500 bg-blue-50" : "border-gray-300"
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
            className="cursor-pointer flex flex-col items-center text-gray-600"
          >
            <FaUpload className="text-3xl mb-2" />
            <span className="text-sm">
              {fileName || "Click to upload or drag and drop a file here"}
            </span>
          </label>
        </div>

        {/* File Name Display */}
        {fileName && !loading && (
          <p className="mt-2 text-sm text-gray-500">
            Selected File: {fileName}
          </p>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex items-center mt-4">
            <div className="spinner border-t-4 border-blue-500 rounded-full w-6 h-6 animate-spin"></div>
            <p className="ml-2 text-gray-600">Uploading file...</p>
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

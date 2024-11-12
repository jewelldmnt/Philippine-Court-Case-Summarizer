/**
 * Program Title: Court Case Summarizer - AddCaseModal Component
 *
 * Programmer: Nicholas Dela Torre
 * Date Written: October 12, 2024
 * Date Revised: October 12, 2024
 *
 * Purpose:
 *    This component provides a modal dialog for adding a new court case to the
 *    system. It allows users to input a link to a court case, display a loading
 *    spinner while the case is being added, and handles the process of adding the
 *    case via the backend.
 *
 * Where the Program Fits in the General System Design:
 *    The AddCaseModal component serves as a user interface element for interacting
 *    with the backend, facilitating the addition of new court cases. It integrates
 *    with the court case summarizer system to upload new cases and manage them within
 *    the system.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering and handling user input.
 *    - react-icons: Used for the "Add" button icon (FaCirclePlus).
 *    - Tailwind CSS: For styling modal and form elements.
 *    - Custom spinner: CSS for handling the loading spinner animation.
 *
 * Control Flow and Logic:
 *    1. `open`: Controls the visibility of the modal. If `open` is false, the modal
 *       will not render.
 *    2. `handleFileAdd`: Handles the submission of the court case link to the backend.
 *    3. Conditional Rendering: Displays the loading spinner and disables form elements
 *       while the case is being added.
 *    4. `onClose`: Closes the modal when the cancel button is clicked.
 *
 * Key Variables:
 *    - `courtCaseLink`: Holds the value of the court case link entered by the user.
 *    - `setCourtCaseLink`: Function to update the `courtCaseLink` state.
 *    - `loading`: Boolean value indicating whether the case is being processed.
 *    - `handleFileAdd`: Function triggered to add the court case.
 */

import React from "react";
import { FaCirclePlus } from "react-icons/fa6";
import "../../assets/spinner.css";

const AddCaseModal = ({
  open,
  onClose,
  courtCaseLink,
  setCourtCaseLink,
  handleFileAdd,
  loading,
}) => {
  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-customRbox text-black p-6 rounded-lg w-[400px]">
        <h2 className="text-lg font-bold mb-4">Add Court Case</h2>
        <label className="block mb-2 font-semibold">Enter link:</label>
        <input
          type="text"
          className="border w-full p-2 rounded mb-4 text-black placeholder-gray-400"
          value={courtCaseLink}
          onChange={(e) => setCourtCaseLink(e.target.value)}
          disabled={loading} // Disable input while loading
        />

        {/* Loading state */}
        {loading ? (
          <div className="flex justify-center mb-4">
            <div className="spinner"></div>
            <p className="ml-2">Adding file...</p>
          </div>
        ) : null}

        <div className="flex justify-between">
          <button
            className="bg-primary -500 text-white px-4 py-2 rounded"
            onClick={handleFileAdd}
            disabled={loading} // Disable button while loading
          >
            {loading ? "Adding..." : "Add Case"}
          </button>
          <button
            className="bg-red-500 text-white px-4 py-2 rounded"
            onClick={onClose}
            disabled={loading} // Disable cancel button while loading
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddCaseModal;

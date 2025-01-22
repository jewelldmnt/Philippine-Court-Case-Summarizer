/**
 * Program Title: Court Case Summarizer - Cancel Component
 *
 * Programmer: Nicholas Dela Torre, Jino Llamado
 * Date Written: October 12, 2024
 * Date Revised: October 12, 2024
 *
 * Purpose:
 *    This component provides a confirmation dialog for discarding changes when
 *    editing a court case. It asks the user for confirmation before discarding any
 *    unsaved changes, offering the option to either discard or continue editing.
 *
 * Where the Program Fits in the General System Design:
 *    The Cancel component fits into the court case editing workflow. It allows users
 *    to safely discard changes and provides an opportunity to confirm their action
 *    before permanently removing any unsaved edits.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering and handling user input.
 *    - react-icons: Used for the question circle icon (BsQuestionCircle).
 *    - Tailwind CSS: For styling modal and button elements.
 *
 * Control Flow and Logic:
 *    1. `open`: Controls the visibility of the modal. If `open` is false, the modal
 *       will not render.
 *    2. `cancel`: Function to discard the changes and proceed with the action.
 *    3. `edit`: Function to keep the current changes and close the confirmation dialog.
 *    4. The modal is centered on the screen and features two action buttons:
 *       - `Discard edit`: Discards the changes and closes the modal.
 *       - `Keep editing`: Closes the modal without discarding changes.
 *
 * Key Variables:
 *    - `open`: Boolean value determining whether the modal is visible.
 *    - `cancel`: Function to trigger the discard action.
 *    - `edit`: Function to trigger the keep editing action.
 */

import { BsQuestionCircle } from "react-icons/bs";
import { useContext } from "react";
import { ThemeContext } from "../../ThemeContext";

const Cancel = ({ open, edit, cancel }) => {
  /**
   * Cancel Component
   *
   * Description:
   * Displays a modal to confirm if the user wants to discard changes. Includes
   * options to discard changes or continue editing. The modal appears based on
   * the `open` state and provides customizable handlers for user actions.
   *
   * Params:
   * @param {Object} props - The props object.
   * @param {boolean} props.open - Determines whether the modal is visible or not.
   * @param {function} props.edit - Function triggered when the user chooses to
   *                                continue editing.
   * @param {function} props.cancel - Function triggered when the user confirms
   *                                to discard changes.
   *
   * Returns:
   * @returns {JSX.Element|null} - The rendered modal component or null if `open` is false.
   */

  const { isDarkMode } = useContext(ThemeContext);

  if (!open) {
    return null;
  }

  return (
    <div
      className={`fixed inset-0 flex items-center justify-center z-50 ${
        isDarkMode
          ? "bg-black bg-opacity-50" // Dark mode: darker backdrop
          : "bg-gray-800 bg-opacity-50" // Light mode: lighter backdrop
      }`}
      aria-label="Cancel Modal"
    >
      <div
        className={`rounded-lg shadow-lg w-96 p-6 ${
          isDarkMode ? "bg-gray-700 text-white" : "bg-white text-black"
        }`}
      >
        <BsQuestionCircle className="text-3xl mb-4 mx-auto text-red-500" />
        <h2 className="text-xl font-semibold mb-4 text-center ">
          Are you sure you want to discard changes?
        </h2>
        <p
          className={`text-sm text-center mb-6 ${
            isDarkMode ? "text-gray-400" : "text-gray-500"
          }`}
        >
          This action cannot be undone.
        </p>
        <div className="flex justify-between">
          <button
            className="bg-red-500 font-bold text-white px-4 py-2 rounded hover:bg-red-600 transition duration-300"
            onClick={cancel}
          >
            Discard Changes
          </button>
          <button
            className="bg-blue-500 font-bold text-white px-4 py-2 rounded hover:bg-blue-600 transition duration-300"
            onClick={edit}
          >
            Keep Editing
          </button>
        </div>
      </div>
    </div>
  );
};

export default Cancel;

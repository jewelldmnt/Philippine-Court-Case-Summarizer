/**
 * Program Title: Court Case Summarizer - Confirm Save Component
 *
 * Programmer: Nicholas dela Torre
 * Date Written: January 22, 2025
 * Date Revised: January 22, 2025
 *
 * Purpose:
 *    This component provides a confirmation modal for saving changes to a court case.
 *    It prompts the user to confirm whether they want to save their changes, with options
 *    to cancel or proceed with saving. The modal appears based on the `isOpen` state.
 *
 * Where the Program Fits in the General System Design:
 *    The Confirm Save component is integrated into the court case editing flow.
 *    It ensures that users confirm their intent to save any changes made to a case,
 *    helping to prevent accidental overwrites.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering and handling state.
 *    - ThemeContext: Provides dynamic styling for light and dark modes.
 *    - react-icons: Used for the question circle icon (BsQuestionCircle).
 *
 * Control Flow and Logic:
 *    1. `isOpen`: Determines the visibility of the modal. If `isOpen` is false,
 *       the modal does not render.
 *    2. `onClose`: Closes the modal without saving the changes.
 *    3. `onSave`: Executes the save action and then closes the modal.
 *    4. User feedback:
 *       - Displays a warning message and confirmation buttons for the user to choose.
 *       - Modal content includes a red question circle icon to emphasize caution.
 *    5. Dynamic styling:
 *       - Applies different styles based on the current theme (light or dark mode).
 *
 * Key Variables:
 *    - `isOpen`: Boolean value controlling the visibility of the modal.
 *    - `onClose`: Function to close the modal without saving changes.
 *    - `onSave`: Function to save changes and close the modal.
 */

import { useContext } from "react";
import { ThemeContext } from "../../ThemeContext";
import { BsQuestionCircle } from "react-icons/bs";

const ConfirmSave = ({ isOpen, onClose, onSave }) => {
  /**
   * ConfirmSave Component
   *
   * Description:
   * Displays a confirmation modal for saving changes to a case. Provides options to cancel
   * the save action or confirm saving. The modal is visible based on the `isOpen`
   * state and calls the respective handlers on user actions.
   *
   * Params:
   * @param {Object} props - The props object.
   * @param {boolean} props.isOpen - Determines whether the modal is visible or not.
   * @param {function} props.onClose - Function triggered to close the modal.
   * @param {function} props.onSave - Function triggered when the user confirms
   *                                     the save action.
   *
   * Returns:
   * @returns {JSX.Element|null} - The rendered modal component or null if `isOpen`
   *                              is false.
   */
  if (!isOpen) return null;
  const { isDarkMode } = useContext(ThemeContext);

  return (
    <div
      className={`fixed inset-0 flex items-center justify-center z-50 ${
        isDarkMode
          ? "bg-black bg-opacity-50" // Dark mode: darker backdrop
          : "bg-gray-800 bg-opacity-50" // Light mode: lighter backdrop
      }`}
    >
      <div
        className={`rounded-lg shadow-lg w-96 p-6 ${
          isDarkMode ? "bg-gray-700 text-white" : "bg-white text-black"
        }`}
      >
        <BsQuestionCircle className="text-3xl mb-4 mx-auto text-red-500" />
        <h2 className="text-xl font-semibold mb-4 text-center ">
          Are you sure you want to save the changes to this court case?
        </h2>
        <p
          className={`text-sm text-center mb-6 ${
            isDarkMode ? "text-gray-400" : "text-gray-500"
          }`}
        >
          This action cannot be undone.
        </p>
        <div className="mt-6 flex justify-between">
          <button
            onClick={onClose}
            className={`rounded px-4 py-2 font-bold transition duration-300 ${
              isDarkMode
                ? "bg-gray-500 text-white hover:bg-gray-600" // Dark mode styles
                : "bg-gray-300 text-black hover:bg-gray-400" // Light mode styles
            }`}
          >
            Cancel
          </button>
          <button
            onClick={() => {
              onSave();
              onClose();
            }}
            className={`rounded px-4 py-2 font-bold ${
              isDarkMode
                ? "bg-red-600 text-white hover:bg-red-700" // Dark mode styles
                : "bg-red-500 text-white hover:bg-red-600" // Light mode styles
            }`}
          >
            Confirm Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmSave;

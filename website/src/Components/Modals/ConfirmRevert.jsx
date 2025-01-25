/**
 * Program Title: Court Case Summarizer - Confirm Revert Component
 *
 * Programmer: Nicholas dela Torre
 * Date Written: January 22, 2025
 * Date Revised: January 22, 2025
 *
 * Purpose:
 *    This component provides a confirmation modal for reverting changes made
 *    to a court case. It asks the user for confirmation before discarding all
 *    edits and reverting the case to its original state.
 *
 * Where the Program Fits in the General System Design:
 *    The Confirm Revert component is part of the court case editing workflow.
 *    It ensures that users confirm their intent to discard all changes, helping
 *    to prevent accidental data loss.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering and handling state.
 *    - ThemeContext: Provides dynamic styling for light and dark modes.
 *    - react-icons: Used for the question circle icon (BsQuestionCircle).
 *
 * Control Flow and Logic:
 *    1. `isOpen`: Determines the visibility of the modal. If `isOpen` is false,
 *       the modal does not render.
 *    2. `onClose`: Closes the modal without taking any further action.
 *    3. `onConfirm`: Executes the revert action and calls `onClose` to close the modal.
 *    4. User feedback:
 *       - Modal content includes a warning icon and descriptive text to
 *         clearly communicate the consequences of the revert action.
 *
 * Key Variables:
 *    - `isOpen`: Boolean value controlling the visibility of the modal.
 *    - `onClose`: Function to close the modal.
 *    - `onConfirm`: Function to execute the revert action and close the modal.
 */

import { useContext } from "react";
import { ThemeContext } from "../../ThemeContext";
import { BsQuestionCircle } from "react-icons/bs";

const ConfirmRevert = ({ isOpen, onClose, onConfirm }) => {
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
          Are you sure you want to revert the changes made to this court case?
        </h2>
        <p
          className={`text-sm text-center mb-6 ${
            isDarkMode ? "text-gray-400" : "text-gray-500"
          }`}
        >
          Revert to original will remove all edits made to this court case.
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
              onConfirm();
              onClose();
            }}
            className={`rounded px-4 py-2 font-bold ${
              isDarkMode
                ? "bg-red-600 text-white hover:bg-red-700" // Dark mode styles
                : "bg-red-500 text-white hover:bg-red-600" // Light mode styles
            }`}
          >
            Confirm Revert
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmRevert;

/**
 * Program Title: Court Case Management - ConfirmDelete Component
 *
 * Programmer: Nicholas Dela Torre, Jino Llamado, Jewell Anne Diamante
 * Date Written: November 15, 2024
 * Date Revised: January 22, 2025
 *
 * Purpose:
 *    This component provides a confirmation modal for deleting a court case.
 *    It allows users to confirm or cancel the deletion action, ensuring that
 *    deletions are intentional and irreversible.
 *
 * Where the Program Fits in the General System Design:
 *    The ConfirmDelete component acts as a user interface element that provides
 *    a safeguard against accidental deletions. It integrates into the court case
 *    management system, handling user confirmation for deletion actions.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering and handling user input.
 *    - Tailwind CSS: For styling modal and button elements.
 *
 * Control Flow and Logic:
 *    1. `isOpen`: Controls the visibility of the modal. If `isOpen` is false, the modal
 *       will not render.
 *    2. `onConfirm`: Triggered when the user confirms the deletion. It handles the
 *       deletion logic in the parent component or backend.
 *    3. `onClose`: Closes the modal without performing any action when the cancel
 *        button is clicked.
 *    4. Conditional Rendering: Ensures the modal only renders when `isOpen` is true.
 *
 * Key Variables:
 *    - `isOpen`: Boolean value that controls whether the modal is displayed.
 *    - `onClose`: Function to close the modal and cancel the action.
 *    - `onConfirm`: Function to execute the delete action upon user confirmation.
 */

import React from "react";
import { useContext } from "react";
import { ThemeContext } from "../../ThemeContext";
import { BsQuestionCircle } from "react-icons/bs";

const ConfirmDelete = ({ isOpen, onClose, onConfirm }) => {
  /**
   * ConfirmDelete Component
   *
   * Description:
   * Displays a confirmation modal for deleting an item. Provides options to cancel
   * the action or confirm the deletion. The modal is visible based on the `isOpen`
   * state and calls the respective handlers on user actions.
   *
   * Params:
   * @param {Object} props - The props object.
   * @param {boolean} props.isOpen - Determines whether the modal is visible or not.
   * @param {function} props.onClose - Function triggered to close the modal.
   * @param {function} props.onConfirm - Function triggered when the user confirms
   *                                      the deletion.
   *
   * Returns:
   * @returns {JSX.Element|null} - The rendered modal component or null if `isOpen`
   *                              is false.
   */
  const { isDarkMode } = useContext(ThemeContext);

  if (!isOpen) return null;

  return (
    <div
      className={`fixed inset-0 flex items-center justify-center z-50 ${
        isDarkMode
          ? "bg-black bg-opacity-50" // Dark mode: darker backdrop
          : "bg-gray-800 bg-opacity-50" // Light mode: lighter backdrop
      }`}
    >
      <div
        className={`rounded-lg shadow-lg w-96 p-6 text-center ${
          isDarkMode ? "bg-gray-700 text-white" : "bg-white text-black"
        }`}
      >
        <BsQuestionCircle className="text-3xl mb-4 mx-auto text-red-500" />
        <h2 className="text-xl font-semibold mb-4 text-center ">
          Are you sure you want to delete this court case?
        </h2>
        <p
          className={`text-sm text-center mb-6 ${
            isDarkMode ? "text-gray-400" : "text-gray-500"
          }`}
        >
          This action cannot be undone.
        </p>
        <div className="mt-6 flex justify-center space-x-40">
          <button
            onClick={onClose}
            className={`rounded px-4 py-2 font-bold ${
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
            className="bg-red-500 text-white rounded px-4 py-2 font-bold 
            hover:bg-red-600"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmDelete;

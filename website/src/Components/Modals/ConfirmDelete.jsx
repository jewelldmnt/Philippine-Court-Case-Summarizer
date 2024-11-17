/**
 * Program Title: Court Case Management - ConfirmDelete Component
 *
 * Programmer: Nicholas Dela Torre, Jino Llamado
 * Date Written: November 15, 2024
 * Date Revised: November 15, 2024
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
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center 
    justify-center z-50"
    >
      <div className="bg-white rounded-lg p-6 w-80 text-center">
        <h2 className="text-lg font-bold mb-4">Confirm Delete</h2>
        <p>Are you sure you want to delete this court case?</p>
        <div className="mt-6 flex justify-between">
          <button
            onClick={onClose}
            className="bg-gray-300 rounded px-4 py-2 font-bold hover:bg-gray-400"
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

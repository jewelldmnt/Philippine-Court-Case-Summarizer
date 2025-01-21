import React from "react";
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
        className={`rounded-lg shadow-lg w-96 p-6 ${
          isDarkMode ? "bg-gray-700 text-white" : "bg-white text-black"
        }`}
      >
        <BsQuestionCircle className="text-3xl mb-4 mx-auto text-blue-500" />
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
        <div className="mt-6 flex justify-center space-x-40">
          <button
            onClick={onClose}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition duration-300"
          >
            Cancel
          </button>
          <button
            onClick={() => {
              onSave();
              onClose();
            }}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition duration-300"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmSave;

import React from "react";

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

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-80 text-center">
        <h2 className="text-lg font-bold mb-4">Confirm Save</h2>
        <p>Are you sure you want to save the changes to this court case?</p>
        <div className="mt-6 flex justify-between">
          <button
            onClick={onClose}
            className="bg-gray-300 rounded px-4 py-2 font-bold hover:bg-gray-400"
          >
            Cancel
          </button>
          <button
            onClick={() => {
              onSave();
              onClose();
            }}
            className="bg-green-500 text-white rounded px-4 py-2 font-bold hover:bg-green-600"
          >
            Confirm Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmSave;

import React from "react";

const ConfirmDelete = ({ isOpen, onClose, onConfirm }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
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
            className="bg-red-500 text-white rounded px-4 py-2 font-bold hover:bg-red-600"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmDelete;

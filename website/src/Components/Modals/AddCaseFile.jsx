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
      <div className="bg-white text-black p-6 rounded-lg w-[400px]">
        <h2 className="text-lg font-bold mb-4">Add Court Case</h2>
        <label className="block mb-2 font-semibold">Enter link:</label>
        <input
          type="text"
          className="border w-full p-2 rounded mb-4"
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
            className="bg-blue-500 text-white px-4 py-2 rounded"
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

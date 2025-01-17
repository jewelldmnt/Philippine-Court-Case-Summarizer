import { useState } from "react";
import { NavLink } from "react-router-dom";
import { FaQuestionCircle } from "react-icons/fa";

const NavBar = ({ activePage }) => {
  const [isModalOpen, setIsModalOpen] = useState(false); // State for modal visibility

  const toggleModal = () => {
    setIsModalOpen(!isModalOpen); // Toggle modal visibility
  };

  const getModalContent = () => {
    if (activePage === "Summarizer") {
      return (
        <>
          <h2 className="text-lg font-bold mb-4">How to Use the Summarizer</h2>
          <ol className="list-decimal pl-5 text-sm space-y-2">
            <li>
              <b>Upload</b> a court case file by clicking <b>"Add Case."</b>
            </li>
            <li>
              <b>Select a file</b> from the list <b>to view</b> its details.
            </li>
            <li>
              Click <b>"Summarize" button</b> to process and view the summary.
            </li>
            <li>
              <b>Edit or delete</b> a file using the respective options.
            </li>
            <li>
              <b>Download</b> the summarized case as a `.txt` file. by pressing
              the <b>"Download" button</b>
            </li>
          </ol>
        </>
      );
    } else if (activePage === "Statistics") {
      return (
        <>
          <h2 className="text-lg font-bold mb-4">
            How to Use the Statistics Page
          </h2>
          <ol className="list-decimal pl-5 text-sm space-y-2">
            <li>
              <b>Select a court case</b> file from the list.
            </li>
            <li>
              <b>View the unigram and bigram frequency statistics</b> of the
              selected file.
            </li>
            <li>
              <b>Explore</b> the <b>word cloud visualization</b> of the court
              case text.
            </li>
            <li>
              <b>Use the statistics</b> to identify key terms and phrase
              patterns in the case.
            </li>
          </ol>
        </>
      );
    }
  };

  return (
    <>
      <div className="bg-customLight px-4 pt-6 border-b-[0.1px] border-[#3F3F3F] w-full">
        <div className="mb-3 mx-2 flex justify-between">
          <div className="flex items-center gap-[8px]">
            <img
              alt="logo"
              className="w-[17px]"
              src="/images/logo/ph_flag.png"
            />
            <p className="text-white font-bold font-sans text-[16px]">
              <span className="text-primary">PHILIPPINE </span>
              <span className="text-tertiary">COURT CASE </span>
              <span className="text-secondary">SUMMARIZER</span>
            </p>
          </div>
          <div className="flex text-white gap-10 font-bold text-[16px] font-sans mr-21">
            {/* Summarizer Link */}
            <div className="relative group">
              <NavLink to="/">
                <p
                  className={`cursor-pointer transition duration-300 ${
                    activePage === "Summarizer" ? "text-active" : "text-active1"
                  }`}
                >
                  Summarizer
                </p>
              </NavLink>
              <div className="absolute left-0 -bottom-1 w-full h-1 bg-active opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>

            {/* Statistics Link */}
            <div className="relative group">
              <NavLink to="/Statistics">
                <p
                  className={`cursor-pointer transition duration-300 ${
                    activePage === "Statistics" ? "text-active" : "text-active1"
                  }`}
                >
                  Statistics
                </p>
              </NavLink>
              <div className="absolute left-0 -bottom-1 w-full h-1 bg-active1 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>

            {/* Help Icon (Trigger for Modal) */}
            <div
              className="relative group cursor-pointer"
              onClick={toggleModal}
              title="Help"
            >
              <p className="text-black font-bold">
                <FaQuestionCircle size={24} />
              </p>
              <div className="absolute left-0 -bottom-1 w-full h-1 bg-active opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Modal (will show when isModalOpen is true) */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 shadow-lg">
            {getModalContent()}
            <button
              className="mt-4 bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600"
              onClick={toggleModal}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default NavBar;

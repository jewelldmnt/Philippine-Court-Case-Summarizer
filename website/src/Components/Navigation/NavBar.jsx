import { useState, useContext } from "react";
import { NavLink } from "react-router-dom";
import { FaSun, FaMoon, FaQuestionCircle } from "react-icons/fa";
import { ThemeContext } from "../../ThemeContext"; // Import ThemeContext, not ThemeProvider

const NavBar = ({ activePage }) => {
  const { isDarkMode, toggleTheme } = useContext(ThemeContext); // Use the correct context

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
              <b>Download</b> the summarized case as a `.txt` file by pressing
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
    <div
      className={`${
        isDarkMode ? "bg-darkPrimary text-white" : "bg-white text-black"
      } transition duration-300`}
    >
      <div
        className={`${
          isDarkMode ? "bg-darkPrimary border-gray-700" : "bg-customLight"
        } px-4 pt-6 border-b-[0.1px] w-full`}
      >
        <div className="mb-3 mx-2 flex justify-between items-center">
          <div className="flex items-center gap-[8px]">
            <img
              alt="logo"
              className="w-[17px]"
              src="/images/logo/ph_flag.png"
            />
            <p className="font-bold font-sans text-[16px]">
              <span
                className={`${
                  isDarkMode ? "text-darkAccent1" : "text-primary"
                }`}
              >
                PHILIPPINE{" "}
              </span>
              <span
                className={`${isDarkMode ? "text-white" : "text-tertiary"}`}
              >
                COURT CASE{" "}
              </span>
              <span
                className={`${
                  isDarkMode ? "text-darkAccent2" : "text-secondary"
                }`}
              >
                SUMMARIZER
              </span>
            </p>
          </div>
          <div className="flex items-center gap-10 font-bold text-[16px] font-sans">
            <NavLink to="/" className="relative group">
              <p
                className={`cursor-pointer transition duration-300 ${
                  activePage === "Summarizer"
                    ? isDarkMode
                      ? "text-darkAccent1"
                      : "text-primary"
                    : isDarkMode
                    ? "text-white"
                    : "text-black"
                }`}
              >
                Summarizer
              </p>
            </NavLink>
            <NavLink to="/Statistics" className="relative group">
              <p
                className={`cursor-pointer transition duration-300 ${
                  activePage === "Statistics"
                    ? isDarkMode
                      ? "text-darkAccent1"
                      : "text-primary"
                    : isDarkMode
                    ? "text-white"
                    : "text-black"
                }`}
              >
                Statistics
              </p>
            </NavLink>
            {/* Toggle Switch */}
            <div
              onClick={toggleTheme}
              className={`relative w-14 h-8 flex items-center rounded-full cursor-pointer p-1 transition-all duration-300 ${
                isDarkMode ? "bg-darkTertiary" : "bg-gray-300"
              }`}
            >
              <div
                className={`absolute w-6 h-6  rounded-full shadow-md transform transition-transform ${
                  isDarkMode
                    ? "translate-x-6 bg-darkSecondary"
                    : "translate-x-0 bg-white"
                }`}
              ></div>
              <FaSun
                className={`absolute left-1.5 transition-opacity ${
                  isDarkMode ? "opacity-0" : "opacity-100"
                }`}
                size={16}
                color="#FFD700"
              />
              <FaMoon
                className={`absolute right-1.5 transition-opacity ${
                  isDarkMode ? "opacity-100 text-yellow-400" : "opacity-0"
                }`}
                size={16}
              />
            </div>
            <div
              className="relative group cursor-pointer"
              onClick={toggleModal}
              title="Help"
            >
              <FaQuestionCircle size={24} />
            </div>
          </div>
        </div>
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div
            className={`${
              isDarkMode ? "bg-gray-700 text-white" : "bg-white text-black"
            } rounded-lg p-6 w-96 shadow-lg`}
          >
            {getModalContent()}
            <button
              className="mt-4 bg-blue-500 text-white hover:bg-blue-600 px-4 py-2 rounded shadow"
              onClick={toggleModal}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default NavBar;

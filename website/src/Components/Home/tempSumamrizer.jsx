import NavBar from "../Navigation/NavBar";
import Delete from "../Modals/Delete";
import Cancel from "../Modals/Cancel";
import Save from "../Modals/Save";
import { PiArrowLineDownBold } from "react-icons/pi";
import { FaCirclePlus, FaCircleMinus, FaTrash } from "react-icons/fa6";
import { ImCloudDownload } from "react-icons/im";
import { useState } from "react";
import { BiSolidEditAlt } from "react-icons/bi";
import { HiMiniLockOpen, HiMiniLockClosed } from "react-icons/hi2";

const Summarizer = () => {
  const [editCase, setEditCase] = useState(false);
  const [deleteCase, setDeleteCase] = useState(false);
  const [cancelEdit, setCancelEdit] = useState(false);
  const [saveEdit, setSaveEdit] = useState(false);

  const handleDeleteCase = () => {
    setDeleteCase(true);
  };

  const handleCancelDeleteCase = () => {
    setDeleteCase(false);
  };

  const handleCancelEdit = () => {
    setCancelEdit(false);
    setEditCase(!editCase);
  };

  const handleSaveEdit = () => {
    setSaveEdit(false);
    setEditCase(!editCase);
  };

  const [input, setInput] = useState({
    text: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Id iusto deleniti accusantium, ea quam aperiam repudiandae eos, iure magnam facere, tempore officia totam nesciunt similique odit dolore! At, maiores praesentium? Lorem ipsum dolor sit amet consectetur adipisicing elit. Id iusto deleniti accusantium, ea quam aperiam repudiandae eos, iure magnam facere, tempore officia totam nesciunt similique odit dolore! At, maiores praesentiumLorem ipsum dolor sit amet consectetur adipisicing elit. Id iusto deleniti accusantium, ea quam aperiam repudiandae eos, iure magnam facere, tempore officia totam nesciunt similique odit dolore! At, maiores praesentiumLorem ipsum dolor sit amet consectetur adipisicing elit. Id iusto deleniti accusantium, ea quam aperiam repudiandae eos, iure magnam facere, tempore officia totam nesciunt similique odit dolore! At, maiores praesentiumLorem ipsum dolor sit amet consectetur adipisicing elit. Id iusto deleniti accusantium, ea quam aperiam repudiandae eos, iure magnam facere, tempore officia totam nesciunt similique odit dolore! At, maiores praesentiumLorem ipsum dolor sit amet consectetur adipisicing elit. Id iusto deleniti accusantium, ea quam aperiam repudiandae eos, iure magnam facere, tempore officia totam nesciunt similique odit dolore! At, maiores praesentium...",
  });

  const wordCount = {
    count: "12345",
  };

  const handleOrigCase = () => {
    setEditCase(!editCase);
  };

  const [courtCases, setCourtCases] = useState([
    "Case No. 001: Smith vs. Johnson",
    "Case No. 002: State vs. Doe",
    "Case No. 003: Jones vs. State",
    "Case No. 004: Brown vs. Taylor",
    "Case No. 005: Wilson vs. Lee",
    "Case No. 006: Garcia vs. Martinez",
    "Case No. 007: Clark vs. Rodriguez",
    "Case No. 008: Lewis vs. Walker",
    "Case No. 009: Hall vs. Young",
    "Case No. 010: Allen vs. King",
  ]);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      // filename without the extension
      const fileNameWithoutExtension = file.name
        .split(".")
        .slice(0, -1)
        .join(".");
      // Add the file name to the list of court cases
      setCourtCases((prevCases) => [
        ...prevCases,
        `Case No. ${prevCases.length + 1}: ${fileNameWithoutExtension}`,
      ]);
    }
  };

  return (
    <>
      <Delete
        open={deleteCase}
        del={handleCancelDeleteCase}
        cancel={handleCancelDeleteCase}
      />
      <Cancel
        open={cancelEdit}
        edit={() => {
          setCancelEdit(false);
        }}
        cancel={handleCancelEdit}
      />
      <Save open={saveEdit} save={handleSaveEdit} />

      <div className="bg-background text-white h-screen">
        <NavBar activePage="Summarizer" />
        <div className="grid grid-cols-[1fr,2fr,2fr] gap-x-10 h-fit m-8">
          <div>
            <p className="font-bold font-sans text-[15px] ml-4 mb-4">
              LIST OF COURT CASES
            </p>
            <div className="font-sans text-sm bg-box rounded-xl py-6 h-[450px] overflow-y-auto custom-scrollbar">
              <ol className="list-decimal list-inside">
                {courtCases.map((caseTitle, index) => (
                  <li
                    key={index}
                    className="hover:bg-wordCount w-full px-4 cursor-pointer mb-2"
                  >
                    {caseTitle}
                  </li>
                ))}
              </ol>
            </div>
            <div className="mt-4 flex justify-between px-2">
              <label className="flex items-center cursor-pointer">
                <FaCirclePlus className="size-6 text-icon-10" />
                <p className="font-bold font-sans text-[14px] ml-2">Add Case</p>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </label>
              <button onClick={handleDeleteCase} className="flex items-center">
                <FaCircleMinus className="size-6 text-icon-20" />
                <p className="font-bold font-sans text-[14px] ml-2 ">
                  Delete Case
                </p>
              </button>
            </div>
          </div>

          <div>
            <p className="font-bold font-sans text-[15px] ml-4 mb-4 flex items-center">
              ORIGINAL COURT CASE
              {editCase ? (
                <>
                  <HiMiniLockOpen className="ml-2 size-6 text-primary" />
                </>
              ) : (
                <>
                  <HiMiniLockClosed className="ml-2 size-6 text-primary" />
                </>
              )}
            </p>
            <div className="relative">
              <textarea
                className="bg-box rounded-xl px-4 py-6 pb-10 h-[450px] w-full overflow-y-auto custom-scrollbar"
                value={input.text}
                onChange={(e) => setInput({ text: e.target.value })}
                readOnly={!editCase}
                style={{ paddingBottom: "2.5rem" }}
              />
              <div className="grid grid-cols-3 items-center font-sans font-bold text-xs absolute left-0 right-0 bottom-0 h-10 bg-wordCount rounded-bl-xl rounded-br-xl px-4 z-10">
                <div className="flex gap-2">
                  <p>Word Count:</p>
                  <p className="text-active">
                    {" "}
                    {input.text.split(/\s+/).filter(Boolean).length}{" "}
                  </p>
                  <label className="flex items-center cursor-pointer h-6 bg-summarize justify-center rounded-xl shadow-xl">
                    <p className="font-bold font-sans text-xs m-2">Summarize</p>
                    <input type="button" className="hidden" />
                  </label>
                </div>

                <div></div>
              </div>
            </div>

            {editCase ? (
              <div className="mt-4 flex justify-between px-2">
                <button
                  className="flex items-center"
                  onClick={() => {
                    setSaveEdit(true);
                  }}
                >
                  <PiArrowLineDownBold className="size-6 text-icon-10" />
                  <p className="font-bold font-sans text-[14px] ml-2">
                    Save Case
                  </p>
                </button>
                <button
                  className="flex items-center"
                  onClick={() => {
                    setCancelEdit(true);
                  }}
                >
                  <FaTrash className="size-6 text-icon-20" />
                  <p className="font-bold font-sans text-[14px] ml-2">
                    Cancel Edit
                  </p>
                </button>
              </div>
            ) : (
              <div className="mt-4 flex justify-center px-2">
                <button className="flex items-center" onClick={handleOrigCase}>
                  <BiSolidEditAlt className="text-icon-10 size-6" />
                  <p className="font-bold font-sans text-[14px] ml-2">
                    Edit Case
                  </p>
                </button>
              </div>
            )}
          </div>

          <div>
            <p className="font-bold font-sans text-[15px] ml-4 mb-4">
              SUMMARIZED COURT CASE
            </p>
            <div className="relative">
              <textarea
                className="bg-box rounded-xl px-4 py-6 pb-10 h-[450px] w-full overflow-y-auto custom-scrollbar"
                readOnly
                value={input.text}
                style={{ paddingBottom: "2.5rem" }}
              />
              <div className="gap-2 flex items-center font-sans font-bold text-xs absolute left-0 right-0 bottom-0 h-10 bg-wordCount rounded-bl-xl rounded-br-xl p-4 z-10">
                <p>Word Count:</p>
                <p className="text-active"> {wordCount.count} </p>
              </div>
            </div>
            <div className="mt-4 flex justify-center px-2">
              <button className="flex items-center">
                <ImCloudDownload className="text-icon-30 size-6" />
                <p className="font-bold font-sans text-[14px] ml-2">Download</p>
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Summarizer;

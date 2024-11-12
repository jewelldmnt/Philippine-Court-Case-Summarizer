/**
 * Program Title: Court Case Summarizer - Save Component
 *
 * Programmer: Nicholas Dela Torre
 * Date Written: October 12, 2024
 * Date Revised: October 12, 2024
 *
 * Purpose:
 *    This component displays a success message when changes to a court case
 *    have been successfully saved. It provides a visual confirmation to the user,
 *    letting them know that their changes have been applied.
 *
 * Where the Program Fits in the General System Design:
 *    The Save component serves as a feedback mechanism to inform the user
 *    that their changes have been successfully saved. It can be used in various
 *    parts of the application where changes are made to court cases, such as
 *    after editing or updating case details.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering and handling user interactions.
 *    - react-icons: Used for the success checkmark icon (IoCheckmarkDone).
 *    - Tailwind CSS: Used for styling the modal, text, and button elements.
 *
 * Control Flow and Logic:
 *    1. `open`: Controls the visibility of the modal. The modal will only be visible if `open` is true.
 *    2. `save`: Function to close the modal and acknowledge the saved changes.
 *    3. The modal includes a single action button:
 *       - `Okay`: Closes the modal and confirms the changes have been saved.
 *
 * Key Variables:
 *    - `open`: Boolean value that determines whether the modal is visible.
 *    - `save`: Function to handle the closure of the modal and acknowledge the success.
 */

import { IoCheckmarkDone } from "react-icons/io5";

const Save = ({ open, save }) => {
  if (!open) {
    return null;
  }

  return (
    <>
      <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 transition-opacity duration-300 z-50 ">
        <div className="font-sans text-white bg-box w-[350px] h-[270px] flex flex-col justify-center items-center text-center rounded-xl">
          <IoCheckmarkDone className="text-summarize w-[61px] h-[61px]" />
          <h1 className="font-bold text-[20px] tablet-xs:text-[24px]">
            Successfully Changed!
          </h1>
          <p className="mt-2 text-gray-400 text-[10px] tablet-xs:text-xs whitespace">
            Changes has been saved.
          </p>
          <div className="pt-4 flex flex-row space-x-2 font-bold">
            <button
              className=" p-2 w-20 rounded text-white bg-summarize"
              onClick={save}
            >
              Okay
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default Save;

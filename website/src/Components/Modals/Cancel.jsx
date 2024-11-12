/**
 * Program Title: Court Case Summarizer - Cancel Component
 *
 * Programmer: Nicholas Dela Torre, Jino Llamado
 * Date Written: October 12, 2024
 * Date Revised: October 12, 2024
 *
 * Purpose:
 *    This component provides a confirmation dialog for discarding changes when
 *    editing a court case. It asks the user for confirmation before discarding any
 *    unsaved changes, offering the option to either discard or continue editing.
 *
 * Where the Program Fits in the General System Design:
 *    The Cancel component fits into the court case editing workflow. It allows users
 *    to safely discard changes and provides an opportunity to confirm their action
 *    before permanently removing any unsaved edits.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering and handling user input.
 *    - react-icons: Used for the question circle icon (BsQuestionCircle).
 *    - Tailwind CSS: For styling modal and button elements.
 *
 * Control Flow and Logic:
 *    1. `open`: Controls the visibility of the modal. If `open` is false, the modal
 *       will not render.
 *    2. `cancel`: Function to discard the changes and proceed with the action.
 *    3. `edit`: Function to keep the current changes and close the confirmation dialog.
 *    4. The modal is centered on the screen and features two action buttons:
 *       - `Discard edit`: Discards the changes and closes the modal.
 *       - `Keep editing`: Closes the modal without discarding changes.
 *
 * Key Variables:
 *    - `open`: Boolean value determining whether the modal is visible.
 *    - `cancel`: Function to trigger the discard action.
 *    - `edit`: Function to trigger the keep editing action.
 */

import { BsQuestionCircle } from "react-icons/bs";

const Cancel = ({ open, edit, cancel }) => {
  if (!open) {
    return null;
  }

  return (
    <>
      <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 transition-opacity duration-300 z-50 ">
        <div className="font-sans text-black bg-customRbox w-[350px] h-[270px] flex flex-col justify-center items-center text-center rounded-xl">
          <BsQuestionCircle className="text-icon-10 w-[61px] h-[61px]" />
          <h1 className="font-bold text-[20px] tablet-xs:text-[24px]">
            Are you sure you want to <br />
            discard changes?
          </h1>
          <p className="mt-2 text-customRedText -500 text-[12px] tablet-xs:text-xs whitespace">
            This action cannot be undone.
          </p>
          <div className="pt-4 flex flex-row space-x-2 font-bold">
            <button
              className="p-2 w-35 hover:bg-active rounded transition ease-in-out duration-300"
              onClick={cancel}
            >
              Discard edit
            </button>
            <button
              className="p-2 w-35 rounded text-white bg-icon-10"
              onClick={edit}
            >
              Keep editing
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default Cancel;

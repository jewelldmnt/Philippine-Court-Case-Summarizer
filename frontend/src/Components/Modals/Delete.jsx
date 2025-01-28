/**
 * Program Title: Court Case Summarizer - Delete Component
 *
 * Programmer: Nicholas Dela Torre
 * Date Written: October 12, 2024
 * Date Revised: October 12, 2024
 *
 * Purpose:
 *    This component provides a confirmation dialog for deleting a court case.
 *    It prompts the user with a warning message, asking if they are sure they want
 *    to delete the case. The user has the option to cancel or confirm the deletion.
 *
 * Where the Program Fits in the General System Design:
 *    The Delete component is used when the user intends to remove a court case from
 *    the system. It ensures that the user confirms their decision before any irreversible
 *    action is taken.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering and managing user interactions.
 *    - react-icons: Used for the warning icon (IoWarningOutline).
 *    - Tailwind CSS: Utilized for styling the modal and buttons.
 *
 * Control Flow and Logic:
 *    1. `open`: Controls the visibility of the modal. The modal will not display unless `open` is true.
 *    2. `del`: Function that performs the case deletion.
 *    3. `cancel`: Function to close the modal without performing the deletion.
 *    4. The modal includes two action buttons:
 *       - `Cancel`: Closes the modal without deleting the case.
 *       - `Delete`: Confirms the action to delete the case.
 *
 * Key Variables:
 *    - `open`: Boolean value controlling whether the modal is visible.
 *    - `del`: Function to handle the deletion of the case.
 *    - `cancel`: Function to handle the cancellation and close the modal.
 */

import { IoWarningOutline } from "react-icons/io5";

const Delete = ({ open, del, cancel }) => {
  /**
   * Delete Component
   *
   * Description:
   * Displays a confirmation modal for deleting a case. Provides options to confirm
   * or cancel the delete action. The modal is visible based on the `open` state
   * and triggers the appropriate callback functions on user interaction.
   *
   * Params:
   * @param {Object} props - The props object.
   * @param {boolean} props.open - Determines whether the modal is visible or not.
   * @param {function} props.del - Function triggered when the user confirms the deletion.
   * @param {function} props.cancel - Function triggered to cancel the delete action
   *                                  and close the modal.
   *
   * Returns:
   * @returns {JSX.Element|null} - The rendered modal component if `open` is true,
   *                                 or null otherwise.
   */
  if (!open) {
    return null;
  }

  return (
    <>
      <div
        className="fixed inset-0 flex items-center justify-center bg-black 
      bg-opacity-50 transition-opacity duration-300 z-50 "
      >
        <div
          className="font-sans text-black bg-box w-[350px] h-[270px] flex 
        flex-col justify-center items-center text-center rounded-xl"
        >
          <IoWarningOutline className="text-delete w-[61px] h-[61px]" />
          <h1 className="font-bold text-[20px] tablet-xs:text-[24px]">
            Are you sure you want to <br />
            remove this case?
          </h1>
          <p
            className="mt-2 text-gray-400 text-[10px] tablet-xs:text-xs 
          whitespace"
          >
            This action cannot be undone.
          </p>
          <div className="pt-4 flex flex-row space-x-2 font-bold">
            <button
              className="p-2 w-20 hover:bg-active rounded transition ease-in-out 
              duration-300"
              onClick={cancel}
            >
              Cancel
            </button>
            <button
              className=" p-2 w-20 rounded text-white bg-delete"
              onClick={del}
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default Delete;

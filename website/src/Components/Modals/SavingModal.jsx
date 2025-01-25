/**
 * Program Title: Court Case Summarizer - Saving Modal Component
 *
 * Programmer: Nicholas dela Torre
 * Date Written: January 22, 2025
 * Date Revised: January 22, 2025
 *
 * Purpose:
 *    This component displays a modal with a loading spinner to indicate that a saving
 *    operation is in progress. The modal provides feedback to the user with a customizable
 *    message while the save action is being performed.
 *
 * Where the Program Fits in the General System Design:
 *    The Saving Modal is part of the user interface to indicate when the system is processing
 *    a save operation. It helps users understand that the action is being completed and prevents
 *    interaction with the system until the operation finishes.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering and handling state.
 *    - @mui/material: Provides the CircularProgress component for showing the loading spinner.
 *
 * Control Flow and Logic:
 *    1. `open`: Controls the visibility of the modal. If `open` is false, the modal does not render.
 *    2. `text`: A string passed as a prop to display custom text to the user indicating the action in progress.
 *    3. The modal is centered on the screen with a semi-transparent background to prevent interaction
 *       with other elements while the saving action is being completed.
 *    4. The modal includes a loading spinner (CircularProgress) and a text message.
 *
 * Key Variables:
 *    - `open`: Boolean value controlling the visibility of the modal.
 *    - `text`: Custom text to be displayed in the modal.
 */

import CircularProgress from "@mui/material/CircularProgress";

const SavingModal = ({ open, text }) => {
  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 flex flex-col items-center shadow-lg">
        <CircularProgress />
        <p className="mt-4 text-black text-sm">{text}</p>
      </div>
    </div>
  );
};

export default SavingModal;

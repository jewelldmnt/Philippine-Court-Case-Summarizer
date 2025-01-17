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

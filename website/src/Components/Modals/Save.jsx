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

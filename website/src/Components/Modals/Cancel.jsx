import { BsQuestionCircle } from "react-icons/bs";


const Cancel = ({open, edit, cancel}) => {
    if (!open) {
        return null;
      }


  return (
    <>
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 transition-opacity duration-300 z-50 ">
          <div className='font-sans text-black bg-customRbox w-[350px] h-[270px] flex flex-col justify-center items-center text-center rounded-xl'>
            <BsQuestionCircle className="text-icon-10 w-[61px] h-[61px]" />
            <h1 className='font-bold text-[20px] tablet-xs:text-[24px]'>Are you sure you want to <br />discard changes?</h1>
            <p className='mt-2 text-customRedText -500 text-[12px] tablet-xs:text-xs whitespace'>This action cannot be undone.</p>
            <div className='pt-4 flex flex-row space-x-2 font-bold'>
              <button className='p-2 w-35 hover:bg-active rounded transition ease-in-out duration-300' onClick={cancel}>Discard edit</button>
              <button className='p-2 w-35 rounded text-white bg-icon-10' onClick={edit}>Keep editing</button>
            </div>
          </div>
        </div>
    </>
  )
}

export default Cancel
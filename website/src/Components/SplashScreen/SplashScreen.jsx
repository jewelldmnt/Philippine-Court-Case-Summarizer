

const SplashScreen = () => {
  return (
    <> 
    <div className="flex flex-col">
        <div className="flex items-center gap-[8px]">
          <img alt="logo" className=" w-[24px]" src="/images/logo/ph_flag.png" />
          <p className="text-white font-bold font-sans text-[24px]"><span className="text-primary">PHILIPPINE</span> COURT CASE <span className="text-secondary">SUMMARIZER</span></p>
        </div>
        <div className="mt-2 flex justify-center items-center">
          <div className="loading-bar-container">
            <div className="loading-bar"></div>
          </div>
        </div>

        {/* 
        <div className="mt-2 flex justify-center items-center">
            <div className="relative statusLoad" role="status"></div>
        </div>
         */}
       
    </div>
    </>
  )
}

export default SplashScreen
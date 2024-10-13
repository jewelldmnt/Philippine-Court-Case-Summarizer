

import { NavLink } from 'react-router-dom';

const NavBar = ({ activePage }) => {
  return (
    <>
    <div className="bg-background p-4 pt-4">
        <div className="mb-3 mx-2 flex justify-between">
            <div className="flex items-center gap-[8px]">
                <img alt="logo" className=" w-[17px]" src="/images/logo/ph_flag.png" />
                <p className="text-white font-bold font-sans text-[16px]"><span className="text-primary">PHILIPPINE</span> COURT CASE <span className="text-secondary">SUMMARIZER</span></p>
            </div>
            <div className="flex text-white gap-20 font-bold text-[16px] font-sans mr-20">
                    <NavLink to='/'>
                    <p className={`cursor-pointer ${
                        activePage === "Summarizer" ? "text-active" : ""
                      }`}>
                        Summarizer
                    </p>
                    </NavLink>

                    <NavLink to='/Statistics'>
                    <p className={`cursor-pointer ${
                        activePage === "Statistics" ? "text-active" : ""
                      }`}>
                        Statistics
                    </p>
                    </NavLink>
            </div>
        </div>
        <div className="border border-b-[0.1px] border-[#3F3F3F]"></div>
    </div>
    </>
  )
}

export default NavBar


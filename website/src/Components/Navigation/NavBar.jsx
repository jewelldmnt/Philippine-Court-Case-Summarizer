import { NavLink } from 'react-router-dom';

const NavBar = ({ activePage }) => {
  return (
    <>
      <div className="bg-customLightBlue p-4 pt-4">
        <div className="mb-3 mx-2 flex justify-between">
          <div className="flex items-center gap-[8px]">
            <img alt="logo" className="w-[17px]" src="/images/logo/ph_flag.png" />
            <p className="text-white font-bold font-sans text-[16px]">
              <span className="text-primary">PHILIPPINE</span> COURT CASE{' '}
              <span className="text-secondary">SUMMARIZER</span>
            </p>
          </div>
          <div className="flex text-white gap-20 font-bold text-[16px] font-sans mr-20">
            {/* Summarizer Link */}
            <div className="relative group">
              <NavLink to="/">
                <p
                  className={`cursor-pointer transition duration-300 ${
                    activePage === "Summarizer" ? "text-active" : ""
                  }`}
                >
                  Summarizer
                </p>
              </NavLink>
              <div className="absolute left-0 -bottom-1 w-full h-1 bg-active opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>

            {/* Statistics Link */}
            <div className="relative group">
              <NavLink to="/Statistics">
                <p
                  className={`cursor-pointer transition duration-300 ${
                    activePage === "Statistics" ? "text-active" : ""
                  }`}
                >
                  Statistics
                </p>
              </NavLink>
              <div className="absolute left-0 -bottom-1 w-full h-1 bg-active opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
          </div>
        </div>
        <div className="border border-b-[0.1px] border-[#3F3F3F]"></div>
      </div>
    </>
  );
};

export default NavBar;

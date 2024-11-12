/**
 * Program Title: Court Case Summarizer - Navigation Bar
 *
 * Programmer: Nicholas Dela Torre, Jino Llamado
 * Date Written: October 12, 2024
 * Date Revised: October 12, 2024
 *
 * Purpose:
 *    This component renders the navigation bar of the Court Case Summarizer
 *    application. It includes links to different sections of the site, such as
 *    the "Summarizer" and "Statistics" pages, and dynamically highlights the
 *    active page based on the `activePage` prop.
 *
 * Where the Program Fits in the General System Design:
 *    The NavBar component is a part of the core layout and user interface,
 *    providing easy access to the key features of the application, allowing
 *    users to navigate between different sections.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering the navigation bar.
 *    - react-router-dom: Used for navigating between pages (NavLink).
 *    - Tailwind CSS: Used for styling the navigation bar, buttons, and hover effects.
 *
 * Control Flow and Logic:
 *    1. `activePage`: A string value that determines which navigation link is currently active.
 *    2. The component renders two main navigation links:
 *       - `Summarizer`: Navigates to the home page of the application.
 *       - `Statistics`: Navigates to the statistics page of the application.
 *    3. The active link is highlighted with a distinct color and an underline animation.
 *    4. When hovering over any link, an underline appears to indicate the active section.
 *
 * Key Variables:
 *    - `activePage`: A string representing the currently active page (either "Summarizer" or "Statistics").
 */


import { NavLink } from "react-router-dom";

const NavBar = ({ activePage }) => {
  return (
    <>
      <div className="bg-customLight px-4 pt-6">
        <div className="mb-3 mx-2 flex justify-between">
          <div className="flex items-center gap-[8px]">
            <img
              alt="logo"
              className="w-[17px]"
              src="/images/logo/ph_flag.png"
            />
            <p className="text-white font-bold font-sans text-[16px]">
              <span className="text-primary">PHILIPPINE </span>
              <span className="text-tertiary">COURT CASE </span>
              <span className="text-secondary">SUMMARIZER</span>
            </p>
          </div>
          <div className="flex text-white gap-20 font-bold text-[16px] font-sans mr-20">
            {/* Summarizer Link */}
            <div className="relative group">
              <NavLink to="/">
                <p
                  className={`cursor-pointer transition duration-300 ${
                    activePage === "Summarizer" ? "text-active" : "text-active1"
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
                    activePage === "Statistics" ? "text-active" : "text-active1"
                  }`}
                >
                  Statistics
                </p>
              </NavLink>
              <div className="absolute left-0 -bottom-1 w-full h-1 bg-active1 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
          </div>
        </div>
        <div className="border border-b-[0.1px] border-[#3F3F3F]"></div>
      </div>
    </>
  );
};

export default NavBar;

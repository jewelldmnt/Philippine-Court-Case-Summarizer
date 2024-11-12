/**
 * Program Title: Court Case Summarizer - Splash Screen
 *
 * Programmer: Nicholas Dela Torre, Jino Llamado
 * Date Written: October 12, 2024
 * Date Revised: October 12, 2024
 *
 * Purpose:
 *    This component renders a splash screen for the Court Case Summarizer
 *    application. It displays the logo and the name of the application along
 *    with a loading bar, which indicates that the app is in the process of
 *    loading.
 *
 * Where the Program Fits in the General System Design:
 *    The SplashScreen component appears when the application is first loaded
 *    to give users a visually engaging introduction and to allow time for any
 *    initial data to load or processes to complete before the main content is displayed.
 *
 * Dependencies and Resources:
 *    - React: Functional component for rendering the splash screen.
 *    - Tailwind CSS: Used for styling the splash screen, including the logo, text, and loading bar.
 *
 * Control Flow and Logic:
 *    1. Displays the logo of the application along with the name, which is styled with primary, tertiary, and secondary colors.
 *    2. A loading bar is displayed to visually indicate that the application is in a loading state.
 *    3. (Optional) A commented-out section includes a status loader that could be used for a more complex loading animation.
 *
 * Key Variables:
 *    None. This component does not rely on props or state variables.
 */

const SplashScreen = () => {
  return (
    <>
      <div className="flex flex-col">
        <div className="flex items-center gap-[8px]">
          <img
            alt="logo"
            className=" w-[24px]"
            src="/images/logo/ph_flag.png"
          />
          <p className="text-white font-bold font-sans text-[24px]">
            <span className="text-primary">PHILIPPINE </span>
            <span className="text-tertiary">COURT CASE </span>
            <span className="text-secondary">SUMMARIZER</span>
          </p>
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
  );
};

export default SplashScreen;

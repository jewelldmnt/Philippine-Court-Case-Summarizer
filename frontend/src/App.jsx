/**
 * Program Title: Court Case Summarizer - Main Application
 *
 * Programmer: Nicholas Dela Torre
 * Date Written: October 15, 2024
 * Date Revised: November 12, 2024
 *
 * Purpose:
 *    This is the main application component for the Court Case Summarizer.
 *    It manages the application's routing, controls the splash screen display,
 *    and handles the transition from the splash screen to the main content.
 *    The splash screen appears for 3 seconds before loading the primary application
 *    routes.
 *
 * Where the Program Fits in the General System Design:
 *    The `App` component serves as the entry point for the application. It manages
 *    the loading state (displaying the splash screen) and sets up routing for
 *    the app's different views (`Summarizer` and `Statistics`).
 *
 * Dependencies and Resources:
 *    - React: Utilized for building the UI components and handling state.
 *    - React Router (`react-router-dom`): Provides navigation between different
 *      views (routes) of the application.
 *    - CSS file (`App.css`): For styling the components and layout.
 *
 * Control Flow and Logic:
 *    1. The `useState` hook is used to manage the loading state, determining
 *      whether the splash screen or main content should be displayed.
 *    2. The `useEffect` hook sets a timer to control how long the splash screen
 *      is shown (3 seconds).
 *    3. After the timer expires, the splash screen is hidden, and the main content
 *      (routes) is displayed.
 *    4. The `BrowserRouter` component from `react-router-dom` is used to manage
 *      navigation, and `Routes` define the available paths (`/` for Summarizer
 *      and `/Statistics`).
 *
 * Key Variables:
 *    - `loading`: A boolean state that controls whether the splash screen or
 *      main app content is shown.
 *
 * Routing Logic:
 *    - `/`: Loads the `Summarizer` component (main view of the app).
 *    - `/Statistics`: Loads the `Statistics` component.
 */

import { useEffect, useState } from "react";
import "./App.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";

import SplashScreen from "./Components/SplashScreen/SplashScreen.jsx";
import Summarizer from "./Components/Home/Summarizer.jsx";
import Statistics from "./Components/Home/Statistics.jsx";
import ThemeProvider from "./ThemeContext.jsx";

function App() {
  /**
   * Description:
   * The main entry point of the application. Displays a splash screen for 3 seconds
   * and then renders the main application with routes for the `Summarizer`
   * and `Statistics` components.
   *
   * Parameter:
   * None
   *
   * Returns:
   * {JSX.Element} -
   * - Displays a splash screen (`SplashScreen` component) while loading is `true`.
   * - After 3 seconds, renders the main app with routes for `Summarizer` and
   * `Statistics` components using `BrowserRouter`.
   */

  const [loading, setLoading] = useState(false);
  useEffect(() => {
    setLoading(true);
    const timer = setTimeout(() => {
      setLoading(false);
    }, 3000); // Display splash screen for 3 seconds (3000 ms)

    return () => clearTimeout(timer); // Clean up the timer
  }, []);

  return (
    <ThemeProvider>
      {loading ? (
        <div className="flex justify-center items-center h-screen  bg-background ">
          <SplashScreen />
        </div>
      ) : (
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Summarizer />} />
            <Route path="/Statistics" element={<Statistics />} />
          </Routes>
        </BrowserRouter>
      )}
    </ThemeProvider>
  );
}

export default App;

/**
 * Program Title: Theme Context Provider
 *
 * Programmer: Jewell Anne Diamante
 * Date Written: January 18, 2025
 * Date Revised: January 18, 2025
 *
 * Purpose:
 *    This component provides a global theme context for the application.
 *    It manages the application's theme mode (dark or light) and allows
 *    components to toggle between the modes. It also persists the user's
 *    theme preference using `localStorage`.
 *
 * Where the Program Fits in the General System Design:
 *    The `ThemeProvider` component wraps the entire application, ensuring
 *    that any component within the app can access the `ThemeContext` to read
 *    or update the theme mode.
 *
 * Dependencies and Resources:
 *    - React: For managing state (`useState`) and lifecycle methods (`useEffect`).
 *    - localStorage: To persist the user's theme preference across sessions.
 *
 * Control Flow and Logic:
 *    1. The `isDarkMode` state is initialized by reading the stored theme
 *       preference from `localStorage` (defaulting to `false` if not found).
 *    2. The `useEffect` hook listens for changes to `isDarkMode` and updates
 *       `localStorage` whenever the theme mode is toggled.
 *    3. The `toggleTheme` function toggles the `isDarkMode` state between
 *       `true` (dark mode) and `false` (light mode).
 *    4. The current theme mode and `toggleTheme` function are made available
 *       to child components through the `ThemeContext.Provider`.
 *
 * Key Variables:
 *    - `isDarkMode`: A boolean state indicating whether dark mode is enabled.
 *    - `toggleTheme`: A function to toggle the theme between dark and light.
 *
 * How to Use:
 *    - Wrap the root component of the application with `ThemeProvider`.
 *    - Use the `ThemeContext` in child components to access or update the theme.
 *
 * Example Usage:
 *    import { useContext } from "react";
 *    import { ThemeContext } from "./ThemeProvider";
 *
 *    const Component = () => {
 *        const { isDarkMode, toggleTheme } = useContext(ThemeContext);
 *        return (
 *            <button onClick={toggleTheme}>
 *                Switch to {isDarkMode ? "Light" : "Dark"} Mode
 *            </button>
 *        );
 *    };
 */

import React, { createContext, useState, useEffect } from "react";

export const ThemeContext = createContext();

const ThemeProvider = ({ children }) => {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    // Retrieve initial state from localStorage
    return localStorage.getItem("isDarkMode") === "true";
  });

  useEffect(() => {
    // Save dark mode preference to localStorage
    localStorage.setItem("isDarkMode", isDarkMode);
  }, [isDarkMode]);

  const toggleTheme = () => {
    setIsDarkMode((prevMode) => !prevMode);
  };

  return (
    <ThemeContext.Provider value={{ isDarkMode, toggleTheme }}>
      <div className={isDarkMode ? "dark" : ""}>{children}</div>
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;

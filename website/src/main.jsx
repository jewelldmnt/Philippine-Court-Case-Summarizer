/**
 * Program Title: Court Case Summarizer - Application Entry
 *
 * Programmer: Nicholas Dela Torre
 * Date Written: October 15, 2024
 * Date Revised: November 12, 2024
 *
 * Purpose:
 *    This is the entry point for the Court Case Summarizer application. 
 *    It initializes the React application by rendering the `App` component into 
 *    the root HTML element and applying `StrictMode` to help identify potential 
 *    problems in the application during development.
 *
 * Where the Program Fits in the General System Design:
 *    This file serves as the main entry point where the React app is bootstrapped 
 *    and rendered. It is responsible for rendering the root component (`App`) of 
 *    the application into the DOM.
 *
 * Dependencies and Resources:
 *    - React: The main JavaScript library for building user interfaces.
 *    - React DOM (`react-dom/client`): Used for rendering the React application 
 *                                      into the DOM.
 *    - `index.css`: Global CSS file for styling the application.
 *
 * Control Flow and Logic:
 *    1. The `createRoot` function from `react-dom/client` is called to create a 
 *        root React element in the DOM.
 *    2. The `StrictMode` wrapper is used to highlight potential issues in the 
 *        development build.
 *    3. The `App` component is rendered as the root component, serving as the 
 *        entry point for the rest of the app.
 *
 * Key Variables:
 *    - `root`: The root DOM element where the React application is mounted 
 *              (retrieved using `document.getElementById('root')`).
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);

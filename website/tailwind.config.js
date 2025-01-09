/** @type {import('tailwindcss').Config} */
import tailwindScrollbar from "tailwind-scrollbar";

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        customLight: "#FFFFFF", // Use for Navbar Color
        customGray: "#EEEEEE", // Use for Background
        customWC: "#62B5FF",
        customRbox: "#FFFFFF", // Use for light color of rounded box
        customLock: "#FDAD15", // Use for lock button
        customRedText: "#972338",
        customHoverC: "#79B5E1",
        primary: "#4D91E2",
        secondary: "#DF1619",
        tertiary: "#192E40",
        background: "#EEEEEE",
        wordCount: "#205D93",
        active: "#79B5E1",
        active1: "#192E40",
        delete: "#D90429",
        summarize: "#EBF4FB",
        icon: {
          10: "#F67F3B",
          20: "#F05546",
          30: "#329A30",
          40: "#FFC14B",
        },
      },
    },
  },
  plugins: [
    tailwindScrollbar({ nocompatible: true }), // Use the imported plugin
  ],
};

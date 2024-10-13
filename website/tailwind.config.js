/** @type {import('tailwindcss').Config} */
import tailwindScrollbar from "tailwind-scrollbar";

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#4D91E2",
        secondary: "#FC5271",
        background: "#021526",
        box: "#192E40",
        wordCount: "#3B5366",
        active: "#B1D8FB",
        delete: "#D90429",
        summarize: "#1F8146",
        icon: {
          10: "#FDAD15",
          20: "#FF6252",
          30: "#61BB5F",
        },
      },
    },
  },
  plugins: [
    tailwindScrollbar({ nocompatible: true }), // Use the imported plugin
  ],
};

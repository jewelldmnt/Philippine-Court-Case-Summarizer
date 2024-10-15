/** @type {import('tailwindcss').Config} */
import tailwindScrollbar from "tailwind-scrollbar";

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        customLightBlue: "#649AC2", // Use for Light Blue Blackground
        customRbox:"#2C77AD", // Use for light color of rounded box
        primary: "#0D2541",
        secondary: "#DF1619",
        background: "#649AC2",
        wordCount: "#155686",
        active: "#052B4D",
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

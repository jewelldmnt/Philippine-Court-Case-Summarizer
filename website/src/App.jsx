import { useEffect, useState } from 'react';
import './App.css';

import { BrowserRouter, Routes, Route } from "react-router-dom";

import SplashScreen from './Components/SplashScreen/SplashScreen.jsx';
import Summarizer from './Components/Home/Summarizer.jsx';
import Statistics from './Components/Home/Statistics.jsx';

function App() {
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    setLoading(true);
    const timer = setTimeout(() => {
      setLoading(false);
    }, 3000); // Display splash screen for 3 seconds (3000 ms)

    return () => clearTimeout(timer); // Clean up the timer
  }, []);

  return (
    <>
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
    </>
  );
}

export default App;

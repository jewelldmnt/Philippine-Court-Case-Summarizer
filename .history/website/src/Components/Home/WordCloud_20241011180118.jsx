import { useEffect, useState } from "react";

const WordCloud = ({ stats }) => {
  const [positions, setPositions] = useState([]);

  const getFontSize = (frequency) => {
    const maxFrequency = Math.max(...stats.map((stat) => stat.frequency));
    const minFrequency = Math.min(...stats.map((stat) => stat.frequency));
    const fontSize =
      12 + ((frequency - minFrequency) / (maxFrequency - minFrequency)) * 40;
    return `${fontSize}px`;
  };

  useEffect(() => {
    // Generate random positions only once when stats change
    const newPositions = stats.map(() => ({
      top: `${Math.random() * 80}%`,
      left: `${Math.random() * 80}%`,
    }));
    setPositions(newPositions);
  }, [stats]);

  if (!stats || stats.length === 0) {
    return <p>No word cloud data available.</p>;
  }

  return (
    <div className="relative h-[300px] w-[100%] overflow-hidden bg-gray-200">
      {stats.map((stat, index) => (
        <div
          key={stat.rank}
          className="absolute font-sans font-bold"
          style={{
            fontSize: getFontSize(stat.frequency),
            top: positions[index]?.top,
            left: positions[index]?.left,
            transform: "translate(-50%, -50%)",
            whiteSpace: "nowrap",
          }}
        >
          {stat.unigram || stat.bigram}
        </div>
      ))}
    </div>
  );
};

export default WordCloud;

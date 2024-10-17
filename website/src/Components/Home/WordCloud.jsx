const WordCloud = ({ stats }) => {
  const getFontSize = (frequency) => {
    const maxFrequency = Math.max(...stats.map((stat) => stat.frequency));
    const minFrequency = Math.min(...stats.map((stat) => stat.frequency));

    // Handle case where all frequencies are the same
    if (maxFrequency === minFrequency) {
      return "20px"; // Default font size when there's no frequency range
    }

    const fontSize =
      12 + ((frequency - minFrequency) / (maxFrequency - minFrequency)) * 40;
    return `${fontSize}px`;
  };

  if (!stats || stats.length === 0) {
    return <p>No word cloud data available.</p>;
  }

  return (
    <div
      className="relative w-full h-full overflow-hidden"
      // Adjust height for the container
      style={{ position: "relative", maxWidth: "100%", maxHeight: "100%" }}
    >
      {stats.map((stat) => (
        <div
          key={stat.rank}
          className="absolute font-sans font-bold"
          style={{
            fontSize: getFontSize(stat.frequency),
            top: `${Math.random() * 80 + 10}%`, // Keeps word within 10%-90% height of container
            left: `${Math.random() * 80 + 10}%`, // Keeps word within 10%-90% width of container
            transform: "translate(-50%, -50%)",
            whiteSpace: "nowrap",
            pointerEvents: "none", // Prevents interaction interference
          }}
        >
          {stat.unigram ? stat.unigram : stat.bigram}
        </div>
      ))}
    </div>
  );
};

export default WordCloud;

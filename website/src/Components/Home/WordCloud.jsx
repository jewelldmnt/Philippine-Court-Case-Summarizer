const WordCloud = ({ stats }) => {
  const getFontSize = (frequency) => {
    const maxFrequency = Math.max(...stats.map((stat) => stat.frequency));
    const minFrequency = Math.min(...stats.map((stat) => stat.frequency));
    const fontSize =
      12 + ((frequency - minFrequency) / (maxFrequency - minFrequency)) * 40;
    return `${fontSize}px`;
  };

  if (!stats || stats.length === 0) {
    return <p>No word cloud data available.</p>;
  }

  return (
    <div className="relative h-full w-full overflow-hidden">
      {stats.map((stat) => (
        <div
          key={stat.rank}
          className="absolute animate-move font-sans font-bold"
          style={{
            fontSize: getFontSize(stat.frequency),
            top: `${Math.random() * 80}%`,
            left: `${Math.random() * 80}%`,
            transform: "translate(-50%, -50%)",
            whiteSpace: "nowrap",
          }}
        >
          {stat.unigram}
        </div>
      ))}
    </div>
  );
};

export default WordCloud;

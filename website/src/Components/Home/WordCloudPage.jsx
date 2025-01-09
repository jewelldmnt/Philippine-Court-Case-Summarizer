import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import cloud from "d3-cloud";

const WordCloudPage = ({ stats }) => {
  const cloudRef = useRef();

  useEffect(() => {
    if (!stats || stats.length === 0) return;

    const container = cloudRef.current;
    const width = container.offsetWidth - 20; // Adjust for margins
    const height = container.offsetHeight - 20; // Adjust for margins

    const maxFontSize = Math.min(width, height) / 5; // Adjust divisor for scaling
    const minFontSize = maxFontSize / 4; // Ensure readability for smaller words

    const fontSizeScale = d3
      .scaleLinear()
      .domain([0, d3.max(stats, (d) => d.frequency)])
      .range([minFontSize, maxFontSize]);

    const layout = cloud()
      .size([width, height])
      .words(
        stats.map((d) => ({
          text: d.unigram || d.bigram, // Handle both unigram and bigram
          size: fontSizeScale(d.frequency),
        }))
      )
      .padding(5)
      .rotate(() => (Math.random() > 0.5 ? 0 : 90))
      .font("sans-serif")
      .fontSize((d) => d.size)
      .on("end", draw);

    layout.start();

    function draw(words) {
      d3.select(container).select("svg").remove(); // Clear previous cloud

      d3.select(container)
        .append("svg")
        .attr("width", layout.size()[0])
        .attr("height", layout.size()[1])
        .append("g")
        .attr(
          "transform",
          `translate(${layout.size()[0] / 2}, ${layout.size()[1] / 2})`
        )
        .selectAll("text")
        .data(words)
        .enter()
        .append("text")
        .style("font-size", (d) => `${d.size}px`)
        .style("font-family", "sans-serif")
        .style(
          "fill",
          () => d3.schemeCategory10[Math.floor(Math.random() * 10)]
        )
        .attr("text-anchor", "middle")
        .attr(
          "transform",
          (d) => `translate(${d.x}, ${d.y}) rotate(${d.rotate})`
        )
        .text((d) => d.text);
    }
  }, [stats]);

  return <div ref={cloudRef} className="wordcloud-container"></div>;
};

export default WordCloudPage;

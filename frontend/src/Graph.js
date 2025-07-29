import { useEffect, useRef } from "react";
import * as d3 from "d3";

export default function Graph({ highlight }) {
  const ref = useRef();

  useEffect(() => {
    fetch("http://localhost:5000/api/graph")
      .then((res) => res.json())
      .then((data) => {
        const svg = d3.select(ref.current);
        svg.selectAll("*").remove(); // clear before redraw

        const width = ref.current.clientWidth || 600;
        const height = ref.current.clientHeight || 600;

        const simulation = d3.forceSimulation(data.nodes)
          .force("link", d3.forceLink(data.links).id((d) => d.id).distance(100))
          .force("charge", d3.forceManyBody().strength(-300))
          .force("center", d3.forceCenter(width / 2, height / 2));

        const link = svg.append("g")
          .attr("stroke", "#aaa")
          .selectAll("line")
          .data(data.links)
          .enter()
          .append("line");

        const node = svg.append("g")
          .selectAll("circle")
          .data(data.nodes)
          .enter()
          .append("circle")
          .attr("r", 6)
          .attr("fill", (d) => {
            if (highlight.includes(d.id)) return "orange";
            if (d.type === "added") return "green";
            if (d.type === "deleted") return "red";
            if (d.type === "modified") return "blue";
            return "gray";
          })
          .call(d3.drag()
            .on("start", (event, d) => {
              if (!event.active) simulation.alphaTarget(0.3).restart();
              d.fx = d.x;
              d.fy = d.y;
            })
            .on("drag", (event, d) => {
              d.fx = event.x;
              d.fy = event.y;
            })
            .on("end", (event, d) => {
              if (!event.active) simulation.alphaTarget(0);
              d.fx = null;
              d.fy = null;
            })
          );

        simulation.on("tick", () => {
          link
            .attr("x1", (d) => d.source.x)
            .attr("y1", (d) => d.source.y)
            .attr("x2", (d) => d.target.x)
            .attr("y2", (d) => d.target.y);

          node
            .attr("cx", (d) => d.x)
            .attr("cy", (d) => d.y);
        });
      });
  }, [highlight]);

  return (
    <svg
      ref={ref}
      style={{ width: "100%", height: "100%", backgroundColor: "#f9f9f9" }}
    />
  );
}

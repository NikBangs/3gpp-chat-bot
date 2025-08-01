import React, { useEffect, useRef } from "react";
import ForceGraph2D from "react-force-graph-2d";

function Graph({ graphData, highlightedNodes }) {
  const fgRef = useRef();

  useEffect(() => {
    if (fgRef.current) {
      fgRef.current.zoomToFit(400); // Adjust zoom duration
    }
  }, [graphData]);

  return (
    <ForceGraph2D
      ref={fgRef}
      graphData={graphData}
      width={window.innerWidth * 0.66} // Adjust width for 2/3 screen
      height={window.innerHeight}
      nodeLabel={(node) => node.id}
      nodeAutoColorBy="id"
      nodeCanvasObject={(node, ctx, globalScale) => {
        const label = node.id;
        const fontSize = 10 / globalScale;
        ctx.font = `${fontSize}px Sans-Serif`;
        ctx.fillStyle = node.color || "black";
        ctx.beginPath();
        ctx.arc(node.x, node.y, 4, 0, 2 * Math.PI, false);
        ctx.fill();
        ctx.fillText(label, node.x + 6, node.y + 4);
      }}
      linkColor={() => "rgba(0,0,0,0.1)"}
    />
  );
}

export default Graph;

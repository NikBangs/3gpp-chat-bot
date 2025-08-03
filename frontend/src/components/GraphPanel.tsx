import React, { useEffect, useRef, useState } from 'react';

interface GraphPanelProps {
  highlightedNodes?: string[];
  graphHtmlUrl?: string;
}

const GraphPanel: React.FC<GraphPanelProps> = ({ 
  highlightedNodes = [], 
  graphHtmlUrl = "/data/graph.html" 
}) => {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;

    const handleLoad = () => {
      setIsLoading(false);
      try {
        // Try to access iframe content for highlighting
        const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;
        if (iframeDoc && highlightedNodes.length > 0) {
          // Focus on highlighted nodes if the graph is loaded
          highlightNodes(iframeDoc, highlightedNodes);
        }
      } catch (err) {
        console.log('Cannot access iframe content due to CORS restrictions');
      }
    };

    const handleError = () => {
      setIsLoading(false);
      setError('Failed to load graph visualization');
    };

    iframe.addEventListener('load', handleLoad);
    iframe.addEventListener('error', handleError);

    return () => {
      iframe.removeEventListener('load', handleLoad);
      iframe.removeEventListener('error', handleError);
    };
  }, [highlightedNodes]);

  const highlightNodes = (doc: Document, nodeIds: string[]) => {
    try {
      // This would interact with the vis-network instance in the iframe
      // The actual implementation depends on how the PyVis graph exposes its API
      const scriptElement = doc.createElement('script');
      scriptElement.textContent = `
        if (typeof network !== 'undefined' && network) {
          // Highlight specified nodes
          const nodesToHighlight = ${JSON.stringify(nodeIds)};
          if (nodesToHighlight.length > 0) {
            // Focus on the first highlighted node
            network.focus(nodesToHighlight[0], {
              scale: 1.2,
              animation: {
                duration: 1000,
                easingFunction: 'easeInOutQuad'
              }
            });
            
            // You can add additional highlighting logic here
            // such as changing node colors or adding effects
          }
        }
      `;
      doc.head.appendChild(scriptElement);
    } catch (err) {
      console.log('Could not highlight nodes:', err);
    }
  };

  if (error) {
    return (
      <div className="graph-panel">
        <div className="graph-loading">
          <div className="text-center">
            <h3 className="text-lg font-semibold mb-2">Graph Unavailable</h3>
            <p className="text-sm opacity-75">{error}</p>
            <p className="text-xs opacity-50 mt-2">
              Make sure your graph.html is accessible at {graphHtmlUrl}
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="graph-panel">
      {isLoading && (
        <div className="graph-loading">
          <div className="text-center">
            <div className="animate-spin w-8 h-8 border-2 border-white border-t-transparent rounded-full mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold mb-2">Loading Graph</h3>
            <p className="text-sm opacity-75">Initializing 3GPP Knowledge Graph...</p>
          </div>
        </div>
      )}
      
      <iframe
        ref={iframeRef}
        src={graphHtmlUrl}
        className="graph-iframe"
        title="3GPP Knowledge Graph"
        sandbox="allow-scripts allow-same-origin allow-forms"
      />
    </div>
  );
};

export default GraphPanel;
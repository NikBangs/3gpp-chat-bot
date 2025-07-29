from dotenv import load_dotenv
load_dotenv()

import os
import time
import networkx as nx
from openai import OpenAI

# Load your OpenAI API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "You're an expert summarizer for technical documents. "
    "Summarize the section content into a short but meaningful title. "
    "Avoid repeating the section number. Be clear and concise."
)

def summarize_text_gpt(text, retries=3, delay=2):
    """
    Sends section text to GPT-3.5 to generate a one-line title.
    """
    if not text.strip():
        return "Untitled Section"

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text.strip()}
                ],
                temperature=0.4,
                max_tokens=32,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"⚠️ GPT error (attempt {attempt + 1}): {e}")
            time.sleep(delay)

    return "Untitled Section"

def summarize_graph_nodes(G: nx.DiGraph):
    """
    Loops over graph nodes and adds a 'title' field using GPT-3.5
    """
    print("✍️  Summarizing node content using GPT-3.5...")
    enriched_count = 0

    for node_id, data in G.nodes(data=True):
        if "title" in data and data["title"].strip():
            continue  # Skip if already has a title

        text = data.get("text", "").strip()
        summary = summarize_text_gpt(text)
        G.nodes[node_id]["title"] = summary
        enriched_count += 1
        print(f"📝 {node_id}: {summary}")

    print(f"✅ Added summaries to {enriched_count} nodes.")
    return G


if __name__ == "__main__":
    import pickle

    GRAPH_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/unified_graph.pkl"))

    if not os.path.exists(GRAPH_PATH):
        print(f"❌ Graph file not found at {GRAPH_PATH}")
    else:
        with open(GRAPH_PATH, "rb") as f:
            G = pickle.load(f)

        G = summarize_graph_nodes(G)

        with open(GRAPH_PATH, "wb") as f:
            pickle.dump(G, f)

        print("💾 Graph with titles saved.")
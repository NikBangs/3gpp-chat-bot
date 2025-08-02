from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util
from collections import OrderedDict

import numpy as np
import os
import networkx as nx
import pickle
import json
import torch
from openai import OpenAI

# Load environment key
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI()

CACHE_PATH = os.path.join(os.path.dirname(__file__), "cache_gpt_responses.json")

def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return OrderedDict(data)
    return OrderedDict()

MAX_CACHE_SIZE = 50  # You can change this anytime

def save_cache(query, answer):
    cache = load_cache()

    # Move existing query to the end if it exists
    if query in cache:
        del cache[query]

    # Add new entry
    cache[query] = answer

    # Trim to max size
    while len(cache) > MAX_CACHE_SIZE:
        cache.popitem(last=False)  # Removes the oldest entry

    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def find_similar_cached_response(query_text, threshold=0.85):
    cache = load_cache()
    if not cache:
        return None

    cache_queries = list(cache.keys())
    query_embedding = model.encode(query_text, convert_to_tensor=True)
    cache_embeddings = model.encode(cache_queries, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(query_embedding, cache_embeddings)[0]
    best_idx = int(np.argmax(similarities.cpu().numpy()))
    best_score = similarities[best_idx].item()

    if best_score >= threshold:
        print(f"🤝 Fuzzy matched with: '{cache_queries[best_idx]}' (score={best_score:.2f})")
        return cache[cache_queries[best_idx]]

    return None

def detect_answer_length(query: str) -> str:
    query = query.lower()
    if any(kw in query for kw in ["in short", "briefly", "summary", "quickly", "short answer"]):
        return "short"
    elif any(kw in query for kw in ["in detail", "elaborate", "long answer", "full explanation", "explain thoroughly"]):
        return "long"
    else:
        return "normal"

# Load graph
with open(os.path.join(os.path.dirname(__file__), "../data/unified_graph.pkl"), "rb") as f:
    G = pickle.load(f)

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Build documents
node_ids = []
corpus = []

for node_id, attr in G.nodes(data=True):
    text = attr.get("text") or ""
    title = attr.get("title") or ""
    if not isinstance(text, str):
        text = str(text)
    if not isinstance(title, str):
        title = str(title)

    combined = f"{title}. {text}".strip()
    if combined:
        corpus.append(combined)
        node_ids.append(node_id)

corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

@app.route("/api/query", methods=["POST"])
def query():
    try:
        data = request.get_json(force=True)
        print("Received data from frontend:", data)

        query_text = data.get("query", "").strip().lower()
        if not query_text:
            return jsonify({"answer": "Please enter a valid question.", "highlight": []})

        # Encode query and compute similarity
        query_embedding = model.encode(query_text, convert_to_tensor=True)

        # Compute cosine similarities
        similarities = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
        top_idx = int(np.argmax(similarities.cpu().numpy()))
        top_node_id = node_ids[top_idx]
        top_data = G.nodes[top_node_id]
        highlights = [top_node_id]

        # Prepare context: top node + limited neighbors, truncating text
        def format_section(nid):
            data = G.nodes.get(nid, {})
            title = data.get("title", nid)
            text = data.get("text", "")
            return f"{title}:\n{text[:500]}..."  # truncate long texts

        context_sections = [format_section(top_node_id)]
        neighbors = top_data.get("neighbors", {})

        neighbor_limit = 4  # You can increase/decrease this as needed
        neighbor_count = 0

        for rel in ("parent", "siblings", "children"):
            val = neighbors.get(rel)
            if isinstance(val, list):
                for nid in val:
                    if neighbor_count >= neighbor_limit:
                        break
                    context_sections.append(format_section(nid))
                    highlights.append(nid)
                    neighbor_count += 1

        full_context = "\n\n".join(context_sections)

        # 🔍 Try fuzzy match from cache
        cached_answer = find_similar_cached_response(query_text)
        if cached_answer:
            print("⚡ Served from fuzzy cache.")
            return jsonify({
                "answer": cached_answer,
                "highlight": [],
            })

        # Construct AI prompt
        prompt = f"""You are an expert assistant helping explain technical documentation.

Question:
{query_text}

Context:
{full_context}
"""

        length_pref = detect_answer_length(query_text)

        if length_pref == "short":
            max_tokens = 150
            style_note = "Respond briefly and to the point."
        elif length_pref == "long":
            max_tokens = 800
            style_note = "Provide a detailed explanation with examples if needed."
        else:
            max_tokens = 400
            style_note = "Keep your response concise but informative."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Use only the context provided to answer. Be clear and accurate. {style_note}"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=max_tokens
        )
        answer = response.choices[0].message.content.strip()
        save_cache(query_text, answer)

        return jsonify({
            "answer": answer,
            "highlight": highlights,
        })

    except Exception as e:
        print("Error processing query:", e)
        return jsonify({"answer": "Server error occurred.", "highlight": []}), 500

@app.route('/api/graph', methods=['GET'])
def get_graph():
    filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'unified_graph.pkl')
    filepath = os.path.abspath(filepath)

    with open(filepath, "rb") as f:
        data = pickle.load(f)

    graph_data = {
        "nodes": [{"id": str(node)} for node in data.nodes()],
        "links": [{"source": str(u), "target": str(v)} for u, v in data.edges()]
    }
    return jsonify(graph_data)

if __name__ == "__main__":
    app.run(debug=True)
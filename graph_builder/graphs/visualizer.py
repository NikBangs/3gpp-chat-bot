from pyvis.network import Network
import networkx as nx

def format_section_preview(section):
    """
    Format section content (with bullets and title) and show table count or preview.
    """
    if not section:
        return ""

    lines = []

    # Title
    if section.get("title"):
        lines.append(f"<b>{section['title']}</b><br>")

    # Paragraphs (text + bullets)
    for entry in section.get("content", []):
        if entry["type"] == "bullet":
            lines.append(f"• {entry['text']}<br>")
        else:
            lines.append(f"{entry['text']}<br>")

    # Show only first 10 lines
    lines = lines[:10]

    # Table info
    tables = section.get("tables", [])
    if tables:
        lines.append(f"<br><i>{len(tables)} table(s) included</i><br>")

        # Optional: preview first 2 rows of the first table
        preview_rows = tables[0]["rows"][:2]
        table_html = "<table border='1' cellpadding='3' cellspacing='0' style='font-size:12px;'>"
        for row in preview_rows:
            table_html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        table_html += "</table>"

        lines.append(table_html)

    return "".join(lines)

def visualize_semantic_graph(graph: nx.DiGraph, output_html="graph.html", sections10=None, sections17=None):
    net = Network(height="800px", width="100%", bgcolor="#1e1e1e", font_color="white", directed=True)
    net.force_atlas_2based()

    color_map = {
        "added": "#7FFF00",       # light green
        "removed": "#FF4500",     # orange red
        "modified": "#FFD700",    # gold
        "unchanged": "#A9A9A9",   # dark gray
    }

    size_map = {
        "added": 20,
        "removed": 20,
        "modified": 18,
        "unchanged": 10
    }

    for node, attrs in graph.nodes(data=True):
        node_type = attrs.get("type", "unchanged")
        color = color_map.get(node_type, "#CCCCCC")
        size = size_map.get(node_type, 10)

        label = f"{node}\n{node_type.upper()}"

        # Determine source
        section_source = attrs.get("source", "rel10")  # fallback
        rich_section = (sections10 if section_source == "rel10" else sections17).get(node) or (sections10 if section_source == "rel10" else sections17).get(node.strip())
        tooltip_text = format_section_preview(rich_section)

        net.add_node(
            node,
            label=label,
            title=f"<b>{node}</b><br>{node_type}<br>{tooltip_text}",
            color=color,
            size=size,
            shape="dot"
        )

    for src, dst, edge_data in graph.edges(data=True):
        edge_title = edge_data.get("reason", "linked")
        net.add_edge(src, dst, title=edge_title, color="#AAAAAA", arrows="to")

    net.set_options("""
    {
    "nodes": {
        "font": { "size": 16 },
        "borderWidth": 1
    },
    "edges": {
        "smooth": true,
        "arrows": { "to": { "enabled": true, "scaleFactor": 0.5 } },
        "color": { "inherit": true }
    },
    "physics": {
        "forceAtlas2Based": {
        "gravitationalConstant": -50,
        "centralGravity": 0.01,
        "springLength": 100,
        "springConstant": 0.08
        },
        "maxVelocity": 20,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": { "iterations": 150 }
    },
    "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "zoomView": true
    }
    }
    """)

    #net.show_buttons(filter_=["physics"])  # Optional
    net.write_html(output_html)



# # for separate versions
# def export_graph_html(graph: nx.DiGraph, output_html="graph.html", sections=None, height="700px", width="100%"):
#     """
#     Generates an interactive HTML visualization of the graph using pyvis.
#     Optionally enriches node tooltips using the provided sections dictionary.
#     """

#     net = Network(height=height, width=width, directed=True)
#     net.barnes_hut()

#     for node_id, attrs in graph.nodes(data=True):
#         label = attrs.get("title", node_id)
#         tooltip = attrs.get("text", "")

#         # Fallback to external section dict if available
#         if not tooltip and sections and node_id in sections:
#             section = sections[node_id]
#             title = section.get("title", "")
#             content = "\n".join(p.get("text", "") for p in section.get("content", []))
#             tooltip = f"<b>{title}</b><br>{content}" if title else content

#         node_type = attrs.get("type", "")

#         color = {
#             "added": "#A1E3A1",
#             "removed": "#F5A1A1",
#             "modified": "#FFE099",
#             "unchanged": "#D3D3D3",
#             "single": "#B5D5FF",  # new type for single-version graphs
#         }.get(node_type, "#FFFFFF")

#         net.add_node(node_id, label=label[:100], title=tooltip, color=color)

#     for src, dst, edge_attrs in graph.edges(data=True):
#         label = edge_attrs.get("reason", "")
#         net.add_edge(src, dst, label=label)

#     net.set_options("""
#     var options = {
#       "nodes": {
#         "shape": "dot",
#         "size": 16,
#         "font": {
#           "size": 14,
#           "face": "arial"
#         }
#       },
#       "edges": {
#         "arrows": {
#           "to": {
#             "enabled": true
#           }
#         },
#         "smooth": false
#       },
#       "interaction": {
#         "hover": true,
#         "navigationButtons": true
#       },
#       "physics": {
#         "enabled": true,
#         "barnesHut": {
#           "gravitationalConstant": -30000,
#           "centralGravity": 0.3,
#           "springLength": 95
#         },
#         "minVelocity": 0.75
#       }
#     }
#     """)

#     net.show(output_html)
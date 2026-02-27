# mind_map_agent.py

import networkx as nx
from pyvis.network import Network
import os

OUTPUT_DIR = "generated_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_mind_map(data_profile, llm_understanding, brief_analysis=None):
    """
    Creates an interactive mind map showing relationships
    between data, insights, risks, and actions.
    """

    G = nx.Graph()

    # Central node
    G.add_node("Data", label="Uploaded Data", color="#2563eb")

    # ---- Data Structure ----
    if data_profile.get("type") == "tabular":
        G.add_node("Structure", label="Data Structure", color="#10b981")
        G.add_edge("Data", "Structure")

        for col in data_profile.get("column_names", [])[:6]:
            G.add_node(col, label=col, color="#d1fae5")
            G.add_edge("Structure", col)

    else:
        G.add_node("Document", label="Document Content", color="#10b981")
        G.add_edge("Data", "Document")

    # ---- Insights ----
    G.add_node("Insights", label="Key Insights", color="#f59e0b")
    G.add_edge("Data", "Insights")

    for line in llm_understanding.split("\n")[:4]:
        node = f"Insight: {line[:30]}"
        G.add_node(node, label=line[:50], color="#fde68a")
        G.add_edge("Insights", node)

    # ---- Actions ----
    if brief_analysis:
        G.add_node("Actions", label="Recommended Actions", color="#ef4444")
        G.add_edge("Data", "Actions")

        for line in brief_analysis.split("\n"):
            if "action" in line.lower() or "recommend" in line.lower():
                node = f"Action: {line[:30]}"
                G.add_node(node, label=line[:50], color="#fecaca")
                G.add_edge("Actions", node)

    # ---- Render using PyVis ----
    net = Network(height="600px", width="100%", bgcolor="#ffffff")
    net.from_nx(G)

    output_path = os.path.join(OUTPUT_DIR, "data_mind_map.html")
    net.save_graph(output_path)

    return output_path
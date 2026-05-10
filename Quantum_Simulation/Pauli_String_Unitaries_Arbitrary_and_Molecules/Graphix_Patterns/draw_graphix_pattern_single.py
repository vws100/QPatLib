# draw_graphix_pattern_single.py
"""
Minimal drawer for Graphix Pattern -> NetworkX -> Matplotlib.

- **Only input**: `pattern`
- **Styling**: inputs = filled green squares; outputs = open orange circles; others = filled black circles;
  labels on every node (white on dark fills, black on open circles).
- **Layout**: edit `_compute_layout(G)` below if you want a different layout. By default uses spring layout.

Usage
-----
    from draw_graphix_pattern_single import draw_graphix_pattern
    fig, ax = draw_graphix_pattern(pattern)  # shows the plot and returns (fig, ax)

Notes
-----
- Tries `Pattern.extract_graph()` first (Graphix ≥ v0.3.3); falls back to legacy `get_graph()`.
- Uses `pattern.input_nodes` / `pattern.output_nodes` to classify nodes.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

# ------------------------
# EDIT HERE IF YOU WISH
# ------------------------
# Change this function to customize the layout. Keep the signature.
def _compute_layout(G: nx.Graph):
    """Return node positions for drawing.

    Edit this function to switch layout algorithms, e.g.:
        - return nx.kamada_kawai_layout(G)
        - return nx.circular_layout(G)
        - return nx.shell_layout(G)
        - return nx.spectral_layout(G)
        - return nx.random_layout(G, seed=42)
        - return nx.planar_layout(G)  # if graph is planar
        - return nx.spring_layout(G, seed=0)
        - return nx.forceatlas2_layout(G)
        - return nx.bfs_layout(G, 0, store_pos_as="pos")
        - return nx.arf_layout(G) 

    """
    #return nx.kamada_kawai_layout(G)
    return nx.spring_layout(G, seed=0)

# ------------------------
# Internals
# ------------------------

_INPUT_FILL = "tab:red"
_OUTPUT_EDGE = "tab:grey"
_OTHER_FILL = "xkcd:sky blue"
_NODE_SIZE = 20
_EDGE_ALPHA = 0.7


def _get_graph_from_pattern(pattern) -> nx.Graph:
    """Return a NetworkX Graph extracted from a Graphix Pattern.
    Prefers pattern.extract_graph(); falls back to get_graph().
    """
    if hasattr(pattern, "extract_graph"):
        return pattern.extract_graph()
    if hasattr(pattern, "get_graph"):
        nodes, edges = pattern.get_graph()
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G
    raise AttributeError("Pattern does not expose extract_graph() or get_graph().")


def draw_graphix_pattern(pattern):
    """Draw the Graphix pattern. Only argument is the Pattern.

    Returns (fig, ax). Also calls plt.show() for convenience.
    """
    # If available, standardize for consistency (does not change signature)
    if hasattr(pattern, "standardize"):
        pattern.standardize()

    G = _get_graph_from_pattern(pattern)

    inputs = set(getattr(pattern, "input_nodes"))
    outputs = set(getattr(pattern, "output_nodes"))

    inputs_list = [n for n in G.nodes if n in inputs]
    outputs_list = [n for n in G.nodes if n in outputs]
    others_list = [n for n in G.nodes if (n not in inputs) and (n not in outputs)]

    pos = _compute_layout(G)

    fig, ax = plt.subplots(figsize=(6.0, 4.5), dpi=120)

    # Edges
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=_EDGE_ALPHA, width=1.2)

    # Inputs: filled green squares
    if inputs_list:
        nx.draw_networkx_nodes(
            G, pos, nodelist=inputs_list,
            node_shape='s', node_color=_INPUT_FILL,
            edgecolors=_INPUT_FILL, linewidths=1.5, node_size=_NODE_SIZE, ax=ax,
        )

    # Outputs: open orange circles (facecolor='none'; fallback to white)
    if outputs_list:
        try:
            nx.draw_networkx_nodes(
                G, pos, nodelist=outputs_list,
                node_shape='o', node_color='none',
                edgecolors=_OUTPUT_EDGE, linewidths=1.8, node_size=_NODE_SIZE, ax=ax,
            )
        except ValueError:
            nx.draw_networkx_nodes(
                G, pos, nodelist=outputs_list,
                node_shape='o', node_color='white',
                edgecolors=_OUTPUT_EDGE, linewidths=1.8, node_size=_NODE_SIZE, ax=ax,
            )

    # Others: filled black circles
    if others_list:
        nx.draw_networkx_nodes(
            G, pos, nodelist=others_list,
            node_shape='o', node_color=_OTHER_FILL,
            edgecolors=_OTHER_FILL, linewidths=1.0, node_size=_NODE_SIZE, ax=ax,
        )

    # Labels: outputs (bright background) -> black; others/inputs (dark) -> white
    #if outputs_list:
    #    nx.draw_networkx_labels(
    #        G, pos, labels={n: str(n) for n in outputs_list},
    #        font_size=8, font_color='black', ax=ax,
    #    )
    #dark_nodes = inputs_list + others_list
    #if dark_nodes:
    #    nx.draw_networkx_labels(
    #        G, pos, labels={n: str(n) for n in dark_nodes},
    #        font_size=8, font_color='white', ax=ax,
   #     )

    ax.set_axis_off()
    fig.tight_layout()
    plt.show()

    return fig, ax


if __name__ == "__main__":
    print(
        "This module provides draw_graphix_pattern(pattern).\n"
        "Edit _compute_layout(G) to change the layout.\n"
    )

import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
from pkg.db import VPNNetwork, Node, Link

def add_showgraph_subparser(subparsers):
    parser = subparsers.add_parser(
        'showgraph',
        help='Display the network graph of nodes and their connections.'
    )
    parser.add_argument(
        '--output', '-o',
        help='Path to save the generated graph image (e.g., graph.png). If not provided, the graph will be displayed on screen.'
    )
    parser.set_defaults(func=run_showgraph)
    return parser

def run_showgraph(args):
    vpn_net = VPNNetwork()
    nodes = vpn_net.get_nodes()
    links = vpn_net.get_links()

    if not nodes:
        print("No nodes found in the database.", file=sys.stderr)
        sys.exit(1)

    G = nx.Graph()

    for node in nodes:
        G.add_node(node.name)

    for link in links:
        if link.node_a and link.node_b:
            G.add_edge(link.node_a.name, link.node_b.name)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2000,
        node_color='skyblue',
        font_size=15,
        font_weight='bold',
        edge_color='gray'
    )

    if args.output:
        plt.savefig(args.output)
        print(f"[+] Network graph saved to {args.output}")
    else:
        plt.show()
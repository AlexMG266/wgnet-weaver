import os
import sys
from pkg.config_generator import load_nodes, generate_keypair, assign_ips, generate_config_files
from pkg.db import VPNNetwork
from pkg.logger import setup_logger

logger = setup_logger(__name__)

def add_generate_subparser(subparsers):
    parser = subparsers.add_parser(
        'generate',
        help='Generate WireGuard configuration files for all nodes based on a YAML/JSON input.'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to the YAML or JSON file containing node definitions.'
    )
    parser.add_argument(
        '--config-dir', '-d',
        required=False,
        default='~/.wgnet-weaver/netconfigs',
        help='Directory where generated .conf files for each node will be saved.'
    )
    parser.add_argument(
        '--subnet', '-s',
        default='10.10.0.0/16',
        help='Internal subnet range for assigning node IPs. Default: 10.10.0.0/16.'
    )
    parser.set_defaults(func=run_generate)
    return parser

def run_generate(args):
    if not os.path.isfile(args.input):
        print(f"Error: Input file {args.input} does not exist.", file=sys.stderr)
        sys.exit(1)

    nodes = load_nodes(args.input)
    assign_ips(nodes, args.subnet)
    vpn_net = VPNNetwork()
    config_dir = os.path.expanduser(args.config_dir) # ~ -> /home/<user>
    vpn_net.config_path = config_dir
    os.makedirs(config_dir, exist_ok=True)

    # Persistir nodos
    for i, node in enumerate(nodes):
        private_key, public_key = generate_keypair()
        node.private_key = private_key
        node.public_key = public_key
        nodes[i] = vpn_net.add_node(node)

    # Crear links
    for node in nodes:
        peer_names = node.peers if node.peers else [n.name for n in nodes if n.name != node.name]
        for peer_name in peer_names:
            peer_node = next(n for n in nodes if n.name == peer_name)
            vpn_net.add_link(node.id, peer_node.id)

    generate_config_files(nodes, vpn_net.config_path, args.subnet)

    print(f"[+] Configuration files generated in {vpn_net.config_path}")
    print(f"[+] Nodes and links persisted in database: .wgnet-weaver.db")
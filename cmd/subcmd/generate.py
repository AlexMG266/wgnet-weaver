import os
import sys
from pkg.config_generator import load_nodes, generate_keypair, assign_ips, generate_config_files

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
        '--output', '-o',
        required=True,
        help='Directory where generated .conf files for each node will be saved.'
    )
    parser.add_argument(
        '--topology', '-t',
        choices=['full', 'partial'],
        default='full',
        help='Network topology type. Default: full mesh.'
    )
    parser.add_argument(
        '--subnet', '-s',
        default='10.10.0.0/16',
        help='Internal subnet range for assigning node IPs. Default: 10.10.0.0/16.'
    )
    parser.set_defaults(func=run_generate)
    return parser


def run_generate(args):
    # Validate input file
    if not os.path.isfile(args.input):
        print(f"Error: Input file {args.input} does not exist.", file=sys.stderr)
        sys.exit(1)

    nodes = load_nodes(args.input)
    assign_ips(nodes, args.subnet)

    for node in nodes:
        private_key, public_key = generate_keypair()
        node['private_key'] = private_key
        node['public_key'] = public_key

    generate_config_files(nodes, args.output, args.subnet)
    print(f"[+] Configuration files generated in {args.output}")
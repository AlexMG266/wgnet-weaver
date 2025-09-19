import os
import sys

def add_remove_node_subparser(subparsers):
    parser = subparsers.add_parser('removenode', help='Remove a node from the existing configuration.')
    parser.add_argument('--name', '-n', required=True, help='Name of the node to be removed.')
    parser.add_argument('--config-dir', '-c', required=True, help='Directory where the existing configuration files are located.')

    parser.set_defaults(func=run_remove_node)
    return parser

# todo: implement remove_node subcommand
def run_remove_node(args):
    print("Add node functionality is not yet implemented.")
    # Here you would implement the logic to add a new node to the existing configuration.
    # This might involve reading the existing configuration, adding the new node,
    # regenerating keys if necessary, and updating configuration files.
    # For now, we just print the provided arguments.
    print(f"Node Name: {args.name}")
    print(f"Config dir: {args.config_dir}")
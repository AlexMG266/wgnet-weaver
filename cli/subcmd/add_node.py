import os
import sys
from pkg.node import Node

def add_generator_subparser(subparsers):
    parser = subparsers.add_parser('addnode', help='Add a new node to the existing configuration.')
    parser.add_argument('--name', '-n', required=True, help='Name of the new node.')
    parser.add_argument('--public-ip', '-p', required=True, help='Public IP address of the new node.')
    parser.add_argument('--private-ip', '-i', help='Private IP address of the new node (optional).')
    parser.add_argument('--port', '-P', type=int, help='WireGuard port for the new node (optional).')
    parser.add_argument('--allowed-ips', '-a', nargs='*', help='Allowed IPs for the new node (optional).')
    parser.add_argument('--peers', '-r', nargs='*', help='List of peer node names (optional).')

    parser.set_defaults(func=run_add_node)
    return parser

# todo: implement add_node subcommand
def run_add_node(args):
    print("Add node functionality is not yet implemented.")
    # Here you would implement the logic to add a new node to the existing configuration.
    # This might involve reading the existing configuration, adding the new node,
    # regenerating keys if necessary, and updating configuration files.
    # For now, we just print the provided arguments.
    print(f"Node Name: {args.name}")
    print(f"Public IP: {args.public_ip}")
    print(f"Private IP: {args.private_ip}")
    print(f"Port: {args.port}")
    print(f"Allowed IPs: {args.allowed_ips}")
    print(f"Peers: {args.peers}")
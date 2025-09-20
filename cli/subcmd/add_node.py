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
    pass
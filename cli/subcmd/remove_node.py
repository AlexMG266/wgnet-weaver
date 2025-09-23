import os
import sys
from pkg.logger import setup_logger

logger = setup_logger(__name__)

def add_remove_node_subparser(subparsers):
    parser = subparsers.add_parser('removenode', help='Remove a node from the existing configuration.')
    parser.add_argument('--name', '-n', required=True, help='Name of the node to be removed.')
    parser.add_argument('--config-dir', '-d', required=True, help='Directory where the existing configuration files are located.')

    parser.set_defaults(func=run_remove_node)
    return parser

# todo: implement remove_node subcommand
def run_remove_node(args):
    pass
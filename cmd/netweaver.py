#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: alex-mosquera-gundin <alex.mosquera@udc.es>

import argparse
from cmd.subcmd import generate, add_node, remove_node
from pkg.__version__ import __version__

# usage:
# python3 -m cmd.netweaver generate --input [nodes.yaml/json] --output ./configs (directory)

def main():
    parser = argparse.ArgumentParser(
        description='NetWeaver CLI Tool for managing WireGuard mesh networks',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--version', action='version', version=f'NetWeaver {__version__}')
    subparsers = parser.add_subparsers(dest='command', required=True)

    generate.add_generate_subparser(subparsers)
    add_node.add_generator_subparser(subparsers)
    remove_node.add_remove_node_subparser(subparsers)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
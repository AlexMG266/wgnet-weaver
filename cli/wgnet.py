#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: AlexMG266 <alex.mosquera@udc.es>

import argparse
from pkg.__version__ import __version__
from cli.subcmd import generate, destroy, add_node, remove_node, showgraph, deploy
from pkg.paths import init_directories

def main():

    init_directories()

    parser = argparse.ArgumentParser(
        description='NetWeaver CLI Tool for managing WireGuard mesh networks',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--version', action='version', version=f'NetWeaver {__version__}')
    subparsers = parser.add_subparsers(dest='command', required=True)

    generate.add_generate_subparser(subparsers)
    add_node.add_generator_subparser(subparsers)
    remove_node.add_remove_node_subparser(subparsers)
    showgraph.add_showgraph_subparser(subparsers)
    # destroy.add_destroy_subparser(subparsers) not yet tested
    deploy.add_deploy_subparser(subparsers)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
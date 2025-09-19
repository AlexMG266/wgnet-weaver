#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: alex-mosquera-gundin <alex.mosquera@udc.es>

import argparse
from cmd.subcmd.generate import add_generate_subparser
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
    add_generate_subparser(subparsers)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
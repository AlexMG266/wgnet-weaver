import os
import sys
from pkg.logger import setup_logger

logger = setup_logger(__name__)

def add_destroy_subparser(subparsers):
    parser = subparsers.add_parser('destroy', help='Destroy the existing VPN network and remove all associated configuration files and database entries.')
    parser.add_argument('--config-dir', '-c', default='/tmp/wgnet-configs', required=True, help='Directory where the existing configuration files are located.')
    parser.add_argument('--db-path', '-d', default='.wgnet-weaver.db', help='Path to the SQLite database file. Default: .wgnet-weaver.db')
    parser.set_defaults(func=run_destroy)
    return parser

# todo: implement destroy
def run_destroy(args):
    pass
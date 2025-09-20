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

def run_destroy(args):
    config_dir = args.config_dir
    db_path = args.db_path

    # Remove configuration files
    if os.path.isdir(config_dir):
        for filename in os.listdir(config_dir):
            file_path = os.path.join(config_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"[+] Removed configuration file: {file_path}")
            except Exception as e:
                print(f"Error removing file {file_path}: {e}", file=sys.stderr)
        try:
            os.rmdir(config_dir)
            print(f"[+] Removed configuration directory: {config_dir}")
        except OSError as e:
            print(f"Error removing directory {config_dir}: {e}", file=sys.stderr)
    else:
        print(f"Configuration directory {config_dir} does not exist.", file=sys.stderr)

    # Clear database
    if os.path.isfile(db_path):
        try:
            os.remove(db_path)
            print(f"[+] Removed database file: {db_path}")
        except Exception as e:
            print(f"Error removing database file {db_path}: {e}", file=sys.stderr)
    else:
        print(f"Database file {db_path} does not exist.", file=sys.stderr)
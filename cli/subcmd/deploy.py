import os
import sys
import subprocess
from pkg.logger import setup_logger

logger = setup_logger(__name__)

def add_deploy_subparser(subparsers):
    parser = subparsers.add_parser(
        'deploy',
        help='Deploy WireGuard configuration files to the respective nodes using Ansible.'
    )
    parser.add_argument(
        '--config-dir', '-d',
        required=True,
        help='Directory where the generated .conf files for each node are located.'
    )
    parser.add_argument(
        '--inventory', '-i',
        required=True,
        help='Path to the Ansible inventory file (YAML/INI) describing the nodes.'
    )
    parser.add_argument(
        '--playbook', '-p',
        default='ansible/deploy.yml',
        help='Path to the Ansible playbook. Default: ansible/deploy.yml'
    )
    parser.add_argument(
        '--user', '-u',
        required=True,
        help='SSH username for connecting to the nodes.'
    )
    parser.add_argument(
        '--key', '-k',
        help='Path to the SSH private key for authentication.'
    )
    parser.set_defaults(func=run_deploy)
    return parser

def run_deploy(args):
    config_dir = os.path.expanduser(args.config_dir)
    if not os.path.exists(config_dir):
        print(f"Error: Configuration directory {config_dir} does not exist.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(config_dir):
        print(f"Error: {config_dir} is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Cargar el playhook de Ansible
    playbook_path = os.path.join(os.path.dirname(__file__), "../../ansible/deploy.yml")
    if not os.path.isfile(playbook_path):
        print(f"Error: Ansible playbook {playbook_path} not found.", file=sys.stderr)
        sys.exit(1)

    cmd = [
        'ansible-playbook',
        '-i', args.inventory,
        playbook_path,
        '--extra-vars', f'config_dir={config_dir} ansible_user={args.user}'
    ]

    if args.key:
        cmd.extend(['--private-key', args.key])

    try:
        subprocess.run(cmd, check=True)
        print("[+] Deployment completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Deployment failed: {e}", file=sys.stderr)
        sys.exit(1)
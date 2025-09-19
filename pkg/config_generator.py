import os
import json
from jsonschema import validate, ValidationError
from pathlib import Path
import subprocess, ipaddress
from pkg.node import Node

NODE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "public_ip": {"type": "string"},
        "port": {"type": "integer"},
        "allowed_ips": {"type": "array", "items": {"type": "string"}},
        "private_ip": {"type": "string"}
    },
    "required": ["name", "public_ip"],
    "additionalProperties": False
}

SCHEMA = {
    "type": "object",
    "properties": {
        "nodes": {
            "type": "array",
            "items": NODE_SCHEMA,
            "minItems": 1
        }
    },
    "required": ["nodes"]
}

def validate_nodes(data: dict):
    try:
        validate(instance=data, schema=SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Invalid JSON structure: {e.message}")

def load_nodes(input_file):
    file_path = Path(input_file)
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist")

    with open(file_path, "r") as f:
        if file_path.suffix == ".json":
            data = json.load(f)
            validate_nodes(data)
            return [Node(**node) for node in data['nodes']]
        else:
            raise ValueError("Unsupported file type. Use .json")

def generate_keypair():
    private_key = subprocess.check_output(['wg', 'genkey']).strip().decode('utf-8')
    public_key = subprocess.check_output(['wg', 'pubkey'], input=private_key.encode('utf-8')).strip().decode('utf-8')
    return private_key, public_key

def assign_ips(nodes, subnet):
    subnet_obj = ipaddress.ip_network(subnet)
    used_ips = set()

    # Revisar IPs predefinidas
    for node in nodes:
        if node.ip:
            ip_obj = ipaddress.ip_interface(node.ip)
            if ip_obj.ip not in subnet_obj:
                raise ValueError(f"Private IP {ip_obj} of node {node.name} is outside {subnet}")
            if ip_obj.ip in used_ips:
                raise ValueError(f"Duplicate private IP {ip_obj} detected in node {node.name}")
            node.ip = str(ip_obj)
            used_ips.add(ip_obj.ip)

    available_ips = (ip for ip in subnet_obj.hosts() if ip not in used_ips)

    for node in nodes:
        if not node.ip:
            try:
                next_ip = next(available_ips)
            except StopIteration:
                raise ValueError("Not enough IPs available in subnet")
            node.ip = f"{next_ip}/24"
            used_ips.add(next_ip)

# inside output_dir, for all node, create a directory with his name and inside a wg0.conf file
# full mesh topology by default (todo: partial mesh)
def generate_config_files(nodes, output_dir, subnet):
    os.makedirs(output_dir, exist_ok=True)
    for node in nodes:
        node_dir = os.path.join(output_dir, node.name)
        os.makedirs(node_dir, exist_ok=True)
        config_path = os.path.join(node_dir, 'wg0.conf')
        with open(config_path, 'w') as f:
            f.write(f"[Interface]\n")
            f.write(f"PrivateKey = {node.private_key}\n")
            f.write(f"Address = {node.ip}\n")
            f.write(f"ListenPort = {node.port or 51820}\n\n")

            for peer in nodes:
                if peer.name != node.name:
                    f.write(f"[Peer]\n")
                    f.write(f"PublicKey = {peer.public_key}\n")
                    # Allowed IPs
                    if peer.allowed_ips:
                        for allowed_ip in peer.allowed_ips:
                            f.write(f"AllowedIPs = {allowed_ip}\n")
                    else:
                        f.write(f"AllowedIPs = {subnet}\n")
                    f.write(f"Endpoint = {peer.public_ip}:{peer.port or 51820}\n\n")
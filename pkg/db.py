import sqlite3
import json
from pathlib import Path
from pkg.node import Node
from pkg.link import Link

DB_FILE = Path.home() / '.wgnet-weaver.db'

class VPNNetwork:
    def __init__(self, db_path=DB_FILE):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL DEFAULT 'node',  -- nuevo campo type
            public_ip TEXT NOT NULL,
            private_ip TEXT,
            allowed_ips TEXT,
            port INTEGER DEFAULT 51820
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_a INTEGER NOT NULL,
            node_b INTEGER NOT NULL,
            UNIQUE(node_a, node_b),
            FOREIGN KEY(node_a) REFERENCES nodes(id),
            FOREIGN KEY(node_b) REFERENCES nodes(id)
        )
        """)
        self.conn.commit()

    def add_node(self, node: Node):
        cur = self.conn.cursor()
        cur.execute("""
        INSERT OR IGNORE INTO nodes (name, type, public_ip, private_ip, port)
        VALUES (?, ?, ?, ?, ?)
        """, (node.name, node.type, node.public_ip, node.ip, node.port))
        self.conn.commit()

        cur.execute("SELECT id FROM nodes WHERE name=?", (node.name,))
        node.id = cur.fetchone()[0]
        return node

    def get_nodes(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, type, public_ip, private_ip, port FROM nodes")
        rows = cur.fetchall()
        return [
            Node(name=r[1], type=r[2], public_ip=r[3], private_ip=r[4], port=r[5])
            for r in rows
        ]

    def get_node_by_id(self, node_id):
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, type, public_ip, private_ip, port FROM nodes WHERE id=?", (node_id,))
        row = cur.fetchone()
        if row:
            return Node(name=row[1], type=row[2], public_ip=row[3], private_ip=row[4], port=row[5])
        return None

    def add_link(self, node_a_id, node_b_id):
        # Garantizar orden para evitar duplicados (bidireccional)
        a, b = sorted([node_a_id, node_b_id])
        cur = self.conn.cursor()
        cur.execute("""
        INSERT OR IGNORE INTO links (node_a, node_b)
        VALUES (?, ?)
        """, (a, b))
        self.conn.commit()


    def get_links(self, node_id=None):
        cur = self.conn.cursor()
        if node_id:
            cur.execute("""
            SELECT node_a, node_b FROM links
            WHERE node_a=? OR node_b=?
            """, (node_id, node_id))
        else:
            cur.execute("SELECT node_a, node_b FROM links")

        rows = cur.fetchall()
        cur.execute("SELECT id, name, type, public_ip, private_ip, port FROM nodes")
        node_map = {
            r[0]: Node(
                name=r[1],
                type=r[2],
                public_ip=r[3],
                private_ip=r[4],
                port=r[5]
            )
            for r in cur.fetchall()
        }


        links = []
        for a_id, b_id in rows:
            node_a = node_map.get(a_id)
            node_b = node_map.get(b_id)
            if node_a and node_b:
                links.append(Link(node_a, node_b))

        return links


    def load_from_json(self, json_file: str):
        file_path = Path(json_file)
        if not file_path.exists():
            raise FileNotFoundError(f"{json_file} does not exist")
        with open(file_path, "r") as f:
            data = json.load(f)
        # Crear nodos
        nodes = []
        for n in data["nodes"]:
            node = Node(**n)
            self.add_node(node)
            nodes.append(node)
        # Crear enlaces
        for i, node_i in enumerate(self.get_nodes()):
            for j, node_j in enumerate(self.get_nodes()):
                if i < j:  # full mesh
                    self.add_link(node_i.id, node_j.id)
        return nodes

    def close(self):
        self.conn.close()
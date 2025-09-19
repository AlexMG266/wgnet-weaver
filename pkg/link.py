from pkg.node import Node

class Link:
    def __init__(self, node_a: Node, node_b: Node):
        self._node_a = node_a
        self._node_b = node_b

    def __repr__(self):
        return f"Link({self.node_a.name} <-> {self.node_b.name}, status={self.status})"

    @property
    def node_a(self):
        return self._node_a

    @node_a.setter
    def node_a(self, value):
        self._node_a = value

    @property
    def node_b(self):
        return self._node_b

    @node_b.setter
    def node_b(self, value):
        self._node_b = value
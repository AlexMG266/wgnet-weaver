class Node:
    def __init__(self, name, type, public_ip, private_ip=None, port=51820, allowed_ips=None, peers=None, id=None):
        self._id = id
        self._type = type
        self._name = name
        self._public_ip = public_ip
        self.ip = private_ip
        self._port = port
        self._allowed_ips = allowed_ips or []
        self._peers = peers # if none, full mesh in that node

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def type(self):
        return self._type

    @property
    def public_ip(self):
        return self._public_ip

    @public_ip.setter
    def public_ip(self, value):
        self._public_ip = value

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self._ip = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def allowed_ips(self):
        return self._allowed_ips

    def add_allowed_ip(self, ip):
        if ip not in self._allowed_ips:
            self._allowed_ips.append(ip)

    def add_allowed_ips(self, ips):
        for ip in ips:
            self.add_allowed_ip(ip)

    def remove_allowed_ip(self, ip):
        if ip in self._allowed_ips:
            self._allowed_ips.remove(ip)

    def clear_allowed_ips(self):
        self._allowed_ips = []

    @property
    def peers(self):
        return self._peers

    def to_dict(self):
        return {
            "name": self._name,
            "public_ip": self._public_ip,
            "private_ip": self._private_ip,
            "port": self._port,
            "allowed_ips": self._allowed_ips
        }

    def __repr__(self):
        return f"Node(name={self._name}, public_ip={self._public_ip})"

import ipaddress
from dataclasses import dataclass, field
from typing import List


@dataclass
class Switch:
    name: str
    tier: str                                          # "core", "dist", or "access"
    priority: int = 32768
    uplink_ports: List[str] = field(default_factory=list)
    host_ports: List[str] = field(default_factory=list)


@dataclass
class Uplink:
    src: str
    dst: str


@dataclass
class VLANSegment:
    vlan_id: int
    name: str
    subnet: str                                        # CIDR e.g. "10.0.2.0/24"
    purpose: str                                       # "management", "voice", or "data"
    access_switch_index: int = 0
    x: float = 0
    y: float = 0

    def gateway_ip(self):
        # Returns the first usable host IP as the gateway
        net = ipaddress.ip_network(self.subnet, strict=False)
        return str(list(net.hosts())[0])

    def netmask(self):
        net = ipaddress.ip_network(self.subnet, strict=False)
        return str(net.netmask)


@dataclass
class Topology:
    switches: List[Switch]
    uplinks: List[Uplink]
    segments: List[VLANSegment]
    configs: dict
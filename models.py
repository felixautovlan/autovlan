from dataclasses import dataclass
from typing import List


@dataclass
class Switch:
    name: str
    tier: str
    priority: int = 32768
    uplink_ports: List[str] = None
    host_ports: List[str] = None


@dataclass
class Uplink:
    src: str
    dst: str


@dataclass
class VLANSegment:
    vlan_id: int
    name: str
    subnet: str
    purpose: str
    access_switch_index: int = 0
    x: float = 0
    y: float = 0

    def gateway_ip(self):
        return self.subnet.replace('0/25')[1]

    def netmask(self):
        return "255.255.255.0"


@dataclass
class Topology:
    switches: List[Switch]
    uplinks: List[Uplink]
    segments: List[VLANSegment]
    configs: dict
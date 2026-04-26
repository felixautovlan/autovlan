import math
from models import Switch, Uplink, Topology
from vlan_allocator import VLANAllocator
from topology_validator import TopologyValidator


class TopologyEngine:

    def __init__(self):
        self.segment_planner = VLANAllocator()
        self.validator = TopologyValidator()

    def design(self, total_nodes):

        n_access = math.ceil(total_nodes / 24)
        n_dist = max(2, math.ceil(n_access / 10))

        core = [Switch("CORE-1", "core"), Switch("CORE-2", "core")]

        dist = [Switch(f"DIST-{i+1}", "dist") for i in range(n_dist)]
        access = [Switch(f"ACC-{i+1}", "access") for i in range(n_access)]

        uplinks = []

        for d in dist:
            uplinks.append(Uplink("CORE-1", d.name))
            uplinks.append(Uplink("CORE-2", d.name))

        for i, a in enumerate(access):
            uplinks.append(Uplink(a.name, dist[i % n_dist].name))

        segments = self.allocator.allocate(n_access, "10.0.0.0/8", "AUTO")

        topo = Topology(core + dist + access, uplinks, segments, {})

        self.validator.validate(topo)

        return topo
import math
from models import Switch, Uplink, Topology
from vlan_allocator import NetworkSegmentPlanner
from topology_validator import TopologyValidator


class TopologyEngine:

    def __init__(self):
        self.segment_planner = NetworkSegmentPlanner()
        self.validator       = TopologyValidator()

    def design(self, total_nodes: int, name_prefix: str = "AUTO") -> Topology:
        """
        Build a 3-tier topology (core -> dist -> access) for the given device count.
        Each access switch supports up to 24 hosts; each dist switch handles up to 10 access switches.
        """
        n_access = math.ceil(total_nodes / 24)
        n_dist   = max(2, math.ceil(n_access / 10))  # Minimum 2 for redundancy

        core   = [Switch("CORE-1", "core"), Switch("CORE-2", "core")]
        dist   = [Switch(f"DIST-{i + 1}", "dist")   for i in range(n_dist)]
        access = [Switch(f"ACC-{i + 1}",  "access") for i in range(n_access)]

        uplinks = []

        # Every dist switch dual-homes to both core switches
        for d in dist:
            uplinks.append(Uplink("CORE-1", d.name))
            uplinks.append(Uplink("CORE-2", d.name))

        # Access switches connect to dist switches in round-robin order
        for i, a in enumerate(access):
            uplinks.append(Uplink(a.name, dist[i % n_dist].name))

        segments = self.segment_planner.allocate(n_access, "10.0.0.0/8", name_prefix)

        topo = Topology(core + dist + access, uplinks, segments, {})
        self.validator.validate(topo)

        return topo

    def summarize(self, topo: Topology) -> None:
        by_tier = {"core": [], "dist": [], "access": []}
        for s in topo.switches:
            if s.tier in by_tier:
                by_tier[s.tier].append(s)

        tier_labels = {
            "core":   "Core switches",
            "dist":   "Distribution switches",
            "access": "Access switches",
        }

        print("\n NETWORK SUMMARY")
        print("─" * 30)
        for tier, label in tier_labels.items():
            print(f"  {label}: {len(by_tier[tier])}")
        print("─" * 30)
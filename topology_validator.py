import networkx as nx
from models import Topology


class TopologyValidator:

    def validate(self, topo: Topology):

        self._check_vlan_uniqueness(topo)
        self._check_reachability(topo)

    def _check_vlan_uniqueness(self, topo):
        ids = [s.vlan_id for s in topo.segments]
        if len(ids) != len(set(ids)):
            raise Exception("Duplicate VLAN IDs")

    def _check_reachability(self, topo):
        G = nx.Graph()

        for sw in topo.switches:
            G.add_node(sw.name)

        for u in topo.uplinks:
            G.add_edge(u.src, u.dst)

        for sw in topo.switches:
            if not nx.has_path(G, topo.switches[0].name, sw.name):
                raise Exception(f"{sw.name} unreachable")
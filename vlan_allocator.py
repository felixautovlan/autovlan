import ipaddress
from typing import List
from models import VLANSegment


class NetworkSegmentPlanner:

    RESERVED_VLANS = {1, 4030, 4040, 4050, 4060}
    MGMT_VLAN_ID = 4
    VOICE_VLAN_ID = 8
    FIRST_DATA_VLAN = 15

    def allocate(self, n_access: int, supernet: str, name_prefix: str) -> List[VLANSegment]:

        net = ipaddress.ip_network(supernet, strict=False)
        subnets = list(net.subnets(new_prefix=24))

        if len(subnets) < n_access + 2:
            raise ValueError("Supernet too small")

        segments = []

        # Infrastructure VLANs
        segments.append(VLANSegment(self.MGMT_VLAN_ID, "MGMT", str(subnets[0]), "management"))
        segments.append(VLANSegment(self.VOICE_VLAN_ID, "VOICE", str(subnets[1]), "voice"))

        # Data VLANs
        for i in range(n_access):
            vlan_id = self.FIRST_DATA_VLAN + i

            if vlan_id in self.RESERVED_VLANS:
                vlan_id += 1

            segments.append(VLANSegment(
                vlan_id,
                f"{name_prefix}-DATA-{i+1}",
                str(subnets[i + 2]),
                "data",
                i
            ))

        return segments
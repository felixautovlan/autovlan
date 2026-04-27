from models import Topology, Switch


class ConfigGenerator:
    """Generates switch CLI config from a Topology. Override _build_config() for vendor-specific syntax."""

    def generate(self, topo: Topology) -> dict:
        """Returns a dict mapping switch name -> config string."""
        configs = {}
        for switch in topo.switches:
            configs[switch.name] = self._build_config(switch, topo)
        return configs

    def _build_config(self, switch: Switch, topo: Topology) -> str:
        lines = [f"! Config for {switch.name} (tier: {switch.tier})"]

        for segment in topo.segments:
            lines.append(f"vlan {segment.vlan_id}")
            lines.append(f"  name {segment.name}")
            if switch.tier in ("core", "dist"):
                lines.append(f"  ! Gateway: {segment.gateway_ip()} / {segment.netmask()}")

        return "\n".join(lines)
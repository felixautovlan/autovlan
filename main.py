from topology_engine import TopologyEngine


def get_input() -> tuple[int, str]:
    print("\n>>> AUTO VLAN DESIGN SYSTEM >>>\n")
    nodes  = int(input("  Enter number of devices : "))
    prefix = input("  Enter VLAN name prefix   : ")
    return nodes, prefix


def display_results(topo) -> None:
    # Summary header
    print("\n" + "─" * 35)
    print("NETWORK BUILT SUCCESSFULLY")
    print("─" * 35)
    print(f"  Switches : {len(topo.switches)}")
    print(f"  VLANs    : {len(topo.segments)}")
    print(f"  Uplinks  : {len(topo.uplinks)}")
    print("─" * 35)

    # Per-VLAN breakdown with aligned columns
    print("\n  VLAN BREAKDOWN\n")
    for v in topo.segments:
        print(f"  [{v.vlan_id:>4}]  {v.name:<20}  {v.subnet:<18}  GW: {v.gateway_ip()}")


def main() -> None:
    print("\n=====================================")
    print("  AUTO VLAN DESIGN SYSTEM BY FELIX  ")
    print("=====================================")
    nodes, prefix = get_input()

    engine = TopologyEngine()
    topo   = engine.design(nodes, prefix)

    engine.summarize(topo)
    display_results(topo)


if __name__ == "__main__":
    main()
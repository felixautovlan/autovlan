from topology_engine import TopologyEngine

def get_user_input():
    nodes = int(input("Enter number of devices: "))
    prefix = input("Enter VLAN name prefix: ")
    return nodes, prefix


def main():
    print("=== AUTO VLAN DESIGN SYSTEM ===")

    nodes, prefix = get_user_input()

    engine = TopologyEngine()
    topo = engine.design(nodes)

    print("\n NETWORK CREATED SUCCESSFULLY")
    print("Total Switches:", len(topo.switches))
    print("Total VLANs:", len(topo.segments))

    print("\n VLAN DETAILS:")
    for v in topo.segments:
        print(f"VLAN {v.vlan_id} | {v.name} | {v.subnet}")


if __name__ == "__main__":
    main()
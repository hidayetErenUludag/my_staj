import networkx as nx

railway = nx.DiGraph()

railway.add_edge("L11M", "L12M", weight=0.1)
railway.add_edge("L11M", "L14M", weight=0.2)
railway.add_edge("L14M", "L11M", weight=0.2)
railway.add_edge("L12M", "L15M", weight=0.4)
railway.add_edge("L13M", "L12M", weight=0.2)
railway.add_edge("L12M", "L13M", weight=0.2)
railway.add_edge("L14M", "L13M", weight=0.1)
railway.add_edge("L15M", "L16M", weight=0.1)
railway.add_edge("L15M", "L18M", weight=0.2)
railway.add_edge("L18M", "L15M", weight=0.2)
railway.add_edge("L18M", "L15M", weight=0.2)

railway.add_edge("L16M", "L17M", weight=0.2)
railway.add_edge("L16M", "L19M", weight=0.4)
railway.add_edge("L17M", "L16M", weight=0.2)
railway.add_edge("L18M", "L15M", weight=0.2)
railway.add_edge("L17M", "L14M", weight=0.4)
railway.add_edge("L18M", "L17M", weight=0.1)

railway.add_edge("L19M", "L20M", weight=0.1)
railway.add_edge("L19M", "L22M", weight=0.2)
railway.add_edge("L20M", "L23M", weight=0.4)
railway.add_edge("L20M", "L21M", weight=0.2)
railway.add_edge("L21M", "L20M", weight=0.2)
railway.add_edge("L21M", "L18M", weight=0.4)
railway.add_edge("L22M", "L19M", weight=0.2)
railway.add_edge("L22M", "L21M", weight=0.1)

railway.add_edge("L23M", "L24M", weight=0.1)
railway.add_edge("L23M", "L26M", weight=0.2)
railway.add_edge("L24M", "L25M", weight=0.2)
railway.add_edge("L25M", "L24M", weight=0.2)
railway.add_edge("L25M", "L22M", weight=0.4)
railway.add_edge("L26M", "L23M", weight=0.2)
railway.add_edge("L26M", "L25M", weight=0.1)

def find_shortest(start, finish):
    path = nx.shortest_path(railway, start, finish, "weight")
    return path

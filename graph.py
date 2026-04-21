import networkx as nx

def build_graph(parsed):
    functions = parsed["functions"]
    calls = parsed["calls"]

    G = nx.DiGraph()

    # Add nodes
    for func in functions:
        G.add_node(func)

    # Add edges
    for caller, callee in calls:
        if caller in functions and callee in functions:
            G.add_edge(caller, callee)

    return G
def prod(iter, *, start=1, cast=int):
    """This version of product made to cast numpy types to python types so we don't have to worry about overflows.
    """
    m = start
    for i in iter:
        m *= cast(i)
    return m

class adict(dict):
    """A dictionary that allows one to use keys as if they were attributes.
    """
    def __getattr__(self, key):
        return self[key]

def matching(items):
    import networkx as nx
    G = nx.from_dict_of_lists(items)
    return tuple((k, v) for k, v in nx.bipartite.maximum_matching(G, top_nodes=items).items() if k in items)

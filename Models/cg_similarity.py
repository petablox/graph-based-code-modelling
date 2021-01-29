import gzip 
import networkx as nx
import pickle as pkl
from tqdm import tqdm

#ten_file = "small-project/tensorised/chunk_0000.pkl.gz"
test_ten_file = "data/tensorised-clean-test-new/chunk_0000.pkl.gz"
train_ten_file = "data/tensorised-ip-clean-new/chunk_0000.pkl.gz"


def get_graphs(ten_file):
    with gzip.open(ten_file) as f:
        data = pkl.load(f)

    graphs = []
    for item in tqdm(data):
        g = nx.Graph()
        token_ids = item["cg_node_label_token_ids"]
        types = item["cg_node_type_labels"]
        
        if len(token_ids) > 500: continue
        for idx, (_id, _type) in enumerate(zip(token_ids, types)):
            g.add_nodes_from([(idx, {"token_id": _id, "types": _type.tolist()})])
            #g.add_nodes_from([(idx, {"token_id": _id})])

        edges = item["cg_edges"]
        for idx, edge_type in enumerate(edges):
            for (a, b) in edge_type.tolist():
                g.add_edges_from([(a, b, {"type": idx})])
        
        #print(len(g.nodes))
        graphs.append((g, item))

    return graphs

test_graphs = get_graphs(test_ten_file)
train_graphs = get_graphs(train_ten_file)


#node_match=lambda n1, n2: n1["token_id"] == n2["token_id"] and n1["types"] == n2["types"]
#node_match=lambda n1, n2: n1["token_id"] == n2["token_id"]
node_match=lambda n1, n2: n1 == n2
edge_match=lambda e1, e2: e1["type"] == e2["type"]

#print(nx.graph_edit_distance(graphs[0], graphs[1]))
output = []
print(len(train_graphs), len(test_graphs))

for graph, elem in train_graphs:
    if len(graph.nodes) > 500: continue
    print("Train graph is size:", len(graph.nodes))

    for graph2, elem2 in tqdm(test_graphs):
        if len(graph2.nodes) > 500: continue

        edit_distance = nx.graph_edit_distance(graph, graph2, node_match, edge_match, timeout=10)
        if not edit_distance: continue

        print("(train: %s %s, test: %s %s), %.2f"% (elem["fname"], elem["og_expr"], elem2["fname"], elem2["og_expr"], edit_distance))
        output.append({
                        "fname1": elem["fname"], 
                        "fname2": elem2["fname"], 
                        "expr1": elem["og_expr"], 
                        "expr2": elem["og_expr"], 
                        "edit_distance": edit_distance
                       })

edit_sort = lambda elem: elem[2]
output.sort(key=edit_sort)
for (idx, idx2, edit_distance) in reversed(output):
    print("(%d, %d), %.2f"% (idx, idx2, edit_distance))

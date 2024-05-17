class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, node1, node2, weight):
        self.add_node(node1)
        self.add_node(node2)
        self.edges.setdefault(node1, {})[node2] = weight
        self.edges.setdefault(node2, {})[node1] = weight

    def get_weight(self, node1, node2):
        return self.edges.get(node1, {}).get(node2, float('inf'))
        
    def construct_complete_graph(self, num_nodes, min_weight=1, max_weight=20):
        # Add nodes to the graph
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                # Generate a random weight between min_weight and max_weight for each edge
                weight = random.randint(min_weight, max_weight)
                self.add_edge(str(i), str(j), weight)

# Example usage:
if __name__ == "__main__":
    # Generate graphs
    graph_5_nodes = generate_random_graph(5)
    graph_15_nodes = generate_random_graph(15)
    graph_30_nodes = generate_complex_graph(30)



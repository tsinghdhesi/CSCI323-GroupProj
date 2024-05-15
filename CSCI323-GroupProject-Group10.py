class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, node1, node2, weight):
        self.add_node(node1)
        self.add_node(node2)
        self.edges[(node1, node2)] = weight
        self.edges[(node2, node1)] = weight

    def get_weight(self, node1, node2):
        return self.edges.get((node1, node2), float('inf'))

    def __str__(self):
        return f"Nodes: {self.nodes}\nEdges: {self.edges}"
        
def generate_random_graph(num_nodes):
    graph = Graph()
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = random.randint(1, 20)  # Random weight between 1 and 20
            graph.add_edge(str(i), str(j), weight)
    return graph

# Function to generate a complex graph with cycles
def generate_complex_graph(num_nodes):
    graph = Graph()
    for i in range(num_nodes):
        for j in range(i + 1, min(i + 4, num_nodes)):
            weight = random.randint(1, 20)  # Random weight between 1 and 20
            graph.add_edge(str(i), str(j), weight)
    return graph

# Example usage:
if __name__ == "__main__":
    # Generate graphs
    graph_5_nodes = generate_random_graph(5)
    graph_15_nodes = generate_random_graph(15)
    graph_30_nodes = generate_complex_graph(30)



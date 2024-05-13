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


# Example usage:
if __name__ == "__main__":
    graph = Graph()
    graph.add_edge('A', 'B', 5)
    graph.add_edge('B', 'C', 3)
    graph.add_edge('C', 'D', 7)
    graph.add_edge('D', 'A', 2)

    print(graph)
    print("Weight between A and B:", graph.get_weight('A', 'B'))

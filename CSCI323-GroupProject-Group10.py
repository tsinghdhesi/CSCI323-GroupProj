import random
import heapq


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
    
    def get_neighbors(self, node):
        # Return the neighbors of the given node
        return list(self.edges.get(node, {}).keys())

    def dijkstra_shortest_path(self, source, destination):
        # Initialize distances to all nodes as infinity
        distances = {node: float('inf') for node in self.nodes}
        distances[source] = 0
        # Priority queue to store nodes with their current distances
        priority_queue = [(0, source)]
        # Previous node dictionary to reconstruct the path
        previous = {}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            # If the current distance is greater than the known distance, skip
            if current_distance > distances[current_node]:
                continue

            # Visit neighbors of the current node
            for neighbor, edge_weight in self.edges.get(current_node, {}).items():
                distance = current_distance + edge_weight
                # Update the distance if it's shorter than the known distance
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        # Reconstruct the path from source to destination
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous.get(current)
        path.reverse()  # Reverse the path to get it from source to destination

        return path
    
    def generate_random_graph(self, num_nodes, min_weight=1, max_weight=20):
        # Add nodes to the graph
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                # Generate a random weight between min_weight and max_weight for each edge
                weight = random.randint(min_weight, max_weight)
                self.add_edge(str(i), str(j), weight)
    
    def nearest_neighbor_tsp(self, start_node): # Time Complexity: O(n^2), Space Complexity O(n)
        # Initialize variables
        unvisited_nodes = set(self.nodes)
        current_node = start_node
        tsp_tour = [current_node]
        unvisited_nodes.remove(current_node)

        # Loop until all nodes are visited
        while unvisited_nodes:
            # Find nearest neighbor
            neighbours = set(self.get_neighbors(current_node))
            unvisited_neighbours = unvisited_nodes.intersection(neighbours)
            if len(unvisited_neighbours) == 0:
                nearest_neighbor = min(neighbours, key=lambda x: self.get_weight(current_node, x))
            else:
                nearest_neighbor = min(unvisited_neighbours, key=lambda x: self.get_weight(current_node, x))
                unvisited_nodes.remove(nearest_neighbor)
            
            tsp_tour.append(nearest_neighbor)
            current_node = nearest_neighbor
        # Add the edge back to the starting node to complete the tour
        #tsp_tour.append(start_node)
        path_back = self.dijkstra_shortest_path(tsp_tour[-1], start_node)
        path_back.remove(tsp_tour[-1])
        tsp_tour.extend(path_back)
        return tsp_tour
    
    def held_karp_tsp(self): #space complexity: O(n^2 * 2^n), time complexity: O(n^2 * 2^n)
        n = len(self.nodes)
        nodes = list(self.nodes)
        memo = {}
        parent = {}

        def dp(mask, i):
            if (mask, i) in memo:
                return memo[(mask, i)]
            if mask == (1 << n) - 1:
                return self.get_weight(nodes[i], nodes[0])
            res = float('inf')
            for j in range(n):
                if mask & (1 << j) == 0:
                    new_cost = self.get_weight(nodes[i], nodes[j]) + dp(mask | (1 << j), j)
                    if new_cost < res:
                        res = new_cost
                        parent[(mask, i)] = j
            memo[(mask, i)] = res
            return res

        min_cost = float('inf')
        start_node = 0
        for i in range(1, n):
            cost = self.get_weight(nodes[0], nodes[i]) + dp(1 | (1 << i), i)
            if cost < min_cost:
                min_cost = cost
                start_node = i
                parent[(1, 0)] = i

        # Reconstruct the path
        mask = 1 | (1 << start_node)
        i = start_node
        path = [nodes[0], nodes[start_node]]
        while mask != (1 << n) - 1:
            next_node = parent[(mask, i)]
            path.append(nodes[next_node])
            mask |= (1 << next_node)
            i = next_node

        return path

    # ethan's code start --------------------------------------------------------------------------------

    def succ(self, path):
        #print(f"p:{path}")
        # return successors (neighbors)
        # neighbours -> array of successors
        curr_node = path[-1][0]
        neighbors = []
        # explore nodes in the same path (not explored, tsp modification)
        for node, weight in self.edges[curr_node].items():
            #print((node,weight))
            in_path = False
            # if node is same path, skip node
            for n, w in path:
                if n == node:
                    in_path = True
                    continue

            if not in_path:   
                new_path = path[:]
                successor = (node, weight)
                print("succ:",successor)
                new_path.append(successor)
                neighbors.append(new_path)
        #print()
        return neighbors

    def cost(self, path):
        # get cost of current path
        cost = 0
        for item in path:
            #print("item: ",item)
            cost = cost+item[1]
        return cost

    def h(self, path, explored):
        # call succ and return min cost from list
        successors = self.succ(path)
        min_cost = float('inf')
        if successors:
            for path_prime in successors:
                path_cost = self.cost(path_prime)
                if path_cost < min_cost:
                    min_cost = path_cost
        else:
            min_cost = 0
        return min_cost

    def get_total_cost(self, path):
        total_cost = 0
        for node, cost in path:
            total_cost = total_cost+cost
        return total_cost

    def dijkstra(self, start_node):
        # lists to track
        unexplored = []
        frontier = []
        explored = []
        solution = []
        # init frontier
        curr_node = (start_node, 0)
        frontier.append([curr_node])

        # main loop
        while frontier:
            print("f:",frontier)
            #print()
            # print(frontier)
            # print("ex:",explored)
            # lowest_priority -> min(current path cost + lowest future cost) of all path in frontier
            min_cost = float('inf')
            index_to_pop = -1
            curr_path = None
            for i, path in enumerate(frontier):
                future_cost = self.cost(path) + self.h(path, explored)
                #print(f"path: {path}, succ: {self.succ(path, explored)}, fcost: {future_cost}")
                if future_cost < min_cost:
                    index_to_pop = i
                    curr_path = path
                    min_cost = future_cost 
            # check end state
            if index_to_pop != -1:
                if len(curr_path) == len(self.nodes):
                    # end state reached
                    return (curr_path, self.get_total_cost(curr_path))
                frontier.pop(index_to_pop)
            # add to explored
            explored.append(curr_path)
            
            # expand winning node on layer deeper
            for paths in self.succ(curr_path):
                frontier.append(paths[:])

        return solution

    def a_star(self, start_node):
        print(self.dijkstra(start_node))
        #self.dijkstra(start_node)

    # ethan's code end --------------------------------------------------------------------------------


# Example usage:
if __name__ == "__main__":
    #random.seed(42)
    # Generate graphs
    
    graph_5_nodes = Graph()
    graph_15_nodes = Graph()
    graph_30_nodes = Graph()

    graph_5_nodes.generate_random_graph(5)
    graph_15_nodes.generate_random_graph(15)
    graph_30_nodes.generate_random_graph(30)

    # test data
    graph = Graph()
    graph.generate_random_graph(4)

    #print(graph_5_nodes.edges)
    print(graph.edges)
    graph.a_star('0')

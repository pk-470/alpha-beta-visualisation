from math import inf
import matplotlib.pyplot as plt
import igraph as ig


class Game_Tree:
    def __init__(self, edge_dict, leaf_values):
        self.edges = self.create_edges(edge_dict)
        self.graph = ig.Graph(edges=self.edges)
        self.vertices = [i for i in range(len(self.graph.vs))]
        self.leaf_values = leaf_values
        self.graph.vs["label"] = [
            "" if i not in self.leaf_values else self.leaf_values[i]
            for i in self.vertices
        ]
        self.max_nodes = [0]
        self.min_nodes = []
        for i in self.vertices[1:]:
            j = [k for k in self.graph.neighbors(i) if k < i][0]
            if j in self.max_nodes:
                self.min_nodes.append(i)
            elif j in self.min_nodes:
                self.max_nodes.append(i)

    def create_edges(self, edge_dict):
        edges = []
        for v_0 in edge_dict:
            for v_1 in edge_dict[v_0]:
                edges.append((v_0, v_1))
        return edges

    def draw(self, explored=None, optimal_edges=None):
        if explored is None:
            explored = []
        if optimal_edges is None:
            optimal_edges = []
        _, ax = plt.subplots()
        ax.invert_yaxis()
        layout = self.graph.layout_reingold_tilford(root=[0])
        ig.plot(
            self.graph,
            target=ax,
            layout=layout,
            vertex_shape=[
                "square" if i in self.max_nodes else "circle" for i in self.vertices
            ],
            vertex_color=[
                "green"
                if i in explored
                else "cyan"
                if i in self.max_nodes
                else "orange"
                for i in self.vertices
            ],
            vertex_size=[0.6 for _ in self.vertices],
            edge_color=["red" if e in optimal_edges else "black" for e in self.edges],
        )
        plt.show()

    def alpha_beta_minimax(self, i, alpha, beta, explored=None):
        if explored is None:
            explored = []

        if i in self.leaf_values:
            explored.append(i)
            value = self.leaf_values[i]
            self.graph.vs[i]["label"] = value
            return value

        children = [j for j in self.graph.neighbors(i) if j > i]

        # Max player
        if i in self.max_nodes:
            value = -inf
            for child in children:
                value = max(
                    value, self.alpha_beta_minimax(child, alpha, beta, explored)
                )
                alpha = max(alpha, value)
                if alpha >= beta:
                    break

        # Min player
        elif i in self.min_nodes:
            value = inf
            for child in children:
                value = min(
                    value, self.alpha_beta_minimax(child, alpha, beta, explored)
                )
                beta = min(beta, value)
                if alpha >= beta:
                    break

        self.graph.vs[i]["label"] = value
        if i == 0:
            return value, explored
        return value

    def alpha_beta_negamax(self, i, alpha, beta, explored=None):
        if explored is None:
            explored = []

        if i in self.leaf_values:
            explored.append(i)
            value = self.leaf_values[i] if i in self.max_nodes else -self.leaf_values[i]
            self.graph.vs[i]["label"] = value
            return value

        children = [j for j in self.graph.neighbors(i) if j > i]
        value = -inf
        for child in children:
            value = max(value, -self.alpha_beta_negamax(child, -beta, -alpha, explored))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        self.graph.vs[i]["label"] = value
        if i == 0:
            return value, explored
        return value

    def find_optimal(self, algorithm, score, optimal_path=None):
        i = 0
        optimal_path = [0]
        while True:
            children = [j for j in self.graph.neighbors(i) if j > i]
            if not children:
                return optimal_path
            for child in children:
                if algorithm == "minimax":
                    if self.graph.vs[child]["label"] == score:
                        optimal_path.append(child)
                        i = child
                        break
                elif algorithm == "negamax":
                    if self.graph.vs[child]["label"] == -score:
                        optimal_path.append(child)
                        i = child
                        score = -score
                        break

    def solve(self, algorithm):
        if algorithm == "minimax":
            score, explored = self.alpha_beta_minimax(0, -inf, inf)
        elif algorithm == "negamax":
            score, explored = self.alpha_beta_negamax(0, -inf, inf)
        optimal_path = self.find_optimal(algorithm, score)
        optimal_edges = [edge for edge in zip(optimal_path, optimal_path[1:])]
        print(f"Optimal score: {score}")
        self.draw(explored, optimal_edges)

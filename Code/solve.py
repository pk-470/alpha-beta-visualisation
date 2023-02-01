from game_tree import *
from tree_data import *


def draw_and_solve(algorithm):
    t = Game_Tree(EDGE_DICT, LEAF_VALUES)
    t.draw()
    t.solve(algorithm)


if __name__ == "__main__":
    draw_and_solve(algorithm="minimax")

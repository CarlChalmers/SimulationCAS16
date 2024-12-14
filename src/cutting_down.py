import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from IPython.display import clear_output

from src.forest_model import  *

## simulation ##

def cut_down_perimiter(forest,forest_state_manager, cluster_size,cluster_middle_point, radius):
    # Calculate the center of the diseased cluster
    Ni, Nj = forest.shape
    # Iterate through all cells in the forest
    for i in range(Ni):
        for j in range(Nj):
            # Calculate the distance from the current cell to the center of the cluster
            distance = np.sqrt((i - cluster_middle_point[0]) ** 2 + (j - cluster_middle_point[1]) ** 2)

            # cut down
            if radius - 0.5 <= distance <= radius + 0.5 :
                forest_state_manager.update_state(forest[i,j], "EMPTY")
    return forest,forest_state_manager

def prevention_menthod_perimiter(forest,forest_state_manager):
  clusters = find_disease_clusters(forest)
  for cluster in clusters:
    size = cluster["size"]
    if size < 10:
      continue
    forest,forest_state_manager = cut_down_perimiter(forest,forest_state_manager, size,cluster["middle_point"],np.sqrt(size)+1)
  return forest,forest_state_manager

def cut_down_sick_clusters(forest,forest_state_manager,min_size=4):
    """
    Identify clusters of connected 'SICK' and 'DEAD' trees in the forest.
    Each cluster is a group of adjacent (vertically or horizontally) sick or dead trees.
    :param forest: 2D numpy array of Tree objects
    :return: A list of clusters where each cluster is represented as a dictionary with:
             - size: Number of trees in the cluster
             - middle_point: The center position of the cluster (as (x, y))
    """
    amount_cut_down = 0
    forest_size = len(forest)
    visited = np.zeros((forest_size, forest_size), dtype=bool)  # Track visited trees
    clusters = []  # List to store information about each cluster

    def is_valid(x, y):
        """Check if a position is within bounds and unvisited."""
        return 0 <= x < forest_size and 0 <= y < forest_size and not visited[x, y]

    def dfs(x, y):
        """Perform DFS to find all trees in the cluster."""
        stack = [(x, y)]
        cluster_positions = []  # Store positions of trees in the cluster

        while stack:
            cx, cy = stack.pop()
            if not is_valid(cx, cy):
                continue
            visited[cx, cy] = True
            if forest[cx, cy].is_sick() or forest[cx, cy].is_dead():
                cluster_positions.append((cx, cy))

                # Add neighbors to the stack
                neighbors = [
                    (cx - 1, cy),  # Up
                    (cx + 1, cy),  # Down
                    (cx, cy - 1),  # Left
                    (cx, cy + 1)   # Right
                ]
                for nx, ny in neighbors:
                    if is_valid(nx, ny):
                        stack.append((nx, ny))

        return cluster_positions
    
    # Traverse the forest to find clusters
    for i in range(forest_size):
        for j in range(forest_size):
            if not visited[i, j] and (forest[i, j].is_sick() or forest[i, j].is_dead()):
                # Start a new cluster
                cluster_positions = dfs(i, j)
                if len(cluster_positions) >= min_size:
                    for cluster in cluster_positions:
                      amount_cut_down += 1
                      forest_state_manager.update_state(forest[cluster[0],cluster[1]], "EMPTY")

                    

    return forest,forest_state_manager,amount_cut_down

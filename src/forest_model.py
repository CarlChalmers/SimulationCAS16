import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from IPython.display import clear_output


######################################
#           Data Structures          #
######################################

class Tree:
    STATES = ["HEALTHY", "LATENT", "SICK", "DEAD", "EMPTY", "IMMUNE_LATENT", "IMMUNE_HEALTHY"]
    COLORS = {
        "HEALTHY": "green",
        "LATENT": "yellow",
        "SICK": "red",
        "DEAD": "black",
        "EMPTY": "white",
        "IMMUNE_LATENT": "orange",  # Immunized latent trees
        "IMMUNE_HEALTHY": "blue"   # Vaccinated and recovered healthy trees
    }

    def __init__(self, state="HEALTHY", latent_days_threshold=30, sick_days_threshold=10, dead_days_threshold=5, position=None):
        self.state = state
        self.color = Tree.COLORS[state]
        self.latent_days = 0
        self.latent_days_immune = 0
        self.sick_days = 0
        self.dead_days = 0
        self.latent_days_threshold = latent_days_threshold
        self.sick_days_threshold = sick_days_threshold
        self.dead_days_threshold = dead_days_threshold
        self.position = position
        self.immune = False  # If a latent tree recoverd by vaccination, it will be immune, initilized as False

    def __str__(self):
        return f"Tree(state={self.state}, color={self.color}, latent_days={self.latent_days}, sick_days={self.sick_days}, dead_days={self.dead_days})"

    def get_color(self):
        return self.color
    def is_healthy(self):
        return self.state == "HEALTHY"
    def is_latent(self):
        return self.state == "LATENT"
    def is_sick(self):
        return self.state == "SICK"
    def is_dead(self):
        return self.state == "DEAD"
    def is_empty(self):
        return self.state == "EMPTY"
    def is_immune(self):
        return self.immune

class ForestStateManager:
    def __init__(self, latent_days_threshold, sick_days_threshold, dead_days_threshold):
        """
        Initialize the state manager.
        :param latent_days_threshold: Threshold after which latent trees turn into sick trees.
        :param sick_days_threshold: Threshold after which sick trees turn into dead trees.
        :param dead_days_threshold: Threshold after which dead trees turn into empty trees.
        """
        self.latent_trees = []  # List of latent trees
        self.sick_trees = []  # List of sick trees
        self.dead_trees = []  # List of dead trees
        self.empty_trees = []  # List of empty trees
        self.latent_days_threshold = latent_days_threshold
        self.sick_days_threshold = sick_days_threshold
        self.dead_days_threshold = dead_days_threshold

    def update_state(self, tree, new_state):
        """Update the tree's state."""
        if new_state in Tree.STATES:

            # Remove tree from its current state list
            if tree in self.latent_trees:
                self.latent_trees.remove(tree)
            elif tree in self.sick_trees:
                self.sick_trees.remove(tree)
            elif tree in self.dead_trees:
                self.dead_trees.remove(tree)
            elif tree in self.empty_trees:
                self.empty_trees.remove(tree)

            # Update tree's state
            tree.state = new_state
            tree.color = Tree.COLORS[new_state]

            # Reset counters based on the new state
            if tree.state == "LATENT":
                tree.latent_days = 0
                self.latent_trees.append(tree)  # Add to latent_trees list
            elif tree.state == "SICK":
                tree.sick_days = 0
                self.sick_trees.append(tree)  # Add to sick_trees list
            elif tree.state == "DEAD":
                tree.dead_days = 0
                self.dead_trees.append(tree)  # Add to dead_trees list
            elif tree.state == "EMPTY":
                self.empty_trees.append(tree)  # Add to empty_trees list

    def get_sick_trees(self):
        return self.sick_trees

    def get_latent_trees(self):
        return self.latent_trees

    def get_dead_trees(self):
        return self.dead_trees

    def get_empty_trees(self):
        return self.empty_trees


######################################
#          Main Forest Model         #
######################################

def initialize_forest(forest_size, forest_cover_rate, forest_state_manager):
    """
    Initialize a forest and generate a 2D array of forest_size x forest_size.
    95% of the grids are healthy trees and 5% of the grids are empty.
    """
    forest = np.empty((forest_size, forest_size), dtype=object)

    for i in range(forest_size):
        for j in range(forest_size):
            if random.random() < forest_cover_rate:
              #this is ugly but has to be done because we have two thresholds, one for the state manager and one for the Tree Data Structure
                forest[i, j] = Tree("HEALTHY",latent_days_threshold=forest_state_manager.latent_days_threshold,sick_days_threshold=forest_state_manager.sick_days_threshold,dead_days_threshold=forest_state_manager.dead_days_threshold, position=(i, j))
            else:
                forest[i, j] = Tree("EMPTY",latent_days_threshold=forest_state_manager.latent_days_threshold,sick_days_threshold=forest_state_manager.sick_days_threshold,dead_days_threshold=forest_state_manager.dead_days_threshold, position=(i, j))
                forest_state_manager.empty_trees.append(forest[i, j])
    return forest, forest_state_manager
def forest_update(forest_state_manager, iter_num, grow_tree_prob, dead_trees, debug):
    """
    Updates the state of the entire forest: transitions trees from LATENT to SICK,
    from SICK to DEAD, and from DEAD to EMPTY based on their respective thresholds.
    This function also updates the respective lists in the ForestStateManager.
    """
    # Grow new trees in empty cells
    empty_trees = forest_state_manager.get_empty_trees()
    if not empty_trees:
        print("No empty trees available for growth.")
    else:
        for tree in empty_trees[:]:  # Iterate over a copy of the list
            if random.random() <= grow_tree_prob:
                forest_state_manager.update_state(tree, "HEALTHY")

    # Update all latent trees
    for tree in forest_state_manager.get_latent_trees()[:]:
        tree.latent_days += 1
        if tree.latent_days >= tree.latent_days_threshold:
            forest_state_manager.update_state(tree, "SICK")

    # Update all sick trees
    for tree in forest_state_manager.get_sick_trees()[:]:
        tree.sick_days += 1
        if tree.sick_days >= tree.sick_days_threshold:
            forest_state_manager.update_state(tree, "DEAD")
            dead_trees += 1

    # Update all dead trees
    for tree in forest_state_manager.get_dead_trees()[:]:
        tree.dead_days += 1
        if tree.dead_days >= tree.dead_days_threshold:
            forest_state_manager.update_state(tree, "EMPTY")
    if debug:
      print("Iter Number:", iter_num, "latent trees:", len(forest_state_manager.latent_trees),
            "sick trees:", len(forest_state_manager.sick_trees),
            "dead trees:", len(forest_state_manager.dead_trees),
            "emptys:", len(forest_state_manager.empty_trees))

    return forest_state_manager, dead_trees
def initialize_disease(forest, num_infected, forest_state_manager):
    """
    Randomly select `num_infected` trees in the forest and set them to SICK state.
    The selected trees must not be empty (i.e., they must be healthy).
    """
    forest_size = len(forest)
    infected_count = 0

    while infected_count < num_infected:
        # Randomly select a position in the forest
        i = random.randint(0, forest_size - 1)
        j = random.randint(0, forest_size - 1)

        if forest[i, j].is_healthy():
            tree = forest[i, j]
            forest_state_manager.update_state(tree, "SICK")
            infected_count += 1

    return forest, forest_state_manager
def propagate_disease_pbc(forest, forest_state_manager, infect_prob_sick, infect_prob_latent):
    """
    Propagate the disease from sick trees to their neighbors.
    """
    forest_size = len(forest)

    trees_state_lists = [
        (forest_state_manager.get_latent_trees()[:], infect_prob_latent),  # LATENT trees with their infection probability
        (forest_state_manager.get_sick_trees()[:], infect_prob_sick)      # SICK trees with their infection probability
    ]

    # Iterate through each list of trees (LATENT and SICK) and their respective infection probability
    for tree_list, infect_prob in trees_state_lists:
        for tree in tree_list:
            i, j = tree.position
            neighbors = [
                ((i - 1) % forest_size, j),  # Up
                ((i + 1) % forest_size, j),  # Down
                (i, (j - 1) % forest_size),  # Left
                (i, (j + 1) % forest_size)   # Right
            ]

            for x, y in neighbors:
                neighbor_tree = forest[x, y]
                if neighbor_tree.is_healthy():  # Only affect healthy trees
                    if random.random() < infect_prob:
                        forest_state_manager.update_state(neighbor_tree, "LATENT")

    return forest, forest_state_manager
def propagate_disease(forest, forest_state_manager, infect_prob_sick, infect_prob_latent):
    """
    Propagate the disease from sick trees to their neighbors without periodic boundary conditions.
    """
    forest_size = len(forest)

    trees_state_lists = [
        (forest_state_manager.get_latent_trees()[:], infect_prob_latent),  # LATENT trees with their infection probability
        (forest_state_manager.get_sick_trees()[:], infect_prob_sick)      # SICK trees with their infection probability
    ]

    # Iterate through each list of trees (LATENT and SICK) and their respective infection probability
    for tree_list, infect_prob in trees_state_lists:
        for tree in tree_list:
            i, j = tree.position
            neighbors = [
                (i - 1, j),  # Up
                (i + 1, j),  # Down
                (i, j - 1),  # Left
                (i, j + 1)   # Right
            ]

            for x, y in neighbors:
                # Check for valid indices
                if 0 <= x < forest_size and 0 <= y < forest_size:
                    neighbor_tree = forest[x, y]
                    if neighbor_tree.is_healthy():  # Only affect healthy trees
                        if random.random() < infect_prob:
                            forest_state_manager.update_state(neighbor_tree, "LATENT")

    return forest, forest_state_manager


######################################
#       Utilities for Simulation     #
######################################

def visualize_forest(forest):
    """
    Visualize the current state of the forest.
    """
    plt.clf()
    forest_size = len(forest)
    color_indices = np.zeros((forest_size, forest_size), dtype=int)

    # Create a mapping from tree states to colormap indices
    state_map = {state: idx for idx, state in enumerate(Tree.STATES)}
    state_counts = {state: 0 for state in Tree.STATES}  # Count occurrences of each state
    for i in range(forest_size):
        for j in range(forest_size):
            tree = forest[i, j]
            # Determine tree's state with vaccination consideration
            if tree.is_latent() and tree.is_immune() and not tree.is_dead() and not tree.is_empty():
                state = "IMMUNE_LATENT"
            elif tree.is_healthy() and tree.is_immune() and not tree.is_dead() and not tree.is_empty():
                state = "IMMUNE_HEALTHY"
            else:
                state = tree.state
            color_indices[i, j] = state_map[state]
            state_counts[state] += 1  # Count the state occurrence
    for i in range(forest_size):
        for j in range(forest_size):
            state = forest[i, j].state
            color_indices[i, j] = state_map[state]
            state_counts[state] += 1  # Count the state occurrence

    # Filter out states with zero occurrences
    active_states = [state for state, count in state_counts.items() if count > 0]
    active_colors = [Tree.COLORS[state] for state in active_states]
    active_indices = [state_map[state] for state in active_states]

    # Create a colormap from active states
    cmap = ListedColormap(active_colors)

    # Map `color_indices` to only active states
    remapped_indices = np.zeros_like(color_indices)
    remap_map = {old_idx: new_idx for new_idx, old_idx in enumerate(active_indices)}
    for i in range(forest_size):
        for j in range(forest_size):
            remapped_indices[i, j] = remap_map[color_indices[i, j]]
    # Plot the forest
    im = plt.imshow(remapped_indices, cmap=cmap)

    # Create legend for active states
    handles = [Patch(color=Tree.COLORS[state], label=state) for state in active_states]
    plt.legend(handles=handles, loc="upper right", fontsize='small')
    clear_output(wait=True)  # Clear the previous plot
    plt.title("Forest Visualization")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.grid(False)
    plt.pause(0.01)  # Pause to allow visualization update

def find_disease_clusters(forest,min_size=10):
    """
    Identify clusters of connected 'SICK' and 'DEAD' trees in the forest.
    Each cluster is a group of adjacent (vertically or horizontally) sick or dead trees.
    :param forest: 2D numpy array of Tree objects
    :return: A list of clusters where each cluster is represented as a dictionary with:
             - size: Number of trees in the cluster
             - middle_point: The center position of the cluster (as (x, y))
    """
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
                if cluster_positions:
                    # Calculate cluster size and middle point
                    cluster_size = len(cluster_positions)

                    x_coords = [pos[0] for pos in cluster_positions]
                    y_coords = [pos[1] for pos in cluster_positions]
                    middle_point = (sum(x_coords) // cluster_size, sum(y_coords) // cluster_size)

                    clusters.append({
                        "size": cluster_size,
                        "middle_point": middle_point
                    })

    return clusters

def plot_state_counts(state_counts, epochs):
    """
    Plot the count of different tree states over epochs.
    """
    plt.figure(figsize=(10, 6))
    for state, counts in state_counts.items():
        plt.plot(range(epochs), counts, label=state)
    plt.title("Tree States Over Time")
    plt.xlabel("Epochs")
    plt.ylabel("Number of Trees")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()

def loss_function(a, b, c, d, e, vaxinate_cost, dead_trees, sum_cuted_down, immune_treees_healthy, disease_eliminated_days):
    value = a * vaxinate_cost + b * dead_trees + c * sum_cuted_down - d * immune_treees_healthy + e * disease_eliminated_days
    return value
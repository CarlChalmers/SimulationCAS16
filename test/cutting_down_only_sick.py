import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from IPython.display import clear_output
import sys
# sys.path.insert(0,"C:\Chalmers\Simulation")
sys.path.insert(0,"D:\Projects\Simulations2024\SimulationCAS16")

from src.forest_model import *
from src.cutting_down import *
from src.vaxinate_model import *

def test_forest_model():

    # Initialize the forest state manager as global
    state_counts = {
        "HEALTHY": [],
        "LATENT": [],
        "SICK": [],
        "DEAD": [],
        "EMPTY": [],
        "IMMUNE_LATENT": [],
        "IMMUNE_HEALTHY": []
    }
    forest_state_manager = ForestStateManager(7,10,15)
    N_skip = 20
    iter_num = 1
    epochs = 500
    forest_size = 100
    num_infected = 10
    forest_cover_rate = 0.95
    # low: 0.06 medium: 0.14 high: 0.35
    infect_prob_sick = 0.06  
    # low: 0.04 medium: 0.08 high: 0.2
    infect_prob_latent = 0.04
    grow_tree_prob = 0.01
    unsucceceful_vaccination = 0.20
    latent_days_immune_threshold = 5
  

    a = 1.5
    b = 2
    c = 1
    d = 1
    e = 0.7
    vaxinate_cost = 0
    dead_trees = 0
    sum_cuted_down = 0
    immune_treees_healthy = 0
    disease_eliminated_days = 0

    # 1. Initialize the forest
    forest, forest_state_manager = initialize_forest(forest_size, forest_cover_rate, forest_state_manager)
    visualize_forest(forest)

    # 2. Initialize the disease
    forest, forest_state_manager = initialize_disease(forest, num_infected, forest_state_manager)
    visualize_forest(forest)
    trees_cut_down = 0

    # 4. Propagate the disease
    for i in range(epochs):
        forest, forest_state_manager = propagate_disease(forest, forest_state_manager, infect_prob_sick, infect_prob_latent)
        forest_state_manager,dead_trees = forest_update(forest_state_manager, iter_num, grow_tree_prob,dead_trees,False)
        trees_cut_down = 0

        forest,forest_state_manager,trees_cut_down = cut_down_sick_clusters(forest,forest_state_manager)
        sum_cuted_down+=trees_cut_down

        state_counts["HEALTHY"].append(len([tree for row in forest for tree in row if tree.is_healthy()]))
        state_counts["LATENT"].append(len([tree for row in forest for tree in row if tree.is_latent()]))
        state_counts["SICK"].append(len([tree for row in forest for tree in row if tree.is_sick()]))
        state_counts["DEAD"].append(len([tree for row in forest for tree in row if tree.is_dead()]))
        state_counts["EMPTY"].append(len([tree for row in forest for tree in row if tree.is_empty()]))
        state_counts["IMMUNE_LATENT"].append(len([tree for row in forest for tree in row if tree.state == "IMMUNE_LATENT"]))
        state_counts["IMMUNE_HEALTHY"].append(len([tree for row in forest for tree in row if tree.state == "IMMUNE_HEALTHY"]))

        if len(forest_state_manager.sick_trees) == 0 and len(forest_state_manager.latent_trees) == 0:
           break

        # for cluster in find_disease_clusters(forest):
        #   print(cluster["middle_point"])
        if iter_num % N_skip == 0:
          visualize_forest(forest)
        iter_num += 1
        
    disease_eliminated_days = iter_num
    print("After ", iter_num, "days, the forest disease is eliminated!")
    print("Vaxinate cost is: ", vaxinate_cost)
    print("Dead trees is: ", dead_trees)
    print("Number of immuned healthy trees is: ", immune_treees_healthy)
    print("Disease eliminated days is: ", disease_eliminated_days)
    print("Sum of cut down trees: ", sum_cuted_down)
    loss_value = loss_function(a, b, c, d, e, vaxinate_cost, dead_trees, sum_cuted_down, immune_treees_healthy, disease_eliminated_days)
    print("Loss value is: ", loss_value)
    current_epoch = i
    ## Final Step in one iteration
    forest_state_manager ,dead_trees= forest_update(forest_state_manager, iter_num, grow_tree_prob,dead_trees,True)
    plot_state_counts(state_counts, current_epoch + 1)




# Run the test
if __name__ == "__main__":
    test_forest_model()

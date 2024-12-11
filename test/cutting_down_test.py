import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from IPython.display import clear_output
import sys
sys.path.insert(0,"C:\Chalmers\Simulation")

from scr.forest_model import *
from scr.cutting_down import *
from scr.vaxinate_model import *

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
    N_skip = 2
    iter_num = 1
    epochs = 100
    forest_size = 100
    num_infected = 10
    forest_cover_rate = 0.99
    infect_prob_sick = 0.4
    infect_prob_latent = 0.4
    grow_tree_prob = 0.05
    unsucceceful_vaccination = 0.20
    latent_days_immune_threshold = 5
    # 1. Initialize the forest
    forest, forest_state_manager = initialize_forest(forest_size, forest_cover_rate, forest_state_manager)
    visualize_forest(forest)

    # 2. Initialize the disease
    forest, forest_state_manager = initialize_disease(forest, num_infected, forest_state_manager)
    visualize_forest(forest)

    # 3. Choose prevention method
    prevention_method = "cut_down_perimiter"
    # prevention_method = "vaxinate" #--------WIP
    #prevention_method = "cut_down_dead"----TODO
    # prevention_method = "none"

    # 4. Propagate the disease
    for i in range(epochs):
        forest, forest_state_manager = propagate_disease(forest, forest_state_manager, infect_prob_sick, infect_prob_latent)
        forest_state_manager = forest_update(forest_state_manager, iter_num, grow_tree_prob,False)

        match prevention_method:
          case "cut_down_perimiter":
             forest, forest_state_manager = prevention_menthod_perimiter(forest,forest_state_manager)
          case "vaxinate":
             forest, forest_state_manager = prevention_menthod_vaxinate(forest,forest_state_manager,unsucceceful_vaccination,latent_days_immune_threshold)

        state_counts["HEALTHY"].append(len([tree for row in forest for tree in row if tree.is_healthy()]))
        state_counts["LATENT"].append(len([tree for row in forest for tree in row if tree.is_latent()]))
        state_counts["SICK"].append(len([tree for row in forest for tree in row if tree.is_sick()]))
        state_counts["DEAD"].append(len([tree for row in forest for tree in row if tree.is_dead()]))
        state_counts["EMPTY"].append(len([tree for row in forest for tree in row if tree.is_empty()]))
        state_counts["IMMUNE_LATENT"].append(len([tree for row in forest for tree in row if tree.state == "IMMUNE_LATENT"]))
        state_counts["IMMUNE_HEALTHY"].append(len([tree for row in forest for tree in row if tree.state == "IMMUNE_HEALTHY"]))

        # for cluster in find_disease_clusters(forest):
        #   print(cluster["middle_point"])
        if iter_num % N_skip == 0:
          visualize_forest(forest)
        iter_num += 1

    ## Final Step in one iteration
    forest_state_manager = forest_update(forest_state_manager, iter_num, grow_tree_prob,True)
    plot_state_counts(state_counts, epochs)



# Run the test
if __name__ == "__main__":
    test_forest_model()

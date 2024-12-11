from scr.forest_model import  *

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
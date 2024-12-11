from scr.forest_model import  *


def vaxinate_perimiter(forest,forest_state_manager, cluster_size,cluster_middle_point, radius,unsucceceful_vaccination,recovering_trees):
    # Calculate the center of the diseased cluster
    Ni, Nj = forest.shape
    # Iterate through all cells in the forest
    for i in range(Ni):
        for j in range(Nj):
            # Calculate the distance from the current cell to the center of the cluster
            distance = np.sqrt((i - cluster_middle_point[0]) ** 2 + (j - cluster_middle_point[1]) ** 2)

            # vaxinate
            if random.random() < unsucceceful_vaccination:
              continue
            if radius - 0.5 <= distance <= radius + 0.5 :
              if forest[i,j].is_healthy():
                forest_state_manager.update_state(forest[i,j], "IMMUNE_HEALTHY")
                forest[i,j].is_immune = True
              elif forest[i,j].is_latent():
                forest[i,j].is_immune = True
                forest_state_manager.update_state(forest[i,j], "IMMUNE_LATENT")
                
                recovering_trees.append(forest[i,j])
    return forest,forest_state_manager,recovering_trees



def prevention_menthod_vaxinate(forest,forest_state_manager,unsucceceful_vaccination,recovering_trees, latent_days_immune_threshold):
  clusters = find_disease_clusters(forest)
  
  for cluster in clusters:
    size = cluster["size"]
    if size < 10:
      continue
    forest,forest_state_manager,recovering_trees = vaxinate_perimiter(forest,forest_state_manager, size,cluster["middle_point"],np.sqrt(size)+1,unsucceceful_vaccination,recovering_trees)
    for tree in recovering_trees:
        tree.latent_days_immune += 1
        if(tree.latent_days_immune >= latent_days_immune_threshold):
           forest_state_manager.update_state(tree, "IMMUNE_HEALTHY")
           recovering_trees.remove(tree)
  return forest,forest_state_manager,recovering_trees
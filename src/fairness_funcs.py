import numpy as np


def calculate_in_class_homophily(graph,
                                 features_dict,
                                 class_feature_value):
    '''
    Calculates simple average homophily for specified class.

    Notes:
        - features_dict contains values for the feature of interest. Based on
          this feature the average homophily for specified class is calculated.
          For nodes i and j (where i is from the class of interest):
              if features_dict[i] == features_dict[j], then it counts as 1 (homophilic)
              else it counts as 0 (heterophilic)
    
    Arguments:
        graph(snap.Graph): The graph
        features_dict(dictionary): A dictionary with (keys: <node_id>, values: <feature value>)
        class_feature_value(int): The value of the class feature
    Returns:
        Average homophily for specified class

    '''

    class_nodes_sum = 0
    avg_homophily_sum = 0
    for node in graph.Nodes():
        # Check if node is of class specified by class_feature_value
        if features_dict[node.GetId()] != class_feature_value:
            continue

        class_nodes_sum += 1
        homophily_sum = 0
        
        # Get neighbors
        num_of_neighbors, neighbors = graph.GetNodesAtHop(node.GetId(),
                                                          1,
                                                          True)
        if num_of_neighbors == 0:
            continue
        
        # Iterate through neighbors
        for neighbor in neighbors:
            if features_dict[neighbor] == class_feature_value:
                homophily_sum += 1

        avg_homophily_sum += homophily_sum/num_of_neighbors

    return avg_homophily_sum/class_nodes_sum
        
        
def calculate_top_k_class_rate(k,
                               class_feature_value,
                               features_dict,
                               scores_sorted_desc):
    '''
    Calculates the rate of a specific class in top-k% of a rank.

    Arguments:
        k(int): The top-k% parameter
        class_feature_value(int): The class value to calculate its percentage
        features_dict(dictionary): A dictionary with 
        scores_sorted_desc(dictionary): A dictionary with (keys: <node_id>, values: <score>)
            sorted in descending order
    '''
    # Input check
    if k < 0 or k > 100:
        print("Invalid value of parameter 'k': should be in range [0,100]")
        exit(-1)
        
    num_of_top_k_nodes = round(len(scores_sorted_desc)*k/100)

    class_sum = 0
    temp_counter = 0

    for node in scores_sorted_desc:
        if features_dict[node] == class_feature_value:
            class_sum += 1

        temp_counter += 1
        if temp_counter == num_of_top_k_nodes:
            break

    return class_sum/num_of_top_k_nodes


def calculate_gini_coefficient(x):
    '''
    Calculates the GINI coefficient of vector x

    Arguments:
        x(array_like): An array-like variable with the values
    Returns:
        The GINI coefficient
    '''
    gini = 0
    for i in range(len(x)):
        for j in range(len(x)):
            gini += abs(x[i] - x[j])
    gini /= 2*np.mean(x)*len(x)**2
    
    return gini


def calculate_scores(graph,
                     algorithm,
                     sorted_bool=False):
    '''
    Calculates scores for nodes of a graph based on specific algorithm.

    Arguments:
        graph(snap.Graph): The graph
        algorithm(str): Which algorithm to use for producing scores
            Options:
                - 'pagerank'
        sorted_bool(bool): If True, sort the scores in descending order
    Returns:
        A dictionary with the scores for each node
    '''

    if algorithm == 'pagerank':
        scores = graph.GetPageRank()
    elif algorithm == 'eccentricity':
        scores = {}
        for node in graph.Nodes():
            node_eccentricity = graph.GetNodeEcc(node.GetId(), True)

            # Store the reciprocal of node eccentricity
            scores[node.GetId()] = (1/node_eccentricity) if node_eccentricity != 0 else 0

    elif algorithm == 'centrality':
        scores, _ = graph.GetBetweennessCentr(0.5)

        # Normalize scores
        #min_score = min(scores.values())
        #max_score = max(scores.values())

        #for key in scores:
        #    scores[key] = (scores[key] - min_score)/(max_score - min_score)
    else:
        print('Not supported or invalid algorithm was given')
        exit(-1)

    if sorted_bool:
        scores = {k: v for k, v in sorted(scores.items(),
                                          key=lambda item: item[1],
                                          reverse=True)}

    return scores

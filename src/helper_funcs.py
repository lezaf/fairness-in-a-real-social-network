import os


def make_genders_dict(features_filename,
                      nodes_mapping,
                      gender_start_pos,
                      gender_end_pos,
                      node_name_pos=0):
    '''
    Creates a dictionary with the gender of each node

    Arguments:
        features_filename(str): The name of the file with the features
        nodes_mapping(dictionary): The dictionary of mapping from
            node names to node is as specified from snap.LoadEdgeListStr()
            when Mapping=True
        gender_start_pos(int): The starting position of gender feature
        gender_end_pos(int): The ending position of gender feature
        node_name_pos(int): The position of node name
    Returns:
        Dictionary with (keys: <node_id>, values: <gender>)

    '''

    genders_dict = {}

    with open(features_filename) as f:
        for line in f:
            line_split = line.split()

            # Get the name of the node
            node_name = line_split[node_name_pos]

            # Get the gender 0/1 features
            gender_features = line_split[gender_start_pos:gender_end_pos + 1]

            # Get the node id for the node name
            node_id = nodes_mapping.GetKeyId(node_name)

            # Note: There are some nodes in features file that don't exist
            #       in edges. GetKeyId(node_name) returns -1 in this case.
            #       Skip nodes that return -1 as node_id
            if node_id == -1:
                continue

            # Decide gender
            if int(gender_features[0]) == 1:
                genders_dict[node_id] = 1
            elif int(gender_features[1]) == 1:
                genders_dict[node_id] = 2
            elif int(gender_features[2]) == 1:
                genders_dict[node_id] = 3
            else:
                genders_dict[node_id] = -1 # Case that gender info is missing

    return genders_dict


def eliminate_no_gender_nodes(graph,
                              genders_dict):
    '''
    Removes nodes with no gender information from the graph.

    Arguments:
        graph(snap.Graph): The graph
        genders_dict(dictionary): A dictionary with (keys: <node_id>, values: <gender>)
    Returns:
        Updated graph and genders_dict
    '''

    no_gender_nodes = []

    # Find no gender nodes
    for node in genders_dict:
        if genders_dict[node] == -1:
            no_gender_nodes.append(node)

    if len(no_gender_nodes) == 0:
        return graph, genders_dict

    # Remove no gender nodes from dictionary
    for node in no_gender_nodes:
        del genders_dict[node]

    # Remove nodes from graph
    graph.DelNodes(no_gender_nodes)

    return graph, genders_dict


def get_gender_counters(genders_dict,
                        num_of_genders=3):
    '''
    Calculates the counter for each gender

    Notes:
        Assumes that the genders are notated as: 1, 2, 3, ...
    Arguments:
        genders_dict(dictionary): Dictionary with the (keys: <node_id>, values: <gender>)
        num_of_genders(int): The number of genders
    Returns:
        Dictionary with counters
    '''

    gender_counters = {}

    # Initialize counters
    for i in range(1, num_of_genders + 1):
        gender_counters[i] = 0

    # Find gender counters
    for node in genders_dict:
        gender = genders_dict[node]
        gender_counters[gender] += 1

    return gender_counters


def save_score_results(directory_path,
                       network_name,
                       algorithm_str,
                       scores,
                       genders_dict,
                       mapping=None):
    '''
    Saves the results of a ranking algorithm in a .txt file

    Arguments:
        directory_str(str): The directory to save the results
        network_name(str): The name of the network to be used for filename
        algorithm_str(str): The ranking algorithm used
        scores(dictionary): A dictionary with (keys: <node_id>, values: <score>)
        genders_dict(dictionary): A dictionary with (keys: <node_id>, values: <gender>)
        mapping(dictionary): A dictionary with the labels for each node id
    '''
    filename = "{}_{}_scores.txt".format(network_name,
                                         algorithm_str)
    
    with open(os.path.join(directory_path, filename), 'w') as f:
        # Write header line
        f.write("#node_label\t\t#score\t\t\t#gender\n")

        for key in scores:
            if mapping:
                node_label = mapping.GetKey(key)
            else:
                node_label = key

            # Write info
            f.write("{}\t{}\t{}\n".format(node_label,
                                          scores[key],
                                          genders_dict[key]))


def load_score_results(file_path):
    '''
    Loads the scores from the corresponding file

    Arguments:
        file_path(str): The path of the file to load
    '''
    scores = []
    genders = []
    with open(file_path) as f:
        # Skip header line
        f.readline()

        for line in f.readlines():
            scores.append(float(line.split()[1]))
            genders.append(float(line.split()[2]))
            
    return scores, genders

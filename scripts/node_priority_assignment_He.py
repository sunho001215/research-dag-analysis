import os
import tqdm
from spin_rate_optimization import read_csv_file
from random_dag_generator import create_csv_file, compute_length, no_successor

def no_predecessor(node, node_assign):
    for parent_node in node.parent:
        if node_assign[parent_node] == False:
            return False
    return True

def node_priority_assign_He(node_list):
    l, lb = compute_length(node_list)

    node_assign = [False] * len(node_list)
    p = 0

    A, new_A = [], []
    while True:
        A = []
        for idx, node in reversed(list(enumerate(node_list))):
            if no_predecessor(node, node_assign) and not node_assign[idx]:
                A.append(idx)
        
        while len(A) != 0:
            max, max_lb, value = 0, 0, 0
            max_idx = A[0]

            for idx, val in enumerate(A):
                if max < l[val] or (max == l[val] and max_lb < lb[val]):
                    max = l[val]
                    max_lb = lb[val]
                    max_idx = idx
                    value = val
            
            node_list[A[max_idx]].priority = p
            p += 1

            node_assign[A[max_idx]] = True

            A.remove(value)

        if False not in node_assign:
            break

    return node_list

if __name__ == "__main__":
    parent_dir = os.getcwd()
    
    #raw_data_dir = parent_dir + '/csv/raw_data/'
    optimization_result_dir = parent_dir + '/csv/optimization_result/'

    #raw_data_dir_He = parent_dir + '/csv/raw_data_He/'
    optimization_result_dir_He = parent_dir + '/csv/optimization_result_He/'

    csv_list = []
    for path in os.listdir(optimization_result_dir):
        if os.path.isfile(os.path.join(optimization_result_dir, path)):
            csv_list.append(path)
    csv_list.sort()
    
    for file in csv_list:    
        # csv_path = raw_data_dir_He + file
        # node_list = read_csv_file(os.path.join(raw_data_dir, file))
        # node_list = node_priority_assign_He(node_list)
        # create_csv_file(node_list, csv_path)

        csv_path = optimization_result_dir_He + file   
        node_list = read_csv_file(os.path.join(optimization_result_dir, file))
        node_list = node_priority_assign_He(node_list)
        create_csv_file(node_list, csv_path)
        

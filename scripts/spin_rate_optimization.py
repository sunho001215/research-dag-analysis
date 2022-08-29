import os
import csv
import json
import math
from time import sleep
from ros_node import Node
from random_dag_generator import create_csv_file, find_all_paths
from tqdm import tqdm

############# PARAM #############
core_num_ = 4
#################################

def read_csv_file(file):
    node_list = []
    node_idx = 0
    with open(file, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader)
            
        for row in csv_reader:
            node_list.append(Node())
            
            node_list[node_idx].level = int(row[1])
            node_list[node_idx].idx = int(row[2])
            node_list[node_idx].priority = int(row[3])
                
            node_list[node_idx].d_exec_t = float(row[4])
            node_list[node_idx].c_exec_t = float(row[5])
            node_list[node_idx].period = int(row[6])
                
            node_list[node_idx].isSource = (row[7] == 'True')
            node_list[node_idx].isSink = (row[8] == 'True')

            node_list[node_idx].parent = json.loads(row[9])
            node_list[node_idx].child = json.loads(row[10])

            node_idx += 1

    return node_list

def calculate_total_workload(node_list):
    total_workload = 0
    for node in node_list:
        if node.level != 0:
            total_workload += node.period + node.c_exec_t
        else:
            total_workload += node.c_exec_t
    return total_workload

def find_longest_path_dfs(node_list, start_vertex, end_vertex):
    paths = find_all_paths(node_list, start_vertex, end_vertex)

    costs = []
    for path in paths:
        cost = 0
        for node in path:
            if node.level != 0:
                cost += node.period + node.c_exec_t
            else:
                cost += node.c_exec_t
        costs.append(cost)

    (m, i) = max((v,i) for i,v in enumerate(costs))

    return m, paths[i]   

def calculate_critical_length(node_list):
    critical_length, critical_nodes = find_longest_path_dfs(node_list, node_list[0], node_list[len(node_list)-1])
    return critical_length, critical_nodes

def default_routine_interference(node_list, window_length):
    interference = 0
    for node in node_list:
        if node.level != 0:
            interference += math.floor((window_length + node.period - node.d_exec_t) / (node.period)) * node.d_exec_t + node.d_exec_t
    
    return interference

def calculate_response_time(node_list, total_workload, critical_length, response_time):
    response_time_new = 0
    while response_time != response_time_new:
        response_time = response_time_new
        response_time_new = critical_length + (total_workload - critical_length) / core_num_ \
                            + default_routine_interference(node_list, response_time) / core_num_
    return response_time

def optimize_spin_rate(node_list, file):
    total_workload = calculate_total_workload(node_list)
    
    critical_length_new, critical_nodes_new = calculate_critical_length(node_list)
    response_time_new = critical_length_new + (total_workload - critical_length_new) / core_num_

    critical_length, response_time, critical_nodes = 0, 0, []
    
    count = 0
    while critical_nodes != critical_nodes_new and response_time != response_time_new:
        critical_length = critical_length_new
        critical_nodes = critical_nodes_new
        response_time = response_time_new

        response_time_new = calculate_response_time(node_list, total_workload, critical_length, response_time)

        for node in node_list:
            if node.level != 0:
                if node in critical_nodes:
                    node.period = int(math.sqrt((response_time_new - node.d_exec_t) * node.d_exec_t / core_num_))
                else:
                    node.period = int(math.sqrt((response_time_new - node.d_exec_t) * node.d_exec_t))
                
                if node.period <= 0:
                    node.period = 1
        
        critical_length_new, critical_nodes_new = calculate_critical_length(node_list)
        count += 1

        if count >= 99999:
            print(str(file) + ": Critical Path Not Converged!!")
            break 

    return node_list


if __name__ == '__main__':
    parent_dir = os.getcwd()
    raw_data_dir = parent_dir + '/csv/raw_data/'
    result_dir = parent_dir + '/csv/optimization_result/'

    csv_list = []
    for path in os.listdir(raw_data_dir):
        if os.path.isfile(os.path.join(raw_data_dir, path)):
            csv_list.append(path)
    csv_list.sort()
    
    for file in tqdm(csv_list):    
        csv_path = result_dir + file
        
        node_list = read_csv_file(os.path.join(raw_data_dir, file))
        node_list = optimize_spin_rate(node_list, file)
        create_csv_file(node_list, csv_path)
        


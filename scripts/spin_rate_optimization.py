import os
import csv
import json
import math
import random
from time import sleep
from ros_node import Node
from random_dag_generator import create_csv_file, calculate_critical_length, node_priority_assign
from tqdm import tqdm

############# PARAM #############
core_num_ = 4
# Simulated Annealing Parameters
N_ = 50
alpha_ = 0.5
beta_ = 1.3
gamma_ = 0.9
temperature_ = 100
#################################

random.seed(1)

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
            node_list[node_idx].period = float(row[6])
                
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

def compute_local_minimum(node_list):
    response_time = math.inf
    
    total_workload = calculate_total_workload(node_list)
    critical_length, critical_nodes = calculate_critical_length(node_list)
    response_time_new = calculate_response_time(node_list, total_workload, critical_length, \
                            critical_length + (total_workload - critical_length) / core_num_)
    
    while response_time > response_time_new :
        response_time = response_time_new
        node_backup = node_list

        for node in node_list:
            if node.level != 0:
                if node in critical_nodes:
                    node.period = round(math.sqrt((response_time_new - node.d_exec_t) * node.d_exec_t / core_num_),1)
                else:
                    node.period = round(math.sqrt((response_time_new - node.d_exec_t) * node.d_exec_t), 1)
                
                if node.period <= 0:
                    node.period = 0.1
        
        total_workload = calculate_total_workload(node_list)
        critical_length, critical_nodes = calculate_critical_length(node_list)
        response_time_new = calculate_response_time(node_list, total_workload, critical_length, \
                                critical_length + (total_workload - critical_length) / core_num_)
    
    return node_backup, response_time

def simulated_annealing(node_list, response_time, temperature):
    node_backup = node_list

    for node in node_list:
        if node.level != 0:
            node.period = round(random.uniform(alpha_ * node.period, beta_ * node.period), 1)
    
    total_workload = calculate_total_workload(node_list)
    critical_length, _ = calculate_critical_length(node_list)
    response_time_new = calculate_response_time(node_list, total_workload, critical_length, \
                            critical_length + (total_workload - critical_length) / core_num_)
    
    response_time_change = response_time_new - response_time

    if response_time_change > 0 and random.uniform(0, 1) > math.exp(-response_time_change/temperature):
        node_list = node_backup

    temperature = temperature * gamma_
    
    return node_list, temperature

def optimize_spin_rate(node_list, file):
    minimum_response_time = math.inf
    minimum_node_list = node_list
    
    temperature = temperature_
    for i in range(N_):
        node_list, response_time = compute_local_minimum(node_list)
        
        if response_time < minimum_response_time:
            minimum_response_time = response_time
            minimum_node_list = node_list
        
        node_list, temperature = simulated_annealing(node_list, response_time, temperature)
    
    return minimum_node_list

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
        node_list = node_priority_assign(node_list)
        create_csv_file(node_list, csv_path)
        


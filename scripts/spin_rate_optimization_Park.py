import os
import math
from tqdm import tqdm
from spin_rate_optimization import read_csv_file, core_num_
from random_dag_generator import calculate_critical_length, node_priority_assign, create_csv_file

def calculate_preemption_delay(critical_node, node_list, initial_value):
    preemption_delay = 0
    for node in node_list:
        if node != critical_node:
            preemption_delay = preemption_delay + math.ceil(initial_value / node.period) * node.d_exec_t

    preemption_delay = (float)(preemption_delay/core_num_)
    
    return preemption_delay

def calculate_response_time_Park(node_list, critical_nodes):
    response_time = 0

    for critical_node in critical_nodes:
        if critical_node.level == 0:
            response_time = response_time + critical_node.c_exec_t
        else:
            response_time = response_time + critical_node.c_exec_t + critical_node.period
        
        preemption_delay_new = calculate_preemption_delay(critical_node, node_list, 0.1)
        preemption_delay = 0
        while preemption_delay_new != preemption_delay:
            preemption_delay = preemption_delay_new
            preemption_delay_new = calculate_preemption_delay(critical_node, node_list, preemption_delay)
        
        response_time += preemption_delay

    return response_time

def optimize_spin_rate_Park(node_list, file):
    _, critical_nodes = calculate_critical_length(node_list)

    minimum_period = 100

    for node in node_list:
        if node.level != 0 and node in critical_nodes:
            minimum_response_time = math.inf

            for p in range(2, 1001):
                node.period = (float)(p/10)
                response_time = calculate_response_time_Park(node_list, critical_nodes)
                if response_time < minimum_response_time:
                    minimum_response_time = response_time
                    minimum_period = node.period
            
            node.period = minimum_period

    return node_list

if __name__ == '__main__':
    parent_dir = os.getcwd()
    raw_data_dir = parent_dir + '/csv/raw_data/'
    result_dir = parent_dir + '/csv/optimization_result_Park/'

    csv_list = []
    for path in os.listdir(raw_data_dir):
        if os.path.isfile(os.path.join(raw_data_dir, path)):
            csv_list.append(path)
    csv_list.sort()
    
    for file in tqdm(csv_list):    
        csv_path = result_dir + file
        
        node_list = read_csv_file(os.path.join(raw_data_dir, file))
        node_list = optimize_spin_rate_Park(node_list, file)
        node_list = node_priority_assign(node_list)
        create_csv_file(node_list, csv_path)
        


import random
import os
import csv
import plotly.graph_objects as go
from ros_node import Node
from tqdm import tqdm

random.seed(1)

############# PARAM #############
dag_num_ = 100
# DAG generation parameter
depth_range_ = [3, 7]
max_parallelism_ = 5
arc_prob_ = 0.05
# Node execution time parameter
d_exec_range_ = [0.01, 0.15]
c_exec_range_ = [1, 40]
c_exec_limit_ = [250, 600]
critical_execution_path_portion_ = 0.65
#################################

def arc_deicision():
    return random.random() < arc_prob_

def dag_generate():
    dag_depth = random.randint(depth_range_[0], depth_range_[1])
    
    node_num = []
    for i in range(dag_depth):
        node_num.append(random.randint(2, max_parallelism_))
    
    node_list = []
    node_idx = 0
    
    # source node
    node_list.append(Node())
    node_list[0].isSource = True
    node_list[0].period = 1000 # 1s
    node_idx += 1

    # make node & assign parent node
    for i in range(dag_depth):
        for j in range(node_num[i]):
            node_list.append(Node())
            node_list[node_idx].level = i + 1
            node_list[node_idx].idx = j + 1
            if i == 0:
                node_list[node_idx].parent.append(0)
            else:
                while len(node_list[node_idx].parent) == 0:
                    for k in range(node_idx):
                        if k == 0:
                            continue
                        elif node_list[k].level < node_list[node_idx].level:
                            if arc_deicision():
                                node_list[node_idx].parent.append(k)
                        else:
                            break
            node_idx += 1

    # sink node
    node_list.append(Node())
    node_list[node_idx].isSink = True
    node_list[node_idx].level = dag_depth+1
    for i in reversed(range(node_idx)):
        if node_list[i].level == dag_depth:
            node_list[node_idx].parent.append(i)
        else:
            break
    node_list[node_idx].parent.sort()
    node_idx += 1

    # assign child node
    for i in range(node_idx):
        for j in range(len(node_list[i].parent)):
            node_list[node_list[i].parent[j]].child.append(i)
    for i in range(node_idx-1):
        while len(node_list[i].child) == 0:
            for j in reversed(range(node_idx-1)):
                if node_list[j].level > node_list[i].level:
                    if arc_deicision():
                        node_list[i].child.append(j)
                        node_list[j].parent.append(i)
                else:
                    break

    return node_list

def dag_check(node_list):
    for i in range(len(node_list)):
        assert(len(node_list[i].child) != 0 or i == len(node_list)-1)
        for child_idx in node_list[i].child:
            assert((i in node_list[child_idx].parent))
            assert((child_idx > i))

        assert(len(node_list[i].parent) != 0 or i == 0)  
        for parent_idx in node_list[i].parent:
            assert((i in node_list[parent_idx].child))
            assert((parent_idx < i))

def graph_visualize(node_list, html_path):
    edge_x, edge_y = [], []
    node_x, node_y = [], []
    node_text = []
    for node in node_list:
        # add node
        node_x.append(node.level)
        node_y.append(node.idx)
        node_text.append('Default Execution Time: ' + str(node.d_exec_t) + ", Callback Execution Time: " + str(node.c_exec_t))
        # add edge
        for child_node in node.child:
            edge_x.append(node.level)
            edge_x.append(node_list[child_node].level)
            edge_x.append(None)
            edge_y.append(node.idx)
            edge_y.append(node_list[child_node].idx)
            edge_y.append(None)
    
    edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

    node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=30,
        line_width=2))
    
    node_trace.text = node_text
    
    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    showarrow=False,
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    fig.write_html(html_path)

def find_all_paths(node_list, start_vertex, end_vertex, path=[]):
    path = path + [start_vertex]

    if start_vertex == end_vertex:
        return [path]

    if start_vertex not in node_list:
        return []
    
    paths = []
    for child_idx in start_vertex.child:
        vertex = node_list[child_idx]
        if vertex not in path:
            extened_paths = find_all_paths(node_list, vertex, end_vertex, path)
            for p in extened_paths:
                paths.append(p)
    
    return paths

def find_longest_execution_time_path_dfs(node_list, start_vertex, end_vertex):
    paths = find_all_paths(node_list, start_vertex, end_vertex)

    costs = []
    for path in paths:
        cost = 0
        for node in path:
            cost += node.c_exec_t
        costs.append(cost)

    (m, i) = max((v,i) for i,v in enumerate(costs))

    return m, paths[i]   

def execution_time_assign(node_list):
    paths = find_all_paths(node_list, node_list[0], node_list[len(node_list)-1])
    
    max_path_length, longest_execution_time = 0, 0
    for path in paths:
        if len(path) > max_path_length:
            max_path_length = len(path)

    c_exec_sum = 0
    for node in node_list:
        node.d_exec_t = random.randint(d_exec_range_[0] * 100, d_exec_range_[1] * 100)
        node.d_exec_t = float(node.d_exec_t/100)

        node.c_exec_t = float(random.randint(c_exec_range_[0], c_exec_range_[1]))
        c_exec_sum += node.c_exec_t

    longest_execution_time, longest_execution_time_path = find_longest_execution_time_path_dfs(node_list, node_list[0], node_list[len(node_list)-1])

    return node_list, c_exec_sum, max_path_length, longest_execution_time, longest_execution_time_path

def create_csv_file(node_list, csv_path):
    with open(csv_path, 'w', newline='') as csv_file:
        fieldnames = ['node_number', 'level', 'idx', 'priority', 'd_exec_t', 'c_exec_t', 'period', 'isSource', 'isSink', 'parent', 'child']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        
        num = 0
        for node in node_list:
            num += 1
            writer.writerow({'node_number': num, 'level': node.level, 'idx': node.idx, 'priority': node.priority, 
                             'd_exec_t': node.d_exec_t, 'c_exec_t': node.c_exec_t, 'period': node.period, 'isSource': node.isSource,
                             'isSink': node.isSink, 'parent': node.parent, 'child': node.child})

if __name__ == "__main__":
    parent_dir = os.getcwd()
    html_dir = parent_dir + '/html/'
    csv_dir = parent_dir + '/csv/raw_data/'
    for i in tqdm(range(dag_num_)):
        name = "DAG_" + str(i+1).zfill(3)
        html_path = html_dir + name + '.html'
        csv_path = csv_dir + name + '.csv'
        
        c_exec_sum, max_path_length, longest_execution_time, longest_execution_time_path = 0, 0, 0, []

        while c_exec_sum < c_exec_limit_[0] or c_exec_sum > c_exec_limit_[1] \
                or longest_execution_time < c_exec_sum * critical_execution_path_portion_ \
                or len(longest_execution_time_path) != max_path_length:
            node_list = dag_generate()
            dag_check(node_list)
            node_list, c_exec_sum, max_path_length, longest_execution_time, longest_execution_time_path = execution_time_assign(node_list)
            
        graph_visualize(node_list, html_path)
        create_csv_file(node_list, csv_path)
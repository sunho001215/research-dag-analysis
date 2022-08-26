import random
import os
import plotly.graph_objects as go

############# PARAM #############
dag_num_ = 10
# DAG generation parameter
depth_range_ = [2, 6]
max_parallelism_ = 4
arc_prob_ = 0.05
# Node execution time parameter
d_exec_range_ = [0.5, 2.5]
c_exec_range_ = [15, 40]
d_exec_limit_ = 35
c_exec_limit_ = 750
#################################

class Node(object):
    idx = 0
    def __init__(self):
        # Node Number
        self.idx = 1
        self.priority = 1

        # Execution Time
        self.d_exec_t = 0
        self.c_exec_t = 0
        self.period = 100 # ms

        # Graph Info
        self.parent = []
        self.child = []
        self.isSink = False
        self.isSource = False
        self.level = 0

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

def execution_time_assign(node_list):
    d_exec_sum, c_exec_sum = 1000, 1000

    while d_exec_sum > d_exec_limit_ and c_exec_sum > c_exec_limit_:
        d_exec_sum, c_exec_sum = 0, 0
        for node in node_list:
            node.d_exec_t = random.randint(d_exec_range_[0] * 10, d_exec_range_[1] * 10)
            node.d_exec_t = float(node.d_exec_t/10)
            d_exec_sum += node.d_exec_t

            node.c_exec_t = float(random.randint(c_exec_range_[0], c_exec_range_[1]))
            c_exec_sum += node.c_exec_t

    return node_list

if __name__ == "__main__":
    parent_dir = os.getcwd()
    html_dir = parent_dir + '/html/'
    csv_dir = parent_dir + '/csv/raw_data/'
    for i in range(dag_num_):
        name = "DAG_" + str(i+1).zfill(3)
        html_path = html_dir + name + '.html'
        csv_path = csv_dir + name + '.csv'

        node_list = dag_generate()
        dag_check(node_list)
        node_list = execution_time_assign(node_list)
        graph_visualize(node_list, html_path)
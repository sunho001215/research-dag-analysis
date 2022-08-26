import random

############# PARAM #############
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
        self.num = Node.idx
        Node.idx += 1
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

    for i in range(node_idx):
        print("node_idx: "+str(i)+", level: "+str(node_list[i].level)+", parent: "+str(node_list[i].parent)+", child: "+str(node_list[i].child))
    print(node_num)

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

def execution_time_assign(node_list):
    return node_list

if __name__ == "__main__":
    node_list = dag_generate()
    dag_check(node_list)
    node_list = execution_time_assign(node_list)
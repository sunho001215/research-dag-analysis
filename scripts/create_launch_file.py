import os
from spin_rate_optimization import read_csv_file
from xml.etree.ElementTree import Element, SubElement, ElementTree

def _pretty_print(current, parent=None, index=-1, depth=0):
    for i, node in enumerate(current):
        _pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = '\n' + ('\t' * depth)
        else:
            parent[index - 1].tail = '\n' + ('\t' * depth)
        if index == len(parent) - 1:
            current.tail = '\n' + ('\t' * (depth - 1))

def create_launch_file(node_list, file_path, attr):
    root = Element("launch")
    for idx in range(len(node_list)):
        node = node_list[idx]

        element = Element("node")
        element.set("pkg", "research-dag-analysis")
        element.set("type", "node"+str(node.priority + 1))
        element.set("name", "node"+str(node.priority + 1))
        element.set("output", "screen")
        root.append(element)

        child_node, parent_node = [], []
        for parent_idx in node.parent:
            parent_node.append(node_list[parent_idx].priority)
        for child_idx in node.child:
            child_node.append(node_list[child_idx].priority)

        sub_element1 = SubElement(element, "rosparam")
        sub_element1.text = str(parent_node)
        sub_element1.set("param", "parent_idx")

        sub_element2 = SubElement(element, "rosparam")
        sub_element2.text = str(child_node)
        sub_element2.set("param", "child_idx")

        sub_element3 = SubElement(element, "param")
        sub_element3.set("name", "default_waste_time")
        sub_element3.set("value", str(node.d_exec_t))

        sub_element4 = SubElement(element, "param")
        sub_element4.set("name", "callback_waste_time")
        sub_element4.set("value", str(node.c_exec_t - node.d_exec_t))

        sub_element5 = SubElement(element, "param")
        sub_element5.set("name", "period")
        if (attr == "single_instance_low_spin" or attr == "multi_instance_low_spin") and node.level != 0:
            sub_element5.set("value", str(100))
        elif (attr == "multi_instance_optimization_result" or attr == "multi_instance_low_spin") and node.level == 0:
            sub_element5.set("value", str(100))
        else:
            sub_element5.set("value", str(node.period))

    _pretty_print(root)
    tree = ElementTree(root)
    
    with open(file_path, "wb") as file:
        tree.write(file, encoding='utf-8', xml_declaration=False)


if __name__ == "__main__":
    parent_dir = os.getcwd()
    launch_file_dir = parent_dir + '/launch/'
    csv_dir = parent_dir + '/csv/optimization_result/'

    csv_list = []
    for path in os.listdir(csv_dir):
        if os.path.isfile(os.path.join(csv_dir, path)):
            csv_list.append(path)
    csv_list.sort()
    
    for file in csv_list:
        csv_dir = parent_dir + '/csv/raw_data/'
        node_list = read_csv_file(os.path.join(csv_dir, file))
        
        low_spin_path = launch_file_dir + 'single_instance_low_spin/' + file[0:-4] + '.launch'
        multi_instance_low_spin_path = launch_file_dir + 'multi_instance_low_spin/' + file[0:-4] + '.launch'

        create_launch_file(node_list, low_spin_path, "single_instance_low_spin")
        create_launch_file(node_list, multi_instance_low_spin_path, "multi_instance_low_spin")

        csv_dir = parent_dir + '/csv/optimization_result/'
        node_list = read_csv_file(os.path.join(csv_dir, file))

        optimization_result_path = launch_file_dir + 'single_instance_optimization_result/' + file[0:-4] + '.launch'
        multi_instance_optimization_result_path = launch_file_dir + 'multi_instance_optimization_result/' + file[0:-4] + '.launch'

        create_launch_file(node_list, optimization_result_path, "single_instance_optimization_result")
        create_launch_file(node_list, multi_instance_optimization_result_path, "multi_instance_optimization_result")
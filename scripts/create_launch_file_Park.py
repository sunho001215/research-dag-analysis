import os
from spin_rate_optimization import read_csv_file
from create_launch_file import create_launch_file

if __name__ == "__main__":
    parent_dir = os.getcwd()
    launch_file_dir = parent_dir + '/launch/'
    csv_dir = parent_dir + '/csv/optimization_result_Park/'

    csv_list = []
    for path in os.listdir(csv_dir):
        if os.path.isfile(os.path.join(csv_dir, path)):
            csv_list.append(path)
    csv_list.sort()
    
    for file in csv_list:
        node_list = read_csv_file(os.path.join(csv_dir, file))

        optimization_result_path = launch_file_dir + 'single_instance_Park/' + file[0:-4] + '.launch'

        create_launch_file(node_list, optimization_result_path, "single_instance_Park")
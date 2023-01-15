import os
from spin_rate_optimization import read_csv_file
from create_launch_file import create_launch_file

if __name__ == "__main__":
    parent_dir = os.getcwd()
    launch_file_dir = parent_dir + '/launch/'
    csv_dir = parent_dir + '/csv/optimization_result_He/'

    csv_list = []
    for path in os.listdir(csv_dir):
        if os.path.isfile(os.path.join(csv_dir, path)):
            csv_list.append(path)
    csv_list.sort()
    
    for file in csv_list:
        # csv_dir = parent_dir + '/csv/raw_data_He/'
        # node_list = read_csv_file(os.path.join(csv_dir, file))
        
        # low_spin_path = launch_file_dir + 'single_instance_low_spin_He/' + file[0:-4] + '.launch'
        # multi_instance_low_spin_path = launch_file_dir + 'multi_instance_low_spin_He/' + file[0:-4] + '.launch'

        # create_launch_file(node_list, low_spin_path, "single_instance_low_spin")
        # create_launch_file(node_list, multi_instance_low_spin_path, "multi_instance_low_spin")

        csv_dir = parent_dir + '/csv/optimization_result_He/'
        node_list = read_csv_file(os.path.join(csv_dir, file))

        optimization_result_path = launch_file_dir + 'single_instance_optimization_result_He/' + file[0:-4] + '.launch'
        multi_instance_optimization_result_path = launch_file_dir + 'multi_instance_optimization_result_He/' + file[0:-4] + '.launch'

        create_launch_file(node_list, optimization_result_path, "single_instance_optimization_result")
        create_launch_file(node_list, multi_instance_optimization_result_path, "multi_instance_optimization_result")
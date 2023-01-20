import os
import rospkg
import matplotlib.pyplot as plt
from spin_rate_experiment import get_avg_response_time, get_max_response_time, read_profiling_file, calculate_response_time
from spin_rate_optimization import node_priority_assign, optimize_spin_rate, read_csv_file, create_csv_file

def get_max_execution_time(file_path):
    callback_exeuction_time_list, default_execution_time_list = [], []

    with open(file_path, 'r') as f:
        line = f.readline()
        line = f.readline()
        while line:
            line_split = line.split(",")

            if int(line_split[5]) == 1:
                callback_exeuction_time_list.append(float(line_split[3])-float(line_split[2]))
            else:
                default_execution_time_list.append(float(line_split[3])-float(line_split[2]))

            line = f.readline()
    
    # callback_exeuction_time_list = callback_exeuction_time_list[100:-1000]
    # default_execution_time_list = default_execution_time_list[100:-1000]
    
    # plt.subplot(2, 1, 1)
    # plt.title(file_path)
    # plt.plot(callback_exeuction_time_list)
    # plt.subplot(2, 1, 2)
    # plt.plot(default_execution_time_list)
    # plt.show()

    return get_max_response_time(callback_exeuction_time_list), get_max_response_time(default_execution_time_list)

if __name__ == "__main__":
    rospack = rospkg.RosPack()
    pkg_path = rospack.get_path("research-dag-analysis")
    result_dir = pkg_path + "/Autoware/before/"

    entry_file_path= result_dir + "lidar_republisher.csv"
    leaf_file_path = result_dir + "twist_gate.csv"

    start_idx_list, end_idx_list, start_time_list, end_time_list = read_profiling_file(entry_file_path, leaf_file_path)
    response_time_list = calculate_response_time(start_idx_list, end_idx_list, start_time_list, end_time_list)

    print("Before Optmization")
    print("Average: " + str(get_avg_response_time(response_time_list)))
    print("Worst-Case: " + str(get_max_response_time(response_time_list)))
    print("")

    result_dir = pkg_path + "/Autoware/before/"

    csv_list = []
    for path in os.listdir(result_dir):
        if os.path.isfile(os.path.join(result_dir, path)):
            csv_list.append(path)
    csv_list.sort()

    for file_name in csv_list:
        file_path = result_dir + file_name
        
        CE, DE = get_max_execution_time(file_path)
        
        # print(file_name)
        # print("Callback Exeuction Time : " + str(CE))
        # print("Default Execution time : " + str(DE))
    
    raw_data = pkg_path + "/Autoware/raw_data.csv"
    save_path = pkg_path + "/Autoware/optimization_result.csv"

    node_list = read_csv_file(raw_data)
    node_list = optimize_spin_rate(node_list, raw_data)
    node_list = node_priority_assign(node_list)
    create_csv_file(node_list, save_path)

    result_dir = pkg_path + "/Autoware/after/"

    entry_file_path= result_dir + "lidar_republisher.csv"
    leaf_file_path = result_dir + "twist_gate.csv"

    start_idx_list, end_idx_list, start_time_list, end_time_list = read_profiling_file(entry_file_path, leaf_file_path)
    response_time_list = calculate_response_time(start_idx_list, end_idx_list, start_time_list, end_time_list)

    print("After Optmization")
    print("Average: " + str(get_avg_response_time(response_time_list)))
    print("Worst-Case: " + str(get_max_response_time(response_time_list)))
    print("")
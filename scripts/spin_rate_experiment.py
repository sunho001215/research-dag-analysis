import os
import signal
import psutil
import rospkg
import csv
import shutil
import subprocess
from tqdm import trange
from time import sleep

########### PARAM ###########
dag_num_ = 100
iter_num_ = 8
test_exec_time_ = 25
#############################

def kill_via_pid(pid):
    os.kill(pid, signal.SIGTERM)

def kill_all_ros_node():
    for proc in psutil.process_iter():
        processName = proc.name()
        processID = proc.pid
        if "ros" in processName or "node" in processName:
            os.kill(processID, signal.SIGTERM)

def ros_fork_execute(test_cmd):
    pid = os.fork()
    if pid == 0:
        os.system(test_cmd + " > /dev/null")
        return
    
    sleep(test_exec_time_)
    kill_via_pid(pid)
    kill_all_ros_node()
    sleep(0.1)

def calculate_response_time(start_idx_list, end_idx_list, start_time_list, end_time_list):
    response_time_list = []

    start_idx_len = len(start_idx_list)
    end_idx_len = len(end_idx_list)

    start_idx, end_idx = 0, 0
    while True:
        if not start_idx < start_idx_len:
            break
        if not end_idx < end_idx_len:
            break

        if start_idx_list[start_idx] == end_idx_list[end_idx]:
            response_time_list.append(end_time_list[end_idx] - start_time_list[start_idx])
            start_idx = start_idx + 1
            end_idx = end_idx + 1
        elif start_idx_list[start_idx] > end_idx_list[end_idx]:
            end_idx = end_idx + 1
        else:
            start_idx = start_idx + 1
            
    return response_time_list

def get_avg_response_time(response_time):
    sum = 0
    for value in response_time:
        sum += value
    return sum / len(response_time)

def get_max_response_time(response_time):
    max = 0
    for value in response_time:
        if(value > max):
            max = value
    return max

def calculate_response_time(start_idx_list, end_idx_list, start_time_list, end_time_list):
    response_time_list = []

    start_idx_len = len(start_idx_list)
    end_idx_len = len(end_idx_list)

    start_idx, end_idx = 0, 0
    while True:
        if not start_idx < start_idx_len:
            break
        if not end_idx < end_idx_len:
            break

        if start_idx_list[start_idx] == end_idx_list[end_idx]:
            response_time_list.append(end_time_list[end_idx] - start_time_list[start_idx])
            start_idx = start_idx + 1
            end_idx = end_idx + 1
        elif start_idx_list[start_idx] > end_idx_list[end_idx]:
            end_idx = end_idx + 1
        else:
            start_idx = start_idx + 1
            
    return response_time_list

def read_profiling_file(entry_file_path, leaf_file_path):
    start_idx_list, end_idx_list, start_time_list, end_time_list = [], [], [], []

    with open(entry_file_path, 'r') as f:
        line = f.readline()
        line = f.readline()
        while line:
            line_split = line.split(",")

            if int(line_split[5]) == 1:
                start_idx = int(line_split[4])
                start_time = float(line_split[2])
            
                start_idx_list.append(start_idx)
                start_time_list.append(start_time)

            line = f.readline()

    with open(leaf_file_path, 'r') as f:
        line = f.readline()
        line = f.readline()
        while line:
            line_split = line.split(",")

            if int(line_split[5]) == 1:
                end_idx = int(line_split[4])
                end_time = float(line_split[3])
            
                end_idx_list.append(end_idx)
                end_time_list.append(end_time)

            line = f.readline()
    
    return start_idx_list, end_idx_list, start_time_list, end_time_list

def get_response_time(pkg_path):
    profiling_path = pkg_path + "/profiling/"
    profiling_list = os.listdir(profiling_path)
    node_num = len(profiling_list)

    entry_file_path = pkg_path + "/profiling/node1.csv"
    leaf_file_path = pkg_path + "/profiling/node"+ str(node_num) +".csv"

    start_idx_list, end_idx_list, start_time_list, end_time_list = read_profiling_file(entry_file_path, leaf_file_path)
    response_time_list = calculate_response_time(start_idx_list, end_idx_list, start_time_list, end_time_list)

    max_response_time = get_max_response_time(response_time_list[2:])
    avg_response_time = get_avg_response_time(response_time_list[2:])

    return max_response_time, avg_response_time

def do_experiment(test_cmd, pkg_path):
    max_response_time_list = []
    avg_response_time_list = []
    for i in range(iter_num_):
        ros_fork_execute(test_cmd)
        max_response_time, avg_response_time = get_response_time(pkg_path)
        max_response_time_list.append(max_response_time)
        avg_response_time_list.append(avg_response_time)
    
    return get_avg_response_time(max_response_time_list), get_avg_response_time(avg_response_time_list)


if __name__ == "__main__":
    rospack = rospkg.RosPack()
    pkg_path = rospack.get_path("research-dag-analysis")
    profiling_path = pkg_path + "/profiling/"

    launch_dir = pkg_path + "/launch/single_instance_low_spin/"
    launch_list = []
    for path in os.listdir(launch_dir):
        if os.path.isfile(os.path.join(launch_dir, path)):
            launch_list.append(path)
    launch_list.sort()

    #############################
    for i in trange(dag_num_):
        if os.path.exists(profiling_path):
            shutil.rmtree(profiling_path)
        os.mkdir(profiling_path)

        # low spin rate experiment
        cmd = "taskset -c 8,9,10,11 roslaunch " + pkg_path + "/launch/single_instance_low_spin/" + launch_list[i]
        low_spin_result = do_experiment(cmd, pkg_path)
        
        # optimization result experiment
        cmd = "taskset -c 8,9,10,11 roslaunch " + pkg_path + "/launch/single_instance_optimization_result/" + launch_list[i]
        optimization_result = do_experiment(cmd, pkg_path)

        result_path = pkg_path + "/result/single-instance_4-core_w-priority-assignment/" + launch_list[i][0:-7] + ".csv"
        f = open(result_path, 'w', newline="")

        wr = csv.writer(f)
        wr.writerow(["low_spin_rate"])
        wr.writerow(["max_response_time", low_spin_result[0]])
        wr.writerow(["avg_response_time", low_spin_result[1]])

        wr.writerow(["optimization_result"])
        wr.writerow(["max_response_time", optimization_result[0]])
        wr.writerow(["avg_response_time", optimization_result[1]])

        f.close()

        # multi-instance low spin rate experiment
        cmd = "taskset -c 8,9,10,11 roslaunch " + pkg_path + "/launch/multi_instance_low_spin/" + launch_list[i]
        low_spin_result = do_experiment(cmd, pkg_path)
        
        # multi-instance optimization result experiment
        cmd = "taskset -c 8,9,10,11 roslaunch " + pkg_path + "/launch/multi_instance_optimization_result/" + launch_list[i]
        optimization_result = do_experiment(cmd, pkg_path)

        result_path = pkg_path + "/result/multi-instance_4-core_w-priority-assignment/" + launch_list[i][0:-7] + ".csv"
        f = open(result_path, 'w', newline="")

        wr = csv.writer(f)
        wr.writerow(["low_spin_rate"])
        wr.writerow(["max_response_time", low_spin_result[0]])
        wr.writerow(["avg_response_time", low_spin_result[1]])

        wr.writerow(["optimization_result"])
        wr.writerow(["max_response_time", optimization_result[0]])
        wr.writerow(["avg_response_time", optimization_result[1]])

        f.close()
    #############################

    os.system("sudo chrt -r -p 99 10")
    os.system("sudo chrt -r -p 99 23")
    os.system("sudo chrt -r -p 99 31")
    os.system("sudo chrt -r -p 99 39")
    os.system("sudo chrt -r -p 99 47")
    os.system("sudo chrt -r -p 99 55")
    os.system("sudo chrt -r -p 99 63")
    os.system("sudo chrt -r -p 99 71")
    os.system("sudo chrt -r -p 99 79")
    os.system("sudo chrt -r -p 99 87")
    os.system("sudo chrt -r -p 99 95")
    os.system("sudo chrt -r -p 99 103")
    sleep(1)

    #############################
    for i in trange(dag_num_):
        if os.path.exists(profiling_path):
            shutil.rmtree(profiling_path)
        os.mkdir(profiling_path)

        # low spin rate experiment
        cmd = "taskset -c 8,9,10,11 roslaunch " + pkg_path + "/launch/single_instance_low_spin/" + launch_list[i]
        low_spin_result = do_experiment(cmd, pkg_path)
        
        # optimization result experiment
        cmd = "taskset -c 8,9,10,11 roslaunch " + pkg_path + "/launch/single_instance_optimization_result/" + launch_list[i]
        optimization_result = do_experiment(cmd, pkg_path)

        result_path = pkg_path + "/result/single-instance_4-core_w-ksoftirq-opt_w-priority-assignment/" + launch_list[i][0:-7] + ".csv"
        f = open(result_path, 'w', newline="")

        wr = csv.writer(f)
        wr.writerow(["low_spin_rate"])
        wr.writerow(["max_response_time", low_spin_result[0]])
        wr.writerow(["avg_response_time", low_spin_result[1]])

        wr.writerow(["optimization_result"])
        wr.writerow(["max_response_time", optimization_result[0]])
        wr.writerow(["avg_response_time", optimization_result[1]])

        f.close()

        # multi-instance low spin rate experiment
        cmd = "taskset -c 8,9,10,11 roslaunch " + pkg_path + "/launch/multi_instance_low_spin/" + launch_list[i]
        low_spin_result = do_experiment(cmd, pkg_path)
        
        # multi-instance optimization result experiment
        cmd = "taskset -c 8,9,10,11 roslaunch " + pkg_path + "/launch/multi_instance_optimization_result/" + launch_list[i]
        optimization_result = do_experiment(cmd, pkg_path)

        result_path = pkg_path + "/result/multi-instance_4-core_w-ksoftirq-opt_w-priority-assignment/" + launch_list[i][0:-7] + ".csv"
        f = open(result_path, 'w', newline="")

        wr = csv.writer(f)
        wr.writerow(["low_spin_rate"])
        wr.writerow(["max_response_time", low_spin_result[0]])
        wr.writerow(["avg_response_time", low_spin_result[1]])

        wr.writerow(["optimization_result"])
        wr.writerow(["max_response_time", optimization_result[0]])
        wr.writerow(["avg_response_time", optimization_result[1]])

        f.close()
    #############################
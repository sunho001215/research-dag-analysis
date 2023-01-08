import os
import rospkg
import csv
import shutil
from tqdm import trange
from spin_rate_experiment import do_experiment, dag_num_

if __name__ == "__main__":
    rospack = rospkg.RosPack()
    pkg_path = rospack.get_path("research-dag-analysis")
    profiling_path = pkg_path + "/profiling/"

    launch_dir = pkg_path + "/launch/single_instance_Park/"
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

        optimization_result_csv_path = pkg_path + "/csv/optimization_result_Park/" + launch_list[i][0:-7] + ".csv"

        # optimization result experiment
        cmd = "taskset -c 8,9,10,11 roslaunch " + pkg_path + "/launch/single_instance_Park/" + launch_list[i]
        optimization_result = do_experiment(cmd, pkg_path, optimization_result_csv_path)

        result_path = pkg_path + "/result/single-instance_4-core_Park/" + launch_list[i][0:-7] + ".csv"
        f = open(result_path, 'w', newline="")

        wr = csv.writer(f)

        wr.writerow(["optimization_result"])
        wr.writerow(["max_response_time", optimization_result[0]])
        wr.writerow(["avg_response_time", optimization_result[1]])

        f.close()
    #############################
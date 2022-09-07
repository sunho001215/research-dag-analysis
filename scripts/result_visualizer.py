import os
import csv

########### PARAM ###########
dag_num_ = 100
#############################

def read_data(file_path):
    f = open(file_path, 'r', newline="")
    rd = csv.reader(f)
    
    idx = 0
    num1, num2, num3, num4 = 0, 0, 0, 0
    for row in rd:
        if idx == 1:
            num1 = float(row[1])
        elif idx == 2:
            num2 = float(row[1])
        elif idx == 4:
            num3 = float(row[1])
        elif idx == 5:
            num4 = float(row[1])
        idx += 1
    f.close()

    return num1, num2, num3, num4


if __name__ == "__main__":
    parent_dir = os.getcwd()
    result_dir = parent_dir + "/result/"
    
    ## O1 : Spin Rate Optimization
    ## O2 : High <ksoftirqd> Thread Priority
    ## O3 : Topological Order Priority Assignment

    single_instance_max = []
    single_instance_O1_max = []
    single_instance_O2_max = []
    single_instance_O3_max = []
    single_instance_O1_O2_max = []
    single_instance_O1_O3_max = []
    single_instance_O2_O3_max = []
    single_instance_O1_O2_O3_max = []

    multi_instance_max = []
    multi_instance_O1_max = []
    multi_instance_O2_max = []
    multi_instance_O3_max = []
    multi_instance_O1_O2_max = []
    multi_instance_O1_O3_max = []
    multi_instance_O2_O3_max = []
    multi_instance_O1_O2_O3_max = []

    single_instance_avg = []
    single_instance_O1_avg = []
    single_instance_O2_avg = []
    single_instance_O3_avg = []
    single_instance_O1_O2_avg = []
    single_instance_O1_O3_avg = []
    single_instance_O2_O3_avg = []
    single_instance_O1_O2_O3_avg = []

    multi_instance_avg = []
    multi_instance_O1_avg = []
    multi_instance_O2_avg = []
    multi_instance_O3_avg = []
    multi_instance_O1_O2_avg = []
    multi_instance_O1_O3_avg = []
    multi_instance_O2_O3_avg = []
    multi_instance_O1_O2_O3_avg = []

    for i in range(dag_num_):
        name = "DAG_" + str(i+1).zfill(3)
        ## Single-Instance Experiment Result
        file_path = result_dir + "single-instance_4-core/" + name + ".csv"
        n1, n2, n3, n4 =read_data(file_path)
        base_val = n1
        single_instance_max.append(n1/base_val)
        single_instance_avg.append(n2/base_val)
        single_instance_O1_max.append(n3/base_val)
        single_instance_O1_avg.append(n4/base_val)
        
        ## Multi-Instance Experiment Result

    
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

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

def list_average(lst):
    if len(lst) == 0:
        return 0
    return sum(lst)/len(lst)

# ( , O3, O2, O2_O3, O1, O1_O3, O1_O2, O1_O2_O3)
def create_histogram(save_path, single_instance_values, multi_instance_values):
    x = np.arange(8)
    xticks = ["", "X\nX\nX", "X\nX\nO", "X\nO\nX", "X\nO\nO", \
              "O\nX\nX", "O\nX\nO", "O\nO\nX", "O\nO\nO"]
    yticks = ["", "", "0.5", "", "1", "", "1.5", "", "2.0"]

    fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(14,6))

    ax0.bar(np.arange(8), single_instance_values, color="dimgray")
    ax0.set_title("Single Instance")
    ax0.set_ylabel("Normalized Response Time", multialignment='center')
    ax0.set_xticklabels(xticks)
    ax0.set_yticklabels(yticks)
    ax0.set_ylim(bottom = 0.0, top = 2.0)

    ax1.bar(np.arange(8), multi_instance_values, color="dimgray")
    ax1.set_title("Multiple Instance")
    ax1.set_ylabel("Normalized Response Time", multialignment='center')
    ax1.set_xticklabels(xticks)
    ax1.set_yticklabels(yticks)
    ax1.set_ylim(bottom = 0.0, top = 2.0)

    ax0.set_xlabel("Spin Rate Optimization\nHigh <ksoftirqd> Priority\nTopological Order Priority", fontsize = 10, loc="left")
    ax0.xaxis.set_label_coords(-0.34,-0.02)

    plt.savefig(save_path)


if __name__ == "__main__":
    parent_dir = os.getcwd()
    result_dir = parent_dir + "/result/"
    
    ## O1 : Spin Rate Optimization
    ## O2 : High <ksoftirqd> Thread Priority
    ## O3 : Topological Order Priority Assignment

    single_instance_max, single_instance_O1_max, single_instance_O2_max, single_instance_O3_max, \
    single_instance_O1_O2_max, single_instance_O1_O3_max, single_instance_O2_O3_max, single_instance_O1_O2_O3_max \
    = [], [], [], [], [], [], [] ,[]

    single_instance_avg, single_instance_O1_avg, single_instance_O2_avg, single_instance_O3_avg, \
    single_instance_O1_O2_avg, single_instance_O1_O3_avg, single_instance_O2_O3_avg, single_instance_O1_O2_O3_avg \
    = [], [], [], [], [], [], [] ,[]

    multi_instance_max, multi_instance_O1_max, multi_instance_O2_max, multi_instance_O3_max, \
    multi_instance_O1_O2_max, multi_instance_O1_O3_max, multi_instance_O2_O3_max, multi_instance_O1_O2_O3_max \
    = [], [], [], [], [], [], [] ,[]

    multi_instance_avg, multi_instance_O1_avg, multi_instance_O2_avg, multi_instance_O3_avg, \
    multi_instance_O1_O2_avg, multi_instance_O1_O3_avg, multi_instance_O2_O3_avg, multi_instance_O1_O2_O3_avg \
    = [], [], [], [], [], [], [] ,[]


    for i in range(dag_num_):
        name = "DAG_" + str(i+1).zfill(3)
        ## Single-Instance Experiment Result
        file_path = result_dir + "single-instance_4-core/" + name + ".csv"
        n1, n2, n3, n4 =read_data(file_path)
        base_max = n1
        base_avg = n2
        single_instance_max.append(n1/base_max)
        single_instance_avg.append(n2/base_avg)
        single_instance_O1_max.append(n3/base_max)
        single_instance_O1_avg.append(n4/base_avg)

        file_path = result_dir + "single-instance_4-core_w-ksoftirq-opt/" + name + ".csv"
        n1, n2, n3, n4 =read_data(file_path)
        single_instance_O2_max.append(n1/base_max)
        single_instance_O2_avg.append(n2/base_avg)
        single_instance_O1_O2_max.append(n3/base_max)
        single_instance_O1_O2_avg.append(n4/base_avg)

        file_path = result_dir + "single-instance_4-core_w-priority-assignment/" + name + ".csv"
        n1, n2, n3, n4 =read_data(file_path)
        single_instance_O3_max.append(n1/base_max)
        single_instance_O3_avg.append(n2/base_avg)
        single_instance_O1_O3_max.append(n3/base_max)
        single_instance_O1_O3_avg.append(n4/base_avg)

        file_path = result_dir + "single-instance_4-core_w-ksoftirq-opt_w-priority-assignment/" + name + ".csv"
        n1, n2, n3, n4 =read_data(file_path)
        single_instance_O2_O3_max.append(n1/base_max)
        single_instance_O2_O3_avg.append(n2/base_avg)
        single_instance_O1_O2_O3_max.append(n3/base_max)
        single_instance_O1_O2_O3_avg.append(n4/base_avg)
        
        ## Multi-Instance Experiment Result

        file_path = result_dir + "multi-instance_4-core/" + name + ".csv"
        n1, n2, n3, n4 =read_data(file_path)
        base_max = n1
        base_avg = n2
        multi_instance_max.append(n1/base_max)
        multi_instance_avg.append(n2/base_avg)
        multi_instance_O1_max.append(n3/base_max)
        multi_instance_O1_avg.append(n4/base_avg)

        file_path = result_dir + "multi-instance_4-core_w-ksoftirq-opt/" + name + ".csv"
        n1, n2, n3, n4 =read_data(file_path)
        multi_instance_O2_max.append(n1/base_max)
        multi_instance_O2_avg.append(n2/base_avg)
        multi_instance_O1_O2_max.append(n3/base_max)
        multi_instance_O1_O2_avg.append(n4/base_avg)

        file_path = result_dir + "multi-instance_4-core_w-priority-assignment/" + name + ".csv"
        n1, n2, n3, n4 =read_data(file_path)
        multi_instance_O3_max.append(n1/base_max)
        multi_instance_O3_avg.append(n2/base_avg)
        multi_instance_O1_O3_max.append(n3/base_max)
        multi_instance_O1_O3_avg.append(n4/base_avg)

        file_path = result_dir + "multi-instance_4-core_w-ksoftirq-opt_w-priority-assignment/" + name + ".csv"
        n1, n2, n3, n4 =read_data(file_path)
        multi_instance_O2_O3_max.append(n1/base_max)
        multi_instance_O2_O3_avg.append(n2/base_avg)
        multi_instance_O1_O2_O3_max.append(n3/base_max)
        multi_instance_O1_O2_O3_avg.append(n4/base_avg)

    single_instance_max = list_average(single_instance_max)
    single_instance_O1_max = list_average(single_instance_O1_max)
    single_instance_O2_max = list_average(single_instance_O2_max)
    single_instance_O3_max = list_average(single_instance_O3_max)
    single_instance_O1_O2_max = list_average(single_instance_O1_O2_max)
    single_instance_O1_O3_max = list_average(single_instance_O1_O3_max)
    single_instance_O2_O3_max = list_average(single_instance_O2_O3_max)
    single_instance_O1_O2_O3_max = list_average(single_instance_O1_O2_O3_max)

    single_instance_avg = list_average(single_instance_avg)
    single_instance_O1_avg = list_average(single_instance_O1_avg)
    single_instance_O2_avg = list_average(single_instance_O2_avg)
    single_instance_O3_avg = list_average(single_instance_O3_avg)
    single_instance_O1_O2_avg = list_average(single_instance_O1_O2_avg)
    single_instance_O1_O3_avg = list_average(single_instance_O1_O3_avg)
    single_instance_O2_O3_avg = list_average(single_instance_O2_O3_avg)
    single_instance_O1_O2_O3_avg = list_average(single_instance_O1_O2_O3_avg)

    multi_instance_max = list_average(multi_instance_max)
    multi_instance_O1_max = list_average(multi_instance_O1_max)
    multi_instance_O2_max = list_average(multi_instance_O2_max)
    multi_instance_O3_max = list_average(multi_instance_O3_max)
    multi_instance_O1_O2_max = list_average(multi_instance_O1_O2_max)
    multi_instance_O1_O3_max = list_average(multi_instance_O1_O3_max)
    multi_instance_O2_O3_max = list_average(multi_instance_O2_O3_max)
    multi_instance_O1_O2_O3_max = list_average(multi_instance_O1_O2_O3_max)

    multi_instance_avg = list_average(multi_instance_avg)
    multi_instance_O1_avg = list_average(multi_instance_O1_avg)
    multi_instance_O2_avg = list_average(multi_instance_O2_avg)
    multi_instance_O3_avg = list_average(multi_instance_O3_avg)
    multi_instance_O1_O2_avg = list_average(multi_instance_O1_O2_avg)
    multi_instance_O1_O3_avg = list_average(multi_instance_O1_O3_avg)
    multi_instance_O2_O3_avg = list_average(multi_instance_O2_O3_avg)
    multi_instance_O1_O2_O3_avg = list_average(multi_instance_O1_O2_O3_avg)
    
    create_histogram(parent_dir + "/histogram/4-core_max.png", [single_instance_max, single_instance_O3_max, \
                     single_instance_O2_max, single_instance_O2_O3_max, single_instance_O1_max, single_instance_O1_O3_max, \
                     single_instance_O1_O2_max, single_instance_O1_O2_O3_max], [multi_instance_max, multi_instance_O3_max, \
                     multi_instance_O2_max, multi_instance_O2_O3_max, multi_instance_O1_max, multi_instance_O1_O3_max, \
                     multi_instance_O1_O2_max, multi_instance_O1_O2_O3_max])
    
    create_histogram(parent_dir + "/histogram/4-core_avg.png", [single_instance_avg, single_instance_O3_avg, \
                     single_instance_O2_avg, single_instance_O2_O3_avg, single_instance_O1_avg, single_instance_O1_O3_avg, \
                     single_instance_O1_O2_avg, single_instance_O1_O2_O3_avg], [multi_instance_avg, multi_instance_O3_avg, \
                     multi_instance_O2_avg, multi_instance_O2_O3_avg, multi_instance_O1_avg, multi_instance_O1_O3_avg, \
                     multi_instance_O1_O2_avg, multi_instance_O1_O2_O3_avg])
    
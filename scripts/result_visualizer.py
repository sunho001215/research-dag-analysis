from cProfile import label
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

def create_histogram_value_Park_He(save_path, single_instance_values, multi_instance_values):
    multi_instance_values[1] = multi_instance_values[1] / multi_instance_values[0]
    multi_instance_values[2] = multi_instance_values[2] / multi_instance_values[0]
    multi_instance_values[0] = multi_instance_values[0] / multi_instance_values[0]

    xticks_1 = ["Base", "Park", "Ours"]
    xticks_2 = ["Base", "He", "Ours"]
    yticks = ["0", "0.5", "1", "1.2"]

    fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(12,6))
    
    ax0.bar(np.arange(3), single_instance_values, color="dimgray")
    ax0.set_title("Performance Comparison")
    ax0.set_ylabel("Normalized Response Time", multialignment='center')
    ax0.set_xticks([0, 1, 2])
    ax0.set_xticklabels(xticks_1)
    ax0.set_yticks([0, 0.5, 1, 1.2])
    ax0.set_yticklabels(yticks)
    ax0.set_ylim(bottom = 0.0, top = 1.2)

    ax1.bar(np.arange(3), multi_instance_values, color="dimgray")
    ax1.set_title("Performance Comparison")
    ax1.set_ylabel("Normalized Response Time", multialignment='center')
    ax1.set_xticks([0, 1, 2])
    ax1.set_xticklabels(xticks_2)
    ax1.set_yticks([0, 0.5, 1, 1.2])
    ax1.set_yticklabels(yticks)
    ax1.set_ylim(bottom = 0.0, top = 1.2)

    ax0.xaxis.set_label_coords(0.17,-0.075)

    ax1.xaxis.set_label_coords(0.17,-0.075)

    print(single_instance_values)
    print(multi_instance_values)

    plt.savefig(save_path)

# ( , O3, O2, O2_O3, O1, O1_O3, O1_O2, O1_O2_O3)
def create_histogram_value(save_path, single_instance_values, multi_instance_values):
    x = np.arange(8)
    # xticks = ["X\nX\nX", "X\nX\nO", "X\nO\nX", "X\nO\nO", \
    #           "O\nX\nX", "O\nX\nO", "O\nO\nX", "O\nO\nO"]
    xticks = ["(X,X,X)", "(X,X,O)", "(X,O,X)", "(X,O,O)", \
              "(O,X,X)", "(O,X,O)", "(O,O,X)", "(O,O,O)"]
    yticks = ["0", "0.5", "1", "1.5", "2"]

    fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(14,6))

    ax0.bar(np.arange(8), single_instance_values, color="dimgray")
    ax0.set_title("Single Instance")
    ax0.set_ylabel("Normalized Response Time", multialignment='center')
    ax0.set_xticks([0, 1, 2, 3, 4, 5, 6, 7])
    ax0.set_xticklabels(xticks)
    ax0.set_yticks([0, 0.5, 1, 1.5, 2])
    ax0.set_yticklabels(yticks)
    ax0.set_ylim(bottom = 0.0, top = 2.0)

    ax1.bar(np.arange(8), multi_instance_values, color="dimgray")
    ax1.set_title("Multiple Instance")
    ax1.set_ylabel("Normalized Response Time", multialignment='center')
    ax1.set_xticks([0, 1, 2, 3, 4, 5, 6, 7])
    ax1.set_xticklabels(xticks)
    ax1.set_yticks([0, 0.5, 1, 1.5, 2])
    ax1.set_yticklabels(yticks)
    ax1.set_ylim(bottom = 0.0, top = 2.0)

    ax0.set_xlabel("(Optimization A, Optimization B, Optimization C)", fontsize = 10, loc="left")
    ax0.xaxis.set_label_coords(0.17,-0.075)

    ax1.set_xlabel("(Optimization A, Optimization B, Optimization C)", fontsize = 10, loc="left")
    ax1.xaxis.set_label_coords(0.17,-0.075)

    print(single_instance_values)
    print(multi_instance_values)

    plt.savefig(save_path)

# (O1, O1_O3, O1_O2, O1_O2_O3)
def create_histogram_count(save_path, single_instance_values, multi_instance_values, real_length):
    labels = ["0.12", "0.16", "0.20", "0.24", "0.28"]
    O1_count = [0, 0, 0, 0, 0]
    O1_O3_count = [0, 0, 0, 0, 0]
    O1_O2_count = [0, 0, 0, 0, 0]
    O1_O2_O3_count = [0, 0, 0, 0, 0]

    # for i in range(len(single_instance_values[0])):
    #     if single_instance_values[0][i] < single_instance_values[1][i] and \
    #         single_instance_values[0][i] < single_instance_values[2][i] and \
    #         single_instance_values[0][i] < single_instance_values[3][i]:
    #         O1_count[0] += 1
    #     elif single_instance_values[1][i] < single_instance_values[0][i] and \
    #         single_instance_values[1][i] < single_instance_values[2][i] and \
    #         single_instance_values[1][i] < single_instance_values[3][i]:
    #         O1_O3_count[0] += 1
    #     elif single_instance_values[2][i] < single_instance_values[0][i] and \
    #         single_instance_values[2][i] < single_instance_values[1][i] and \
    #         single_instance_values[2][i] < single_instance_values[3][i]:
    #         O1_O2_count[0] += 1
    #     else:
    #         O1_O2_O3_count[0] += 1
    
    for i in range(len(multi_instance_values[0])):
        idx = int((real_length[i]-0.1) / (0.04))
        if multi_instance_values[0][i] < multi_instance_values[1][i] and \
            multi_instance_values[0][i] < multi_instance_values[2][i] and \
            multi_instance_values[0][i] < multi_instance_values[3][i]:
            O1_count[idx] += 1
        elif multi_instance_values[1][i] < multi_instance_values[0][i] and \
            multi_instance_values[1][i] < multi_instance_values[2][i] and \
            multi_instance_values[1][i] < multi_instance_values[3][i]:
            O1_O3_count[idx] += 1
        elif multi_instance_values[2][i] < multi_instance_values[0][i] and \
            multi_instance_values[2][i] < multi_instance_values[1][i] and \
            multi_instance_values[2][i] < multi_instance_values[3][i]:
            O1_O2_count[idx] += 1
        else:
            O1_O2_O3_count[idx] += 1 

    for i in range(5):
        cnt = O1_count[i] + O1_O2_count[i] + O1_O3_count[i] + O1_O2_O3_count[i]
        O1_count[i] = O1_count[i] * 100 / cnt
        O1_O2_count[i] = O1_O2_count[i] * 100 / cnt
        O1_O3_count[i] = O1_O3_count[i] * 100 / cnt
        O1_O2_O3_count[i] = O1_O2_O3_count[i] * 100 / cnt

    width = 0.6       # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    p1 = ax.bar(labels, O1_count, width, bottom=[a + b + c for a, b, c in zip(O1_O2_count, O1_O3_count, O1_O2_O3_count)], \
            label='A', color='lightgrey')
    p2 = ax.bar(labels, O1_O2_count, width, bottom=[a + b for a, b in zip(O1_O3_count, O1_O2_O3_count)], label='A+B',\
            color='darkgray')
    p3 = ax.bar(labels, O1_O3_count, width, bottom=O1_O2_O3_count,\
            label='A+C', color='dimgray')
    p4 = ax.bar(labels, O1_O2_O3_count, width, \
            label='A+B+C', color='black')

    ax.set_xlabel('Instance Length (s)')
    ax.set_ylabel('Ratio (%)')
    ax.set_title('Best-Performance Settings')
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.65, box.height])
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # plt.bar_label(p1, label_type='center')
    # plt.bar_label(p2, label_type='center')
    # plt.bar_label(p3, label_type='center')
    # plt.bar_label(p4, label_type='center')

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

    single_instance_Park_avg, single_instance_Park_max = [], []

    single_instance_He_avg, single_instance_He_max = [], []
    multi_instance_He_avg, multi_instance_He_max = [], []

    real_length = []
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

        real_length.append(n3)

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

        ## Park Experiment Result

        file_path = result_dir + "single-instance_4-core_Park/" + name + ".csv"
        n1, n2, n3, n4 =read_data(file_path)
        single_instance_Park_max.append(n1/base_max)
        single_instance_Park_avg.append(n2/base_avg)

        ## He Experiment Result

        file_path = result_dir + "single-instance_4-core_He/" + name + ".csv"
        n1, n2, n3, n4 =read_data(file_path)
        single_instance_He_max.append(n1/base_max)
        single_instance_He_avg.append(n2/base_avg)

        file_path = result_dir + "multi-instance_4-core_He/" + name + ".csv"
        n1, n2, n3, n4 =read_data(file_path)
        multi_instance_He_max.append(n1/base_max)
        multi_instance_He_avg.append(n2/base_avg)


    create_histogram_count(parent_dir + "/histogram/4-core_max_count.png", [single_instance_O1_max, single_instance_O1_O3_max, \
                     single_instance_O1_O2_max, single_instance_O1_O2_O3_max], [multi_instance_O1_max, multi_instance_O1_O3_max, \
                     multi_instance_O1_O2_max, multi_instance_O1_O2_O3_max], real_length)
    
    # create_histogram_count(parent_dir + "/histogram/4-core_avg_count.png", [single_instance_O1_avg, single_instance_O1_O3_avg, \
    #                  single_instance_O1_O2_avg, single_instance_O1_O2_O3_avg], [multi_instance_O1_avg, multi_instance_O1_O3_avg, \
    #                  multi_instance_O1_O2_avg, multi_instance_O1_O2_O3_avg])

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
    
    single_instance_Park_max = list_average(single_instance_Park_max)
    single_instance_Park_avg = list_average(single_instance_Park_avg)

    single_instance_He_max = list_average(single_instance_He_max)
    single_instance_He_avg = list_average(single_instance_He_avg)
        
    multi_instance_He_max = list_average(multi_instance_He_max)
    multi_instance_He_avg = list_average(multi_instance_He_avg)

    create_histogram_value(parent_dir + "/histogram/4-core_max.png", [single_instance_max, single_instance_O3_max, \
                     single_instance_O2_max, single_instance_O2_O3_max, single_instance_O1_max, single_instance_O1_O3_max, \
                     single_instance_O1_O2_max, single_instance_O1_O2_O3_max], [multi_instance_max, multi_instance_O3_max, \
                     multi_instance_O2_max, multi_instance_O2_O3_max, multi_instance_O1_max, multi_instance_O1_O3_max, \
                     multi_instance_O1_O2_max, multi_instance_O1_O2_O3_max])
    
    create_histogram_value_Park_He(parent_dir + "/histogram/4-core_Park_He.png", [single_instance_max, single_instance_Park_max, single_instance_O1_max], \
                     [multi_instance_O1_max, multi_instance_He_max, multi_instance_O1_O3_max])

    # create_histogram_value(parent_dir + "/histogram/4-core_avg.png", [single_instance_avg, single_instance_O3_avg, \
    #                  single_instance_O2_avg, single_instance_O2_O3_avg, single_instance_O1_avg, single_instance_O1_O3_avg, \
    #                  single_instance_O1_O2_avg, single_instance_O1_O2_O3_avg], [multi_instance_avg, multi_instance_O3_avg, \
    #                  multi_instance_O2_avg, multi_instance_O2_O3_avg, multi_instance_O1_avg, multi_instance_O1_O3_avg, \
    #                  multi_instance_O1_O2_avg, multi_instance_O1_O2_O3_avg])
    
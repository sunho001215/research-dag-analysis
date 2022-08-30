#include "ros/ros.h"
#include "std_msgs/String.h"
#include "ros/this_node.h"
#include <ros/package.h>
#include <pthread.h>
#include <unistd.h>

#include <sstream>
#include <vector>
#include <string>
#include <time.h>

#define MAGIC_NUMBER 497000

static int child_num_, parent_num_;
static int msg_count_, iter_ = 0, pid_;
static float callback_waste_time_ = 1000.0;
static float default_waste_time_ = 1000.0;
static float period_ = 100.0;

std::vector<ros::Publisher> publisher_list_;
std::vector<ros::Subscriber> subscriber_list_;
std::vector<int> parent_idx_, child_idx_;
std::vector<bool> sub_flag_;

std::string node_name_, file_name_;

int activation_ = 0;

void parameter_init(ros::NodeHandle nh)
{
    node_name_ = ros::this_node::getName().c_str();
    
    std::string pack_path = ros::package::getPath("research-dag-analysis");
    file_name_ = pack_path + "/profiling/" + node_name_ + ".csv";
    
    std::string child_idx_param_name = node_name_ + "/child_idx";
    std::string parent_idx_param_name = node_name_ + "/parent_idx";
    std::string callback_waste_time_param_name = node_name_ + "/callback_waste_time";
    std::string default_waste_time_param_name = node_name_ + "/default_waste_time";
    std::string period_param_name = node_name_ + "/period";

    nh.getParam(child_idx_param_name, child_idx_);
    nh.getParam(parent_idx_param_name, parent_idx_);
    nh.getParam(callback_waste_time_param_name, callback_waste_time_);
    nh.getParam(default_waste_time_param_name, default_waste_time_);
    nh.getParam(period_param_name, period_);

    parent_num_ = parent_idx_.size();
    child_num_ = child_idx_.size();

    for (int i = 0; i < parent_num_; i++)
    {
        sub_flag_.push_back(false);
    }
}

void publisher_init(ros::NodeHandle nh)
{
    for (int i = 0; i < child_num_; i++)
    {
        std::string topic_name = "topic_" + node_name_.substr(1) + "_node" + std::to_string(child_idx_.at(i)+1);
        ros::Publisher pub = nh.advertise<std_msgs::String>(topic_name, 10);
        publisher_list_.push_back(pub);
    }
}

void publish_message()
{
    std_msgs::String msg;
    std::stringstream ss;
    ss << msg_count_;
    msg.data = ss.str();

    for (int i = 0; i < child_num_; i++)
    {
        publisher_list_[i].publish(msg);
    }
}

void default_waste_time()
{
    float tmp = 3.323;
    for (long long int i = 0; i < MAGIC_NUMBER * default_waste_time_; i++)
    {
        tmp = 1 - tmp;
    }

    if (parent_num_ == 0){
        publish_message();
        msg_count_++;
        activation_ = 1;
    }

    iter_++;
}

void callback_waste_time()
{
    float tmp = 3.323;
    for (long long int i = 0; i < MAGIC_NUMBER * callback_waste_time_; i++)
    {
        tmp = 1 - tmp;
    }

    publish_message();

    activation_ = 1;
}

void topic_callback(const std_msgs::String::ConstPtr &msg, int topic_idx)
{
    sub_flag_.at(topic_idx) = true;

    if (find(sub_flag_.begin(), sub_flag_.end(), false) == sub_flag_.end())
    {
        for (int i = 0; i < parent_num_; i++)
        {
            sub_flag_.at(i) = false;
        }

        msg_count_ = std::stoi(msg->data.c_str());
        callback_waste_time();
    }
}

void subscriber_init(ros::NodeHandle nh)
{
    for (int i = 0; i < parent_num_; i++)
    {
        std::string topic_name = "topic_node" + std::to_string(parent_idx_.at(i)+1) + "_" + node_name_.substr(1);

        ros::Subscriber sub = nh.subscribe<std_msgs::String>(topic_name, 10, boost::bind(topic_callback, _1, i));

        subscriber_list_.push_back(sub);
    }
}

void reset_file()
{
    FILE *fp = fopen(file_name_.c_str(), "w");
    fprintf(fp, "iter,PID,start,end,instance,activation\n");
    fclose(fp);
}

int main(int argc, char **argv)
{
    char process_name[20];
    int ret;

    ret = pthread_getname_np(pthread_self(), process_name, 20);
    if (ret != 0){
        perror("pthread_getname_np");
    }

    ros::init(argc, argv, process_name);

    ros::NodeHandle nh;

    parameter_init(nh);
    publisher_init(nh);
    subscriber_init(nh);

    ros::Rate loop_rate(1000 / period_);

    reset_file();

    iter_ = 0;
    pid_ = getpid();
    
    struct timespec start_time, end_time;
    while (ros::ok())
    {
        clock_gettime(CLOCK_MONOTONIC, &start_time);

        activation_ = 0;

        ros::spinOnce();
        default_waste_time();

        clock_gettime(CLOCK_MONOTONIC, &end_time);

        FILE *fp = fopen(file_name_.c_str(), "a");
        fprintf(fp, "%d,%d,%ld.%.9ld,%ld.%.9ld,%d,%d\n", iter_, pid_, start_time.tv_sec, start_time.tv_nsec, end_time.tv_sec, end_time.tv_nsec, msg_count_, activation_);
        fclose(fp);

        loop_rate.sleep();
    }

    return 0;
}
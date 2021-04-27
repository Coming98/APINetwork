# -*- coding:utf-8 -*-
"""
@ author：Butterflier
@ date: 2021/4/25  9:46
@ Describe：
API名称的排序要基于 PID的基础顺序 —— 并行化
PID之间又存在着大型调用关系
"""
import atexit
import os
import pickle
import re
from functools import reduce

from progress.bar import Bar
from configparser import ConfigParser
import logging
import sys
import seaborn
import matplotlib.pyplot as plt

config=ConfigParser()
config.read("./default.config")
config = dict(config['normal'])

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

winlog = logging.StreamHandler(stream=sys.stdout)
winlog.setFormatter(logging.Formatter("%(asctime)s - %(message)s\n"))

logHandler = logging.FileHandler(os.path.join(config['logdir'], "02get_apiseq.log"))
logHandler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))

logger.addHandler(logHandler)
logger.addHandler(winlog)
def get_apiseq_by_callid(filepath):
    """
    !! type(pid) = str
    # input - filepath
    # output - 按照pid分组的api序列
    # [[api1_pid1, api2_pid1, ..., apin_pid1], [api1_pid2, ..., apim_pid2], []]
    # pid_api_dict - 记录 pid 与 api序列的对应关系
    # pid_orderby_create_time - 记录 pid 的创建顺序
    # apiseq - 由 pid_orderby_create_time 提供 pid 顺序，由 pid_api_dict 提供序列，共同构建得到
    """
    pid_api_dict = {}
    pid_orderby_create_time = []
    apiseq = []

    with open(filepath, 'r') as f:
        content = f.read()

    regex_api_pid = 'api_name="(.*?)".*?call_pid="(.*?)"'
    api_pid = re.findall(regex_api_pid, content)

    for apiname, pid in api_pid:
        if pid not in pid_orderby_create_time:
            pid_orderby_create_time.append(pid)
        if pid not in pid_api_dict.keys():
            pid_api_dict[pid] = []
        pid_api_dict[pid].append(apiname)

    apiseq = [pid_api_dict[pid] for pid in pid_orderby_create_time
              if len(pid_api_dict[pid]) >= int(config['min_apiseq_length'])]

    return apiseq

def get_apiseq_by_callid_dedup(filepath):
    """
    !! type(pid) = str
    # input - filepath
    # output - 按照pid分组的api序列
    # [[api1_pid1, api2_pid1, ..., apin_pid1], [api1_pid2, ..., apim_pid2], []]
    # pid_api_dict - 记录 pid 与 api序列的对应关系
    # pid_orderby_create_time - 记录 pid 的创建顺序
    # apiseq - 由 pid_orderby_create_time 提供 pid 顺序，由 pid_api_dict 提供序列，共同构建得到
    """
    pid_api_dict = {}
    pid_orderby_create_time = []
    apiseq = []

    with open(filepath, 'r') as f:
        content = f.read()

    regex_api_pid = 'api_name="(.*?)".*?call_pid="(.*?)"'
    api_pid = re.findall(regex_api_pid, content)

    for apiname, pid in api_pid:
        if pid not in pid_orderby_create_time:
            pid_orderby_create_time.append(pid)
        if pid not in pid_api_dict.keys():
            pid_api_dict[pid] = [apiname]
        else:
            if apiname != pid_api_dict[pid][-1]:
                pid_api_dict[pid].append(apiname)

    apiseq = [pid_api_dict[pid] for pid in pid_orderby_create_time
              if len(pid_api_dict[pid]) >= int(config['min_apiseq_length'])]

    return apiseq

def info_show(train_apiseq, test_apiseq):

    def info_show_one(**kwargs):
        print("=="*10)
        for key, value, in kwargs.items():
            print(key)
            print("length: ", len(value))
            print("demo show of index 0: ")
            print("apiseq[0]'s length (the count of pid): ", len(value[0]))
            print("apiseq[0][0]'s length (the count of apiseq based on pid_0): ", len(value[0][0]))
            print("apiseq[0][0]'s demo - limits 5: ", len(value[0][0][:5]))
            print("**"*10)
            print("pid length show: ")
            seaborn.stripplot([len(apiseq_pid) for xml in value for apiseq_pid in xml])
            plt.show()
            print("total length show: ")
            seaborn.stripplot([ len(reduce(lambda apiseq_a, apiseq_b: apiseq_a + apiseq_b, xml)) for xml in value if len(xml) > 1])
            plt.show()


    info_show_one(train_apiseq=train_apiseq, test_apiseq=test_apiseq)

def finish(bar):
    try:
        bar.finish()
    except:
        print("end")

def main():

    save_name = "apiseq_callid_dedup.pkl"
    if os.path.exists(os.path.join(config['outputdir'], save_name)):
        logger.debug("loading {}".format(save_name))
        with open(os.path.join(config['outputdir'], save_name), 'rb') as f:
            train_apiseq, test_apiseq = pickle.load(f)
    else:
        train_apiseq, test_apiseq = [], []

        with open("./dumps/train_test_filenames.pkl", 'rb') as f:
            train_filenames, test_filenames = pickle.load(f)
        bar = Bar('Processing', max=len(train_filenames+test_filenames), fill='@', suffix='%(percent)d%%')
        atexit.register(finish, bar)
        for rootpath, dirnames, filenames in os.walk(config['datadir']):
            for filename in filenames:
                filepath = os.path.join(rootpath, filename)
                if "dedup" in save_name:
                    demoseq = get_apiseq_by_callid_dedup(filepath)
                else:
                    demoseq = get_apiseq_by_callid(filepath)

                if(filename in train_filenames):
                    train_apiseq.append(demoseq)
                elif(filename in test_filenames):
                    test_apiseq.append(demoseq)
                else:
                    print("WRONG!", filename)
                bar.next()
        bar.finish()
        with open(os.path.join(config["outputdir"], save_name), 'wb') as f:
            pickle.dump((train_apiseq, test_apiseq), f)

    info_show(train_apiseq, test_apiseq)



if __name__ == '__main__':
    main()

# -*- coding:utf-8 -*-
"""
@ author：Butterflier
@ date: 2021/4/26  10:59
@ Describe：实现 white 数据集的切分
"""
import os
import numpy as np
import pickle
from configparser import ConfigParser

config = ConfigParser()
config.read("./default.config")
config = config['normal']

if not os.path.exists(config['outputdir']):
    os.makedirs(config['outputdir'])

def info_show(train_filenames, test_filenames, white_filenames, black_filenames, extra_filenames):

    def info_show_one(**kwargs):
        for key, value in kwargs.items():
            print("===" * 15)
            print("{}:".format(key))
            print("length: ", len(value))
            print("set length: ", len(set(value)))
            print("demo: ", " # ".join(value[:2]))
            print("length of the intersection with white_filenames: ", len(set(value) & set(white_filenames)))
            print("length of the intersection with black_filenames: ", len(set(value) & set(black_filenames)))
            print("length of the intersection with extra_filenames: ", len(set(value) & set(extra_filenames)))

    info_show_one(train_filenames=train_filenames, test_filenames=test_filenames)

    print("===" * 15)
    print("all:")
    print("intersection between train set and test set: ", set(train_filenames) & set(test_filenames))


def main():

    train_filenames = []
    test_filenames = []
    white_filenames = []
    black_filenames = []
    extra_filenames = []

    for rootpath, dirnames, filenames in os.walk(config['datadir']):

        if "white" in rootpath:
            split_length = int(len(filenames) * 0.5)
            np.random.seed(int(config['randomseed']))
            shuffle_filenames = np.random.permutation(filenames)
            train_filenames.extend(shuffle_filenames[:split_length])
            test_filenames.extend(shuffle_filenames[split_length:])

            white_filenames=list(filenames)
        elif "black" in rootpath:
            train_filenames.extend(filenames)
            black_filenames = list(filenames)
        elif "test" in rootpath:
            test_filenames.extend(filenames)

            extra_filenames=list(filenames)

    info_show(train_filenames, test_filenames, white_filenames, black_filenames, extra_filenames)

    save_name = "train_test_filenames.pkl"
    with open(os.path.join(config['outputdir'], save_name), 'wb') as f:
        pickle.dump((train_filenames, test_filenames), f)

if __name__ == '__main__':
    main()

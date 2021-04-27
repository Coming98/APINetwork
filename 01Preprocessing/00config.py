# -*- coding:utf-8 -*-
"""
@ author：Butterflier
@ date: 2021/4/26  11:05
@ Describe：
"""
import os
from configparser import ConfigParser

default_dict = {
    "datadir":"../ApiData",
    "outputdir":"./dumps",
    "logdir":"./logs",
    "analysisdir":"./analysis",
    "randomseed":"666",
    "min_apiseq_length":"5",
}

config = ConfigParser(default_dict)
config.add_section("normal")

with open("./default.config", 'w') as f:
    config.write(f)

for dirpath in (config['normal']['outputdir'], config['normal']['logdir'], config['normal']['analysisdir']):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
#!/usr/bin/env python
#coding=utf-8

import sys
import pandas as pd
import numpy as np
import pickle

def json2csv():
    df = pd.read_json("./new_data_4800.json")
    df.to_csv("./new_data_4800.csv")

if __name__ == '__main__':
    # inpath = sys.argv[0]
    # outpath = sys.argv[1] # outpath = "./new_data_4800.csv"
    json2csv()


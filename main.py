
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from ggplot import *
from datetime import datetime
import pandas as pd
from helper_functions import *
import itertools


## Set base filepath & import the voter files as pandas dataframes
base_file_path = "/Users/myusername/.virtualenvs/myfolder/"

vf_path = base_file_path + "My_District-VF.csv"
vh_path = base_file_path + "My_District-VH.csv"

voter_file, voter_history = make_dataframes(vf_path, vh_path)
voter_file, voter_history = clean_dataframes(voter_file, voter_history)

## Preview new dataframes
voter_file.dtypes
voter_history.dtypes
voter_file.head(10)
voter_history.head(10)


def main():
    data_quality_check(voter_file, voter_history)
    age_distribution(voter_file)
    elections = get_elections(voter_history)
    age_distribution_by_election(voter_file, voter_history, elections)
    segments_table(voter_file, voter_history, base_file_path)


if __name__ == '__main__':
	main()


























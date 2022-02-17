import json
import numpy as np

base = "exp1-ground_truth"
file_name = ["30","50","70","90","110"]
file_name = ["bare_bare_" + s for s in file_name]
json_file_names = np.arange(8)

path_to_json = 'exp1-ground_truth/bare_bare_30'

with open("exp1-ground_truth/bare_bare_30/bare_bare_30_iter1.json", "r") as json_file:
    bb30 = json.load(json_file)

"""
The json file consists of a dict object with two keys:
1. 'experiment_parameters' : dictionary
2. 'data' : list where each element is a dictionary

==================================
'experiment_parameters'
experiment_title : str
iteration : int
date : str
experiment_start_time : str
rail_material : str
phantom_material : str
compared_curvature : int
first_grating_idx : int
last_grating_idx : int
wav0 : list, float
local_time : str
==================================
'data': list, each element is a dict, keys are listed as follows:
elapsed_time : float
line_number : int
wav_data : list, float
curvatures : list, float
positions_2d : nested list, float
positions_3d : nested list, float
"""
exp_params = bb30["experiment_parameters"]

data = bb30["data"]


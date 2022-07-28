import json
import math

import numpy as np

file = 'data/max_pulling.json'
CENTRAL_CORE = 1
NB_CORES = 4
NB_GRATINGS_PER_CORE = 25
CORE_TO_CENTER_DIST_UM = 37  # (37μm) # Check and update with the correct one
GRATING_SPACING_M = 10 * 10 ** -3  # (mm)
ANGLE_TO_NX = np.radians([0, 120, 240])

# To modify to be able to see another line of data
data_idx = 15


def load_experiment(json_file):
    try:
        # Opening JSON file
        with open(json_file) as json_file:
            experiment_json = json.load(json_file)
            wav0 = np.split(np.array(experiment_json['experiment_parameters']['wav0']), NB_CORES)
            wav_data = np.split(np.array(experiment_json['data'][data_idx]['wav_data']), NB_CORES)


    except json.JSONDecodeError:
        print('JSON is not rightly formatted')

    return np.array(wav0), np.array(wav_data)


def get_wav_difference(wav0, wav_data):
    return wav_data - wav0


def compensate_temperature(wav_diff):
    """ Subscribe to the topic once, and then update the reference wavelength array [wav0 attribute],
    update every optical channel wav0 attribute and calculate the Δλi"""
    # Get the central core wavelength difference
    wav_diff_central_core = wav_diff[CENTRAL_CORE]

    return wav_diff - wav_diff_central_core


def calculate_strain_outer_cores(wav_diff_temp_comp):
    ki_vector = np.zeros((NB_CORES, NB_GRATINGS_PER_CORE)) + 0.045  # nm/m-1
    strain_matrix = wav_diff_temp_comp * CORE_TO_CENTER_DIST_UM / ki_vector
    strain_matrix = np.delete(strain_matrix, 1, 0)
    return strain_matrix


def calculate_curvature_vector(strain_matrix):
    """Return current curvature vector in 1/m"""
    # Create the vectors required to calculate the curvature vector
    shape = np.shape(strain_matrix)
    ones = np.transpose(np.ones(shape))
    cos_mat = np.cos(np.transpose(ANGLE_TO_NX * ones))
    sin_mat = np.sin(np.transpose(ANGLE_TO_NX * ones))

    # Calculate the curvature vector
    curvature_vector_nx = -2 / ((NB_CORES - 1) * CORE_TO_CENTER_DIST_UM) * sum(strain_matrix * cos_mat)
    curvature_vector_ny = -2 / ((NB_CORES - 1) * CORE_TO_CENTER_DIST_UM) * sum(strain_matrix * sin_mat)

    return np.transpose(np.array([curvature_vector_nx, curvature_vector_ny]))  # m-1


def modulus(vector):
    dist = np.sqrt(np.einsum('...i,...i', vector, vector))
    return dist


def calculate_radii_of_curvature(curvature_vector):
    curvature_vector = modulus(curvature_vector)
    mask = curvature_vector < 10 ** -5
    # Replace 0 with nan
    curvature_vector[mask] = np.nan
    # Divide the vector
    radii = 1 / curvature_vector
    # Convert nan back to inf
    radii[mask] = np.inf
    return radii


def calculate_phis(radii_of_curvature):
    phi_vect = GRATING_SPACING_M / radii_of_curvature
    return phi_vect


def calculate_thetas(curvature_vector):
    thetas_array = np.zeros(len(curvature_vector))
    for i in range(len(curvature_vector)):
        thetas_array[i] = math.atan2(curvature_vector[i, 0], curvature_vector[i, 1])

    return thetas_array


if __name__ == '__main__':
    ref, wav_data = load_experiment(file)
    wav_diff = get_wav_difference(ref, wav_data)
    wav_diff_temp_comp = compensate_temperature(wav_diff)
    strains_mat = calculate_strain_outer_cores(wav_diff_temp_comp)
    curvature_vector = calculate_curvature_vector(strains_mat)
    thetas = calculate_thetas(curvature_vector)

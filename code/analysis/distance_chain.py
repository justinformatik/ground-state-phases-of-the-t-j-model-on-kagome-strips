# SPECIFY PATHS!
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from scipy.optimize import curve_fit
import numpy as np
import seaborn as sns
colors = sns.color_palette('colorblind', 3)

#bonds, vertices need to be specified depending on the number of sites
##########################################################################################

#bonds = [20-1, 31-1, 32-1, 1-1, 2-1, 24-1, 15-1, 16-1, 28-1, 27-1, 9-1, 10-1, 29-1, 30-1, 3-1, 4-1, 17-1, 21-1, 5-1, 6-1, 22-1, 23-1, 11-1, 12-1, 33-1, 35-1, 13-1, 14-1, 18-1, 19-1, 25-1, 26-1, 34-1, 7-1, 8-1]
#vertices = list(range(1, 37))

bonds = [60, 61, 22, 0, 1, 13, 51, 71, 62, 43, 32, 23, 24, 76, 66, 67, 63, 64, 68, 69, 73, 37, 38, 52, 53, 65, 33, 34, 9, 10, 11, 12, 57, 4, 5, 44, 74, 47, 48, 39, 40, 41, 42, 16, 17, 72, 75, 70, 58, 59, 30, 31, 25, 6, 2, 3, 28, 29, 7, 8, 27, 26, 20, 21, 56, 14, 15, 45, 46, 54, 55, 18, 19, 35, 36, 49, 50]
vertices = list(range(1, 79))

#bonds = [46, 47, 17, 0, 1, 13, 40, 57, 48, 36, 27, 18, 19, 62, 52, 53, 49, 50, 54, 55, 59, 30, 31, 41, 42, 51, 28, 29, 9, 10, 11, 12, 43, 4, 5, 37, 60, 38, 39, 32, 33, 34, 35, 14, 15, 58, 56, 61, 44, 45, 25, 26, 20, 6, 2, 3, 23, 24, 7, 8, 22, 21, 16]
#vertices = list(range(1, 65))

#######################################################################################

def calculate_averaged_values_middle(matrix, indices, margin=2): #can play around with the margin. 2 might be enough
    distance_values = {}
    n = len(indices)
    middle_section = indices[margin:n-margin]
    
    for dist in range(1, len(middle_section)):
        pairs = list(itertools.combinations(middle_section, 2))
        values = [matrix.iloc[pair[0], pair[1]] for pair in pairs if abs(indices.index(pair[0]) - indices.index(pair[1])) == dist]
        
        if values:
            avg_value = sum(values) / len(values)
            distance_values[dist] = avg_value
    return distance_values

for J in np.arange(0.0, 3.5, 0.5):

    # load any corr functions
    matrix1 = pd.read_csv(f'.csv')
    matrix2 = pd.read_csv(f'.csv')
    matrix3 = pd.read_csv(f'.csv')

    matrix1.columns = [f'x{i+1}' for i in range(matrix1.shape[1])]
    matrix2.columns = [f'x{i+1}' for i in range(matrix2.shape[1])]
    matrix3.columns = [f'x{i+1}' for i in range(matrix3.shape[1])]

    matrix1 = matrix1.abs()
    matrix2 = matrix2.abs()
    matrix3 = matrix3.abs()

    distance_values1 = calculate_averaged_values_middle(matrix1, bonds)
    distance_values2 = calculate_averaged_values_middle(matrix2, vertices)
    distance_values3 = calculate_averaged_values_middle(matrix3, vertices)

    distances1 = np.array(list(distance_values1.keys()))
    values1 = np.array(list(distance_values1.values()))
    distances2 = np.array(list(distance_values2.keys()))
    values2 = np.array(list(distance_values2.values()))
    distances3 = np.array(list(distance_values3.keys()))
    values3 = np.array(list(distance_values3.values()))

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.loglog(distances1, values1, marker='o', linestyle='-', label='Singlet Pairing Correlation Function', color=colors[0], markersize=5, linewidth=1)
    ax.loglog(distances2, values2, marker='^', linestyle='--', label='Spin-Spin Correlation Function', color=colors[1], markersize=5, linewidth=1)
    ax.loglog(distances3, values3, marker='s', linestyle='-.', label='Density-Density Correlation Function', color=colors[2], markersize=5, linewidth=1)

    ax.set_title(rf'Correlation value over distance $\left| i - j \right|$ for 78 sites and filling 1/3 and J = {J}', size='x-large')
    ax.set_xlabel(r'Distance $\left| i - j \right|$', size='x-large')
    ax.set_ylabel('Average Correlation Value', size='x-large')
    ax.grid(which='both', linestyle='--', linewidth=0.5)
    ax.minorticks_on()
    ax.grid(which='minor', alpha=0.5)
    ax.grid(which='major', alpha=0.75)
    ax.legend()
    #plt.savefig(f'.pgf')
    plt.show()
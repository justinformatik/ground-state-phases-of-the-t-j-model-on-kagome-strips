# SPECIFY PATHS!
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from scipy.optimize import curve_fit
import numpy as np
import seaborn as sns
colors = sns.color_palette('colorblind', 3)

#bonds, vertices need to be specified depending on the number of stars
##########################################################################################

#5 stars:
#bonds = [46, 39, 37, 57, 21, 23, 25, 26, 33]
#vertices = [3, 2, 11, 10, 18, 17, 25, 24, 32, 31]

# 9 stars:
#bonds = [76, 60, 57, 82, 83, 70, 68, 21, 65, 19, 63, 101, 26, 28, 44, 14, 11]
#vertices = [2, 3, 10, 11, 17, 18, 24, 25, 31, 32, 38, 39, 45, 46, 52, 53, 59, 60]

#11 stars:
bonds = [99, 73, 70, 105, 106, 88, 86, 21, 19, 82, 80, 125, 30, 32, 53, 14, 11, 28, 25, 91, 34]
vertices = [2, 3, 10, 11, 17, 18, 24, 25, 31, 32, 38, 39, 45, 46, 52, 53, 59, 60, 66, 67, 73, 74]

############################################################################################

def calculate_averaged_values_middle(matrix, indices, margin=1): #can play around with the margin. 2 migh be enough
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

for J in np.arange(3.0, 4.0, 0.5):

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

    ax.set_title(rf'Correlation value over distance $\left| i - j \right|$ for 11 stars and filling 1/3 and J = {J}', size='x-large')
    ax.set_xlabel(r'Distance $\left| i - j \right|$', size='x-large')
    ax.set_ylabel('Average Correlation Value', size='x-large')
    ax.grid(which='both', linestyle='--', linewidth=0.5)
    ax.minorticks_on()
    ax.grid(which='minor', alpha=0.5)
    ax.grid(which='major', alpha=0.75)
    ax.legend()
    #plt.savefig(f'.pgf')
    plt.show()
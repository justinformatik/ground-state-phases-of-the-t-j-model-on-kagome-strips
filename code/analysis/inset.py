# SPECIFY PATHS!
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

def load_and_sort_eigenvalues(file_path):
    if not os.path.exists(file_path):
        return None
    df = pd.read_csv(file_path)
    df_sorted = df.sort_values(by='Eigenvalue', ascending=False).reset_index(drop=True)
    return df_sorted

def calculate_eigenvalue_difference(df_sorted):
    if df_sorted is None or len(df_sorted) < 2:
        return None
    return df_sorted.loc[0, 'Eigenvalue'] - df_sorted.loc[1, 'Eigenvalue']

def plot_eigenvalue_differences(base_paths, J_values, labels, output_path):
    fig, ax1 = plt.subplots(figsize=(10, 8))
    #colors  = ['#2CBDFE', '#47DBCD', '#F3A0F2', '#9D2EC5', '#661D98', '#FF6F61', '#3CB371', '#6B8E23']
    colors = sns.color_palette('colorblind', 2)
    markers = ['o', '^']
    for base_path, label, color, mark in zip(base_paths, labels, colors, markers):
        differences = []
        valid_J = []
        for J in J_values:
            file_path = os.path.join(base_path, f'eigenvalues_{J}.csv')
            df_sorted = load_and_sort_eigenvalues(file_path)
            if df_sorted is not None:
                print(f'Data for {label} at J={J} found.')
            difference = calculate_eigenvalue_difference(df_sorted)
            if difference is not None:
                differences.append(difference)
                valid_J.append(J)
        
        data = {'J': valid_J, 'Difference': differences}
        df_diff = pd.DataFrame(data)
        
        if not df_diff.empty:
            ax1.plot(df_diff['J'], df_diff['Difference'], marker=mark, color=color, label=label)
        else:
            print(f'No valid data to plot for {label}.')
    
    ax1.set_title('Difference between the two largest eigenvalues', fontsize='x-large')
    ax1.set_xlabel('J', fontsize='x-large')
    ax1.set_ylabel('Difference', fontsize='x-large')
    ax1.grid(which='both', linestyle='--', linewidth=0.5)
    ax1.minorticks_on()
    ax1.grid(which='minor', alpha=0.5)
    ax1.grid(which='major', alpha=0.75)
    ax1.legend(fontsize='x-large')

    plt.tight_layout()
    plt.savefig(output_path, dpi=1000)
    plt.show()

base_path_main = '' #specify
base_path_main2 = '' #specify

J_values = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
labels_inset = ['9 star kagome strip', '64 site chain']
output_path = 'inset.pgf'

plot_eigenvalue_differences([base_path_main, base_path_main2], J_values, labels_inset, output_path)
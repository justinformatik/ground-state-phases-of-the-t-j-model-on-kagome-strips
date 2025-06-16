# SPECIFY PATHS!
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

def load_and_sort_eigenvalues(file_path):
    df = pd.read_csv(file_path)
    df_sorted = df.sort_values(by='Eigenvalue', ascending=False).reset_index(drop=True)
    return df_sorted

def plot_eigenvalues(base_path, J_values, output_path):
    fig, ax1 = plt.subplots(figsize=(10, 8))
    #colors = ['#FF4C4C', '#FFA500', '#FFFF00', '#ADFF2F', '#40E0D0', '#1E90FF', '#4B0082', '#8A2BE2', '#FF00FF']
    colors  =['#2CBDFE', '#47DBCD', '#F3A0F2', '#9D2EC5', '#661D98', '#FF6F61', '#FFD700', '#6B8E23']
    colors = sns.color_palette('colorblind', 8)
    for J, color in zip(J_values, colors):
        file_path = os.path.join(base_path, f'eigenvalues_{J}.csv')
        df_sorted = load_and_sort_eigenvalues(file_path)
        ax1.plot(df_sorted.index, df_sorted['Eigenvalue'], label=f'J={J}', marker='.', color=color)
    
    ax1.set_xlabel(r'$i$', fontsize='x-large')
    ax1.set_ylabel(r'$\lambda_i$', fontsize='x-large')
    ax1.set_title('Eigenvalues of pairing correlation matrix for different J for a 64 site chain and filling 1/8', size='x-large')
    ax1.grid(which='both', linestyle='--', linewidth=0.5)
    ax1.minorticks_on()
    ax1.grid(which='minor', alpha=0.5)
    ax1.grid(which='major', alpha=0.75)
    
    ax1.legend(fontsize='x-large')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=1000)
    plt.show()

def calculate_eigenvalue_difference(df_sorted):
    return df_sorted.loc[0, 'Eigenvalue'] - df_sorted.loc[1, 'Eigenvalue']

def plot_eigenvalue_differences(base_paths, J_values, labels, output_path):
    fig, ax1 = plt.subplots(figsize=(10, 8))
    #colors = ['blue', 'red', 'orange', 'green', 'purple', 'brown', 'magenta', 'black', 'goldenrod']
    #colors  =['#2CBDFE', '#47DBCD', '#F3A0F2', '#9D2EC5', '#661D98', '#FF6F61', '#FFD700', '#6B8E23']
    colors = sns.color_palette('colorblind', 8)

    for base_path, label, color in zip(base_paths, labels, colors):
        differences = []
        for J in J_values:
            file_path = os.path.join(base_path, f'eigenvalues_{J}.csv')
            df_sorted = load_and_sort_eigenvalues(file_path)
            difference = calculate_eigenvalue_difference(df_sorted)
            differences.append(difference)
        
        data = {'J': J_values, 'Difference': differences}
        df_diff = pd.DataFrame(data)
        
        ax1.plot(df_diff['J'], df_diff['Difference'], marker='o', color=color, label=label)
    
    ax1.set_xlabel('J', fontsize='x-large')
    ax1.set_ylabel('Difference of first two Eigenvalues', fontsize='x-large')
    ax1.set_title('Difference of first two Eigenvalues over J', size='x-large')
    ax1.grid(which='both', linestyle='--', linewidth=0.5)
    ax1.minorticks_on()
    ax1.grid(which='minor', alpha=0.5)
    ax1.grid(which='major', alpha=0.75)
    ax1.legend(fontsize='x-large')

    plt.tight_layout()
    plt.savefig(output_path, dpi=1000)
    plt.show()

def plot_main_with_inset(base_path, J_values, base_paths_inset, labels_inset, output_path):
    fig, ax1 = plt.subplots(figsize=(10, 8))
    colors_main = ['#FF4C4C', '#FFA500', '#FFFF00', '#ADFF2F', '#40E0D0', '#1E90FF', '#4B0082', '#8A2BE2', '#FF00FF']
    colors_main = ['#2CBDFE', '#47DBCD', '#F3A0F2', '#9D2EC5', '#661D98', '#FF6F61', '#3CB371', '#6B8E23']
    #colors_main = sns.color_palette('colorblind', 8)

    for J, color in zip(J_values, colors_main):
        file_path = os.path.join(base_path, f'eigenvalues_{J}.csv')
        df_sorted = load_and_sort_eigenvalues(file_path)
        ax1.plot(df_sorted.index, df_sorted['Eigenvalue'], label=f'J={J}', marker='.', color=color)
    
    ax1.set_xlabel(r'Index i', fontsize='x-large')
    ax1.set_ylabel(r'Eigenvalue $\lambda_{\mathrm{i}}$', fontsize='x-large')
    ax1.set_title(r'Eigenvalues $\lambda_{\mathrm{i}}$ of $P$ for different $J$ for a 78 site chain and filling 1/3', size='x-large')
    ax1.grid(which='both', linestyle='--', linewidth=0.5)
    ax1.minorticks_on()
    ax1.grid(which='minor', alpha=0.5)
    ax1.grid(which='major', alpha=0.75)
    ax1.legend(fontsize='x-large')

    # inset
    ax_inset = fig.add_axes([0.335, 0.375, 0.5, 0.45])  
    colors_inset = ['black', 'red', 'orange', 'green', 'purple', 'brown', 'magenta', 'black', 'goldenrod']

    for base_path, label, color in zip(base_paths_inset, labels_inset, colors_inset):
        differences = []
        for J in J_values:
            file_path = os.path.join(base_path, f'eigenvalues_{J}.csv')
            df_sorted = load_and_sort_eigenvalues(file_path)
            difference = calculate_eigenvalue_difference(df_sorted)
            differences.append(difference)
        
        data = {'J': J_values, 'Difference': differences}
        df_diff = pd.DataFrame(data)
        #ax_inset.set_ylim([0, 1.0])
        ax_inset.plot(df_diff['J'], df_diff['Difference'], marker='.', color=color, label=label)
    
    ax_inset.set_title('Difference between the two largest eigenvalues', fontsize = 'large')
    ax_inset.set_xlabel(r'$J$', fontsize='large')
    ax_inset.set_ylabel('Difference', fontsize='large')
    ax_inset.grid(which='both', linestyle='--', linewidth=0.5)
    ax_inset.minorticks_on()
    ax_inset.grid(which='minor', alpha=0.5)
    ax_inset.grid(which='major', alpha=0.75)
    plt.tight_layout()
    plt.savefig(output_path, dpi=1000)
    plt.show()

base_path_main = '' #specify ###############
J_values = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

base_paths_inset = [
    base_path_main,
]
labels_inset = ['chain']
output_path = 'chain78_1_over_3.pgf'
plot_main_with_inset(base_path_main, J_values, base_paths_inset, labels_inset, output_path)
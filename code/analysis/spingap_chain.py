# SPECIFY PATHS!
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import seaborn as sns

def plot_with_regression(ax, df, label, color, mark, skip_points=0):
    X = df['J'].values.reshape(-1, 1)[skip_points:]
    y = df['spin_gap_norm'].values[skip_points:]
    model = LinearRegression().fit(X, y)
    slope = model.coef_[0]
    intercept = model.intercept_
        ax.plot(df['J'], df['spin_gap_norm'], marker=mark, color=color, label=label)
    
    x_range = np.linspace(1.5, 3.5, 100)
    y_range = model.predict(x_range.reshape(-1, 1))
    ax.plot(x_range, y_range, linestyle='--', color=color)
    
    return slope, intercept

dataframes_paths = [
    'chain18_1_over_3/spin_gap_and_energy.csv', #specify
    'chain36_1_over_3/spin_gap_and_energy.csv', #specify
    'chain54_1_over_3/spin_gap_and_energy.csv', #specify
    'chain66_1_over_3/spin_gap_and_energy.csv', #specify   
    'chain78_1_over_3/spin_gap_and_energy.csv'  #specify
]

labels = ['18 sites','36 sites', '54 sites', '66 sites', '78 sites']

colors = plt.cm.tab10.colors
colors = sns.color_palette('colorblind', 5)
slopes = []
intercepts = []
x_intercepts = []

fig, ax1 = plt.subplots(figsize=(10, 8))
markers = ['o', 's', 'D', '^', 'v']

for i, path in enumerate(dataframes_paths):
    df = pd.read_csv(path)
    
    df['spin_gap_norm'] = df['spin_gap']
    
    df = df.replace([np.inf, -np.inf], np.nan).dropna()

    slope, intercept = plot_with_regression(ax1, df, labels[i], colors[i], markers[i], skip_points=5)
    slopes.append(slope)
    intercepts.append(intercept)
    x_intercepts.append(-intercept / slope)

ax1.set_xlabel('J', fontsize='x-large')
ax1.set_ylabel('Spin gap value', fontsize='x-large')
ax1.set_title('Spin gap for different J for five chains of different sizes', size='x-large')
ax1.grid(which='both', linestyle='--', linewidth=0.5)
ax1.minorticks_on()
ax1.grid(which='minor', alpha=0.5)
ax1.grid(which='major', alpha=0.75)

ax1.legend(fontsize='x-large', loc = 4)

ax1.scatter(x_intercepts, [0] * len(x_intercepts), color='red', zorder=5)

for i, (slope, intercept, x_intercept) in enumerate(zip(slopes, intercepts, x_intercepts)):
    print(f'{labels[i]}: slope={slope}, intercept={intercept}, x-intercept={x_intercept}')


data = {
    'x_intercept': x_intercepts,
    '1/L': [1/L for L in [18, 36, 54, 66, 78]]
}

df_intercepts = pd.DataFrame(data)

df_intercepts_largest_L = df_intercepts.sort_values('1/L').head(3) # only 3 largest system sizes for inset plot

X_intercept_largest = df_intercepts_largest_L['1/L'].values.reshape(-1, 1)
y_intercept_largest = df_intercepts_largest_L['x_intercept'].values
model_intercept_largest = LinearRegression().fit(X_intercept_largest, y_intercept_largest)
slope_intercept_largest = model_intercept_largest.coef_[0]
intercept_intercept_largest = model_intercept_largest.intercept_

ax_inset = fig.add_axes([0.15, 0.55, 0.45, 0.35])  

ax_inset.plot(df_intercepts_largest_L['1/L'], df_intercepts_largest_L['x_intercept'], 'o', color='red', zorder=5)

x_range_intercept_largest = np.linspace(0, max(df_intercepts_largest_L['1/L']), 100)
y_range_intercept_largest = model_intercept_largest.predict(x_range_intercept_largest.reshape(-1, 1))
ax_inset.plot(x_range_intercept_largest, y_range_intercept_largest, '--', label='Linear regression', color='black')

ax_inset.set_xlabel('1/L', fontsize='large')
ax_inset.set_ylabel('J', fontsize='large')
ax_inset.set_title('Critical J value', size='large')
ax_inset.grid(which='both', linestyle='--', linewidth=0.5)
ax_inset.minorticks_on()
ax_inset.grid(which='minor', alpha=0.5)
ax_inset.grid(which='major', alpha=0.75)

ax_inset.legend(fontsize='medium')
plt.tight_layout()

y_axis_intercept_largest = -intercept_intercept_largest / slope_intercept_largest
print(f'Linear fit (largest L): slope={slope_intercept_largest}, intercept={intercept_intercept_largest}, y-axis intersection={y_axis_intercept_largest}')
plt.savefig('spingap_chain.png')
plt.show()
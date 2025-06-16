# SPECIFY PATHS!
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import seaborn as sns

df2 = pd.read_csv('5stars/filling_1_over_3/spin_gap_and_energy.csv') #speficy
df3 = pd.read_csv('11stars/filling_1_over_3/spin_gap_and_energy.csv')#specify

df2['spin_gap_norm'] = df2['spin_gap']
df3['spin_gap_norm'] = df3['spin_gap']

colors = plt.cm.tab10.colors
colors = sns.color_palette('colorblind', 2)

def plot_with_regression(ax, df, label, color, mark, skip_points=0):
    X = df['J'].values.reshape(-1, 1)[skip_points:]
    y = df['spin_gap_norm'].values[skip_points:]
    model = LinearRegression().fit(X, y)
    slope = model.coef_[0]
    intercept = model.intercept_
    
    ax.plot(df['J'], df['spin_gap_norm'], marker=mark, color=color, label=label)
    
    x_range = np.linspace(1.1, 3.5, 100)
    y_range = model.predict(x_range.reshape(-1, 1))
    ax.plot(x_range, y_range, linestyle='--', color=color)
    
    return slope, intercept

fig, ax1 = plt.subplots(figsize=(10, 8))

markers = ['o', 's']

slope2, intercept2 = plot_with_regression(ax1, df2, '5 stars kagome strip', colors[0], markers[0], skip_points=15) #skip 14 for 5star -> play around
slope3, intercept3 = plot_with_regression(ax1, df3, '11 stars kagome strip', colors[1], markers[1], skip_points=4) #skip 4 for 11star -> play around

ax1.set_xlabel('J', fontsize='x-large')
ax1.set_ylabel('Spin gap value', fontsize='x-large')
ax1.set_title('Spin gap for different J for 5 and 11 star kagome strips', size='x-large')
ax1.grid(which='both', linestyle='--', linewidth=0.5)
ax1.minorticks_on()
ax1.grid(which='minor', alpha=0.5)
ax1.grid(which='major', alpha=0.75)

ax1.legend(fontsize='x-large', loc=4)

x_intercept2 = -intercept2 / slope2
x_intercept3 = -intercept3 / slope3

ax1.scatter([x_intercept2, x_intercept3], [0, 0], color='red', zorder=5)

print(f'kagome5: slope={slope2}, intercept={intercept2}, x-intercept={x_intercept2}')
print(f'kagome11: slope={slope3}, intercept={intercept3}, x-intercept={x_intercept3}')

data = {
    'x_intercept': [x_intercept2, x_intercept3],
    '1/L': [1/5, 1/11]
}

df_intercepts = pd.DataFrame(data)

X_intercept = df_intercepts['1/L'].values.reshape(-1, 1)
y_intercept = df_intercepts['x_intercept'].values
model_intercept = LinearRegression().fit(X_intercept, y_intercept)
slope_intercept = model_intercept.coef_[0]
intercept_intercept = model_intercept.intercept_

ax_inset = fig.add_axes([0.15, 0.55, 0.45, 0.35]) 

ax_inset.plot(df_intercepts['1/L'], df_intercepts['x_intercept'], 'o', color='red', zorder=5)

x_range_intercept = np.linspace(0, max(df_intercepts['1/L']), 100)
y_range_intercept = model_intercept.predict(x_range_intercept.reshape(-1, 1))
ax_inset.plot(x_range_intercept, y_range_intercept, '--', label='Linear regression', color='black')

ax_inset.set_xlabel('1/L', fontsize='large')
ax_inset.set_ylabel('J', fontsize='large')
ax_inset.set_title('Critical J value', size='large')
ax_inset.grid(which='both', linestyle='--', linewidth=0.5)
ax_inset.minorticks_on()
ax_inset.grid(which='minor', alpha=0.5)
ax_inset.grid(which='major', alpha=0.75)

ax_inset.legend(fontsize='medium')

plt.tight_layout()

y_axis_intercept = -intercept_intercept / slope_intercept
print(f'Linear fit: slope={slope_intercept}, intercept={intercept_intercept}, y-axis intersection={y_axis_intercept}')
ax1.scatter([x_intercept2, x_intercept3], [0, 0], color='red', zorder=5)
#plt.savefig('spingap_kagome.pgf')
plt.show()
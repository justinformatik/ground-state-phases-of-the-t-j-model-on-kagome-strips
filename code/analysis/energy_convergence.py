# SPECIFY PATHS!
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

sweep_indices = list(range(1, 31))
import re

# filling 1/6
text2 = '''
After sweep 1 energy=-15.988183443910373  maxlinkdim=10 maxerr=3.49E-04 time=35.999
After sweep 2 energy=-17.014986976325872  maxlinkdim=20 maxerr=7.33E-04 time=4.763
After sweep 3 energy=-17.674684813669224  maxlinkdim=40 maxerr=2.40E-04 time=0.523
After sweep 4 energy=-18.043491676744363  maxlinkdim=75 maxerr=5.06E-05 time=0.822
After sweep 5 energy=-18.093757756598222  maxlinkdim=100 maxerr=4.51E-05 time=1.131
After sweep 6 energy=-18.09885146535492  maxlinkdim=150 maxerr=1.46E-05 time=2.183
After sweep 7 energy=-18.099649089681247  maxlinkdim=200 maxerr=2.83E-06 time=2.444
After sweep 8 energy=-18.099773641614227  maxlinkdim=250 maxerr=8.69E-07 time=3.174
After sweep 9 energy=-18.09979738929833  maxlinkdim=300 maxerr=3.76E-07 time=4.533
After sweep 10 energy=-18.099804463039913  maxlinkdim=350 maxerr=1.41E-07 time=4.644
After sweep 11 energy=-18.09980671591169  maxlinkdim=400 maxerr=5.11E-08 time=6.421
After sweep 12 energy=-18.09980775100585  maxlinkdim=500 maxerr=8.21E-09 time=8.828
After sweep 13 energy=-18.09980791212204  maxlinkdim=600 maxerr=1.93E-09 time=12.362
After sweep 14 energy=-18.099807946581716  maxlinkdim=700 maxerr=4.56E-10 time=15.478
After sweep 15 energy=-18.09980795406355  maxlinkdim=800 maxerr=1.33E-10 time=16.171
After sweep 16 energy=-18.0998079560933  maxlinkdim=900 maxerr=3.31E-11 time=17.659
After sweep 17 energy=-18.09980795661282  maxlinkdim=1000 maxerr=8.51E-12 time=18.649
After sweep 18 energy=-18.099807956737912  maxlinkdim=1100 maxerr=2.20E-12 time=21.792
After sweep 19 energy=-18.099807956761136  maxlinkdim=1151 maxerr=1.00E-12 time=20.824
After sweep 20 energy=-18.099807956764046  maxlinkdim=1157 maxerr=9.99E-13 time=22.259
After sweep 21 energy=-18.09980795676423  maxlinkdim=1157 maxerr=1.00E-12 time=20.940
After sweep 22 energy=-18.099807956764785  maxlinkdim=1157 maxerr=9.99E-13 time=19.367
After sweep 23 energy=-18.099807956764856  maxlinkdim=1157 maxerr=9.98E-13 time=20.888
After sweep 24 energy=-18.099807956764884  maxlinkdim=1157 maxerr=9.98E-13 time=20.439
After sweep 25 energy=-18.099807956764877  maxlinkdim=1157 maxerr=9.97E-13 time=20.650
After sweep 26 energy=-18.0998079567649  maxlinkdim=1157 maxerr=9.98E-13 time=21.515
After sweep 27 energy=-18.099807956764863  maxlinkdim=1157 maxerr=9.98E-13 time=20.950
After sweep 28 energy=-18.09980795676488  maxlinkdim=1157 maxerr=9.98E-13 time=20.055
After sweep 29 energy=-18.099807956764828  maxlinkdim=1157 maxerr=9.98E-13 time=18.967
After sweep 30 energy=-18.09980795676484  maxlinkdim=1157 maxerr=9.98E-13 time=19.914
'''
#filling 1/3
text = '''
After sweep 1 energy=-24.070946464784754  maxlinkdim=10 maxerr=5.55E-03 time=0.247
After sweep 2 energy=-26.985620196611656  maxlinkdim=20 maxerr=3.29E-03 time=0.490
After sweep 3 energy=-27.534847561127204  maxlinkdim=40 maxerr=1.49E-03 time=0.727
After sweep 4 energy=-27.78342296879399  maxlinkdim=75 maxerr=1.13E-03 time=0.961
After sweep 5 energy=-27.876751816991163  maxlinkdim=100 maxerr=8.58E-04 time=1.207
After sweep 6 energy=-27.956464778867772  maxlinkdim=150 maxerr=5.16E-04 time=1.716
After sweep 7 energy=-28.015474608452017  maxlinkdim=200 maxerr=4.10E-04 time=2.349
After sweep 8 energy=-28.052578904105307  maxlinkdim=250 maxerr=3.32E-04 time=2.984
After sweep 9 energy=-28.077978404305057  maxlinkdim=300 maxerr=2.76E-04 time=3.951
After sweep 10 energy=-28.09665279929558  maxlinkdim=350 maxerr=2.70E-04 time=6.219
After sweep 11 energy=-28.110704932253267  maxlinkdim=400 maxerr=2.70E-04 time=8.223
After sweep 12 energy=-28.12486787031795  maxlinkdim=500 maxerr=2.11E-04 time=10.353
After sweep 13 energy=-28.133849936593027  maxlinkdim=600 maxerr=1.65E-04 time=15.730
After sweep 14 energy=-28.13886531654008  maxlinkdim=700 maxerr=1.27E-04 time=19.541
After sweep 15 energy=-28.141666362472847  maxlinkdim=800 maxerr=9.80E-05 time=26.276
After sweep 16 energy=-28.14335625709692  maxlinkdim=900 maxerr=7.78E-05 time=36.682
After sweep 17 energy=-28.144477157925145  maxlinkdim=1000 maxerr=6.35E-05 time=39.275
After sweep 18 energy=-28.145211990914362  maxlinkdim=1100 maxerr=5.18E-05 time=48.206
After sweep 19 energy=-28.145718641616565  maxlinkdim=1200 maxerr=4.30E-05 time=56.794
After sweep 20 energy=-28.146081313607166  maxlinkdim=1300 maxerr=3.59E-05 time=65.466
After sweep 21 energy=-28.14635077762658  maxlinkdim=1400 maxerr=2.99E-05 time=74.129
After sweep 22 energy=-28.146555256766312  maxlinkdim=1500 maxerr=2.58E-05 time=89.303
After sweep 23 energy=-28.1467189736221  maxlinkdim=1600 maxerr=2.18E-05 time=96.691
After sweep 24 energy=-28.14684777620156  maxlinkdim=1700 maxerr=1.84E-05 time=104.774
After sweep 25 energy=-28.146948855563735  maxlinkdim=1800 maxerr=1.60E-05 time=120.801
After sweep 26 energy=-28.147029812312788  maxlinkdim=1900 maxerr=1.36E-05 time=122.737
After sweep 27 energy=-28.147095276136813  maxlinkdim=2000 maxerr=1.16E-05 time=141.300
After sweep 28 energy=-28.147096660757327  maxlinkdim=2000 maxerr=1.18E-05 time=147.003
After sweep 29 energy=-28.14709689859496  maxlinkdim=2000 maxerr=1.19E-05 time=144.617
After sweep 30 energy=-28.147096973851873  maxlinkdim=2000 maxerr=1.19E-05 time=151.637
'''
energy_values = re.findall(r'energy=(-?\d+\.\d+)', text)
energies = [float(value) for value in energy_values]
energy_errors = [abs(energies[i] - energies[i-1]) for i in range(1, len(energies) )]
fig, ax = plt.subplots(figsize=(10, 6))
ax.semilogy(sweep_indices[1:], energy_errors, marker='.', linestyle='-', color='green')
ax.set_xlabel('Index', fontsize = 'x-large')
ax.set_ylabel('Difference', fontsize = 'x-large')
ax.set_title('Energy difference for consecutive sweeps for 5 stars and filling 1/3 for J = 0.0', fontsize = 'x-large')
ax.grid(which='both', linestyle='--', linewidth=0.5)
ax.minorticks_on()
ax.grid(which='minor', alpha=0.5)
ax.grid(which='major', alpha=0.75)

ax.set_xticks(sweep_indices)
#plt.savefig('energy_convergence_5star_1_3.pgf')
plt.show()
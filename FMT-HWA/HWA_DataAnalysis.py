# -*- coding: utf-8 -*-
"""
Created on Sat May 22 14:41:01 2021

@author: Thomas
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import stats

################## Calibration Data ###########################
CalibrationFolder = 'data/Calibration'  # Path to calibation data
pivFolder = "data/piv_data"
save_fig = False

piv_files = [pivFolder + "/" + file for file in os.listdir(pivFolder)]
files = os.listdir(CalibrationFolder)  # File names in calibration folder
CalibrationData = pd.DataFrame({'X_Value': [], 'Voltage': [], 'U': []})  # Empty dataframe

U_list = np.linspace(0, 20, 11)

for file in files:  # Loop over files in folder, read file, specify velocity in df, concat to main df
    FilePath = CalibrationFolder + '/' + file  # Create path
    df = pd.read_csv(FilePath, sep=('\t'), skiprows=(22), usecols=[0, 1])
    df['U'] = float(file[-2:])
    df = df[(np.abs(stats.zscore(df["Voltage"])) < 3)]
    CalibrationData = pd.concat([CalibrationData, df], ignore_index=True)

# Obtain polyfit coefficients 4th order
coef = np.polyfit((CalibrationData[CalibrationData["U"] != 0.0])['Voltage'], (CalibrationData[CalibrationData['U']
                                                                                              != 0.0])["U"], 4)

# plot polyfit
voltages = np.linspace(1.2, 1.9, 100)
plt.figure(4, constrained_layout=True, dpi=150)
fig, ax = plt.subplots(1, 1, constrained_layout=True, dpi=150)
ax.plot(voltages, np.polyval(coef, voltages), label=r"$4^{th}$-order polynomial fit", c='C00')
ax.scatter(CalibrationData['Voltage'][::10000], CalibrationData['U'][::10000], label="measurements", c='C01', zorder=1)
ax.grid()
ax.legend(prop={"size": 14})
ax.set_xlabel("E [V]", fontsize=14)
ax.set_ylabel("U [m/s]", fontsize=14)
plt.savefig('HWA_Calibration.png', bbox_inches='tight') if save_fig else None

#################### 0 AOA ###############################
ZeroAOAFolder = 'data/0 aoa'
files = os.listdir(ZeroAOAFolder)

# List of measurement heights
HeightList = np.arange(-40, 44, 4)

# create empty df
ZeroAoAData = pd.DataFrame({'X_Value': [], 'Voltage': [], 'height': []})

# read all files and append to single df
for file in files:
    FilePath = ZeroAOAFolder + '/' + file
    df = pd.read_csv(FilePath, sep=('\t'), skiprows=(22), usecols=[0, 1])
    df['height'] = float(file[12:15])  # define height from specific data file
    df = df[(np.abs(stats.zscore(df["Voltage"])) < 3)]
    ZeroAoAData = pd.concat([ZeroAoAData, df], ignore_index=True)

# Compute velocity from voltage measurement and polyfit coefficients, add to new column in df
ZeroAoAData['U'] = np.polyval(coef, ZeroAoAData['Voltage'])
ZeroAoAData = ZeroAoAData[::2]
ZeroAoAData[ZeroAoAData["U"] < 0] = 0
# Create empty lists to append mean and rms
ZeroAoA_Mean = []
ZeroAoA_rms = []
ZeroAoA_stdev = []

for height in HeightList:  # Loop over heights
    subset = ZeroAoAData.loc[ZeroAoAData['height'] == height]  # filter specific height from df
    ZeroAoA_Mean.append(np.mean(subset['U']))  # Calculate and append mean
    ZeroAoA_rms.append(np.sqrt(np.mean(subset['U'] ** 2)))  # Calculate and append rms
    variance_u = (subset['U'] - subset['U'].mean()) ** 2  #
    # subtract mean from entries
    ZeroAoA_stdev.append(np.sqrt((1 / (variance_u.size - 1)) * variance_u.sum()))  # compute standard deviation

ZeroAoA_PlusSigma = np.array(ZeroAoA_Mean) + np.array(ZeroAoA_stdev)  # Add
# standard devioation
ZeroAoA_MinusSigma = np.array(ZeroAoA_Mean) - np.array(ZeroAoA_stdev)  #
# Subtract standard deviation


plt.figure(1, constrained_layout=True, dpi=150)
plt.plot(ZeroAoA_Mean, HeightList, marker='D', label=r'$U_{mean}$')
# plt.plot(ZeroAoA_rms, HeightList, marker='X', linestyle='--', label=r'$U_{
# rms}$')
# plt.plot(ZeroAoA_stdev, HeightList, marker='^', label=r'StDev' )
plt.plot(ZeroAoA_PlusSigma, HeightList, label=r'$1\sigma$', color='k', linewidth=0.75, linestyle='--')  # Plot plus
plt.plot(ZeroAoA_MinusSigma, HeightList, color='k', linewidth=0.75, linestyle='--')  # plot minus
plt.xlabel('U [m/s]', fontsize=14)
plt.ylabel('Height [mm]', fontsize=14)
plt.title('Angle of Attack: 0$^\circ$', fontsize=14)
plt.xlim([0,14])
plt.ylim([-40,40])
plt.legend(loc=2)
plt.grid()
plt.savefig('HWA_0AoA.pdf', bbox_inches='tight') if save_fig else None

########################### 5 AOA ################################3
FiveAOAFolder = 'data/5 aoa'
files = os.listdir(FiveAOAFolder)

FiveAoAData = pd.DataFrame({'X_Value': [], 'Voltage': [], 'height': []})

# read all files and append to single df
for file in files:
    FilePath = FiveAOAFolder + '/' + file
    df = pd.read_csv(FilePath, sep=('\t'), skiprows=(22), usecols=[0, 1])
    df['height'] = float(file[12:15])  # define height from specific data file
    df = df[(np.abs(stats.zscore(df["Voltage"])) < 3)]
    FiveAoAData = pd.concat([FiveAoAData, df], ignore_index=True)

# Compute velocity from voltage measurement and polyfit coefficients, add to new column in df
FiveAoAData['U'] = np.polyval(coef, FiveAoAData['Voltage'])
FiveAoAData = FiveAoAData[::2]
FiveAoAData[FiveAoAData["U"] < 0] = 0

# Create empty lists to append mean and rms
FiveAoA_Mean = []
FiveAoA_rms = []
FiveAoA_stdev = []
for height in HeightList:  # Loop over heights
    subset = FiveAoAData.loc[FiveAoAData['height'] == height]  # filter height from df
    FiveAoA_Mean.append(np.mean(subset['U']))  # Calculate and append mean
    FiveAoA_rms.append(np.sqrt(np.mean(subset['U'] ** 2)))  # Calculate and append rms
    variance_u = (subset['U'] - subset['U'].mean()) ** 2  #
    FiveAoA_stdev.append(np.sqrt((1 / (variance_u.size - 1)) * variance_u.sum()))  # compute standard deviation
    # standard deviation

FiveAoA_PlusSigma = np.array(FiveAoA_Mean) + np.array(FiveAoA_stdev)  # Add standard devioation
FiveAoA_MinusSigma = np.array(FiveAoA_Mean) - np.array(FiveAoA_stdev)  # Subtract standard deviation

plt.figure(2)
plt.plot(FiveAoA_Mean, HeightList, marker='D', label='$U_{mean}$')
# plt.plot(FiveAoA_rms, HeightList, marker='X', linestyle='--', label='$U_{rms}$')
plt.plot(FiveAoA_PlusSigma, HeightList, label=r'$1\sigma$', color='k', linewidth=0.75, linestyle='--')  # Plot plus
plt.plot(FiveAoA_MinusSigma, HeightList, color='k', linewidth=0.75, linestyle='--')  # plot minus
plt.xlabel('U [m/s]', fontsize=14)
plt.ylabel('Height [mm]', fontsize=14)
plt.title('Angle of Attack: 5$^\circ$', fontsize=14)
plt.legend(loc=2)
plt.grid()
<<<<<<< Updated upstream
plt.savefig('HWA_5AoA.pdf', bbox_inches='tight') if save_fig else None
=======
plt.xlim([0,14])
plt.ylim([-40,40])
plt.savefig('HWA_5AoA.pdf', bbox_inches='tight')


>>>>>>> Stashed changes

######################## 15 AOA ########################################
FifteenAOAFolder = 'data/15 aoa'
files = os.listdir(FifteenAOAFolder)

FifteenAoAData = pd.DataFrame({'X_Value': [], 'Voltage': [], 'height': []})

# read all files and append to single df
for file in files:
    FilePath = FifteenAOAFolder + '/' + file
    df = pd.read_csv(FilePath, sep=('\t'), skiprows=(22), usecols=[0, 1])
    df['height'] = float(file[12:15])  # define height from specific data file
    FifteenAoAData = pd.concat([FifteenAoAData, df], ignore_index=True)

# Compute velocity from voltage measurement and polyfit coefficients, add to new column in df    
FifteenAoAData['U'] = np.polyval(coef, FifteenAoAData['Voltage'])
FifteenAoAData = FifteenAoAData[::2]
FifteenAoAData[FifteenAoAData["U"] < 0] = 0
# Create empty lists to append mean and rms
FifteenAoA_Mean = []
FifteenAoA_rms = []
FifteenAoA_stdev = []

for height in HeightList:  # Loop over heights
    subset = FifteenAoAData.loc[FifteenAoAData['height'] == height]  # filter specific height data from df
    FifteenAoA_Mean.append(np.mean(subset['U']))  # Calculate and append mean
    FifteenAoA_rms.append(np.sqrt(np.mean(subset['U'] ** 2)))  # Calculate and append rms
    variance_u = (subset['U'] - subset['U'].mean()) ** 2  #
    FifteenAoA_stdev.append(np.sqrt((1 / (variance_u.size - 1)) * variance_u.sum()))  # compute standard deviation
    # standard deviation

FifteenAoA_PlusSigma = np.array(FifteenAoA_Mean) + np.array(FifteenAoA_stdev)  # Addstandard devioation
FifteenAoA_MinusSigma = np.array(FifteenAoA_Mean) - np.array(FifteenAoA_stdev)  # Subtract standard deviation

plt.figure(3)
plt.plot(FifteenAoA_Mean, HeightList, marker='D', label='$U_{mean}$')
# plt.plot(FifteenAoA_rms, HeightList, marker='X', linestyle='--', label='$U_{rms}$')
plt.plot(FifteenAoA_PlusSigma, HeightList, linestyle='--', label=r'$1\sigma$', color='k', linewidth=0.75)  # Plot plus
plt.plot(FifteenAoA_MinusSigma, HeightList, linestyle='--', color='k', linewidth=0.75)  # plot minus
plt.xlabel('U [m/s]', fontsize=14)
plt.ylabel('Height [mm]', fontsize=14)
plt.title('Angle of Attack: 15$^\circ$', fontsize=14)
plt.grid()
plt.legend(loc=2)
<<<<<<< Updated upstream
plt.savefig('HWA_15AoA.pdf', bbox_inches='tight') if save_fig else None
=======
plt.xlim([0,14])
plt.ylim([-40,40])
plt.savefig('HWA_15AoA.pdf', bbox_inches='tight')

>>>>>>> Stashed changes

plt.figure(6)
plt.plot(ZeroAoA_Mean, HeightList)
plt.plot(FiveAoA_Mean, HeightList)
plt.plot(FifteenAoA_Mean, HeightList)
plt.xlim([0,14])
plt.ylim([-40,40])


plt.show()

# comparison with PIV data

# load up data files
piv_0alpha = np.loadtxt(piv_files[0])
piv_5alpha = np.loadtxt(piv_files[2])
piv_15alpha = np.loadtxt(piv_files[1])

fig_mean = plt.figure(constrained_layout=True, dpi=150)

spec_mean = fig_mean.add_gridspec(2, 2)
f_mean_ax1 = fig_mean.add_subplot(spec_mean[0, 0])
f_mean_ax2 = fig_mean.add_subplot(spec_mean[1, 0])
f_mean_ax3 = fig_mean.add_subplot(spec_mean[:, 1])

# HWA data
f_mean_ax1.plot(ZeroAoA_Mean, HeightList, label="HWA")
f_mean_ax2.plot(FiveAoA_Mean, HeightList)
f_mean_ax3.plot(FifteenAoA_Mean, HeightList)

# PIV data
f_mean_ax1.plot(piv_0alpha[::-1, 0], piv_0alpha[:, -1], label="PIV")
f_mean_ax2.plot(piv_5alpha[::-1, 0], piv_5alpha[:, -1])
f_mean_ax3.plot(piv_15alpha[::-1, 0], piv_15alpha[:, -1])

f_mean_ax2.set_xlabel("y [mm]")
f_mean_ax3.set_xlabel("y [mm]")
f_mean_ax1.set_ylabel(r"$U_{mean}$ [m/s]")
f_mean_ax2.set_ylabel(r"$U_{mean}$ [m/s]")

f_mean_ax1.grid()
f_mean_ax2.grid()
f_mean_ax3.grid()

fig_rms = plt.figure(constrained_layout=True, dpi=150)

spec_rms = fig_rms.add_gridspec(2, 2)
f_rms_ax1 = fig_rms.add_subplot(spec_rms[0, 0])
f_rms_ax2 = fig_rms.add_subplot(spec_rms[1, 0])
f_rms_ax3 = fig_rms.add_subplot(spec_rms[:, 1])

# HWA data
f_rms_ax1.plot(ZeroAoA_stdev, HeightList, label="HWA")
f_rms_ax2.plot(FiveAoA_stdev, HeightList)
f_rms_ax3.plot(FifteenAoA_stdev, HeightList)

# PIV data
f_rms_ax1.plot(piv_0alpha[::-1, 1], piv_0alpha[:, -1], label="PIV")
f_rms_ax2.plot(piv_5alpha[::-1, 1], piv_5alpha[:, -1])
f_rms_ax3.plot(piv_15alpha[::-1, 1], piv_15alpha[:, -1])

f_rms_ax2.set_xlabel("y [mm]")
f_rms_ax3.set_xlabel("y [mm]")
f_rms_ax1.set_ylabel(r"$U_{rms}$ [m/s]")
f_rms_ax2.set_ylabel(r"$U_{rms}$ [m/s]")

f_rms_ax1.grid()
f_rms_ax2.grid()
f_rms_ax3.grid()

fig, ax = plt.subplots(2, 3, constrained_layout=True, dpi=150, sharey=True)

hwa_data_rms = [ZeroAoA_stdev, FiveAoA_stdev, FifteenAoA_stdev]
hwa_data_mean = [ZeroAoA_Mean, FiveAoA_Mean, FifteenAoA_Mean]
piv_data = [piv_0alpha, piv_5alpha, piv_15alpha]

for axi_mean, axi_rms, hwa_mean_i, hwa_rms_i, piv_data_i in zip(ax[0], ax[1], hwa_data_mean, hwa_data_rms, piv_data):

    # HWA data
    axi_mean.plot(hwa_mean_i, HeightList,  label="HWA")
    axi_rms.plot(hwa_rms_i, HeightList)

    # PIV data
    axi_mean.plot(piv_data_i[::-1, 0], piv_data_i[:, -1], label="PIV")
    axi_rms.plot(piv_data_i[::-1, 1], piv_data_i[:, -1])

    axi_rms.grid()
    axi_mean.grid()

    # axi_rms.set_xlim(12, 0)
    # axi_mean.set_xlim(0, 12)
    axi_rms.invert_xaxis()

ax[0, 0].legend()
ax[0, 1].set_xlabel(r"$U_{mean}$ [m/s]", fontsize=12)
ax[1, 1].set_xlabel(r"$U_{rms}$ [m/s]", fontsize=12)
ax[0, 0].set_ylabel("y [mm]", fontsize=12)
ax[1, 0].set_ylabel("y [mm]", fontsize=12)

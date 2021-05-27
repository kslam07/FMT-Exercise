# -*- coding: utf-8 -*-
"""
Created on Sat May 22 14:41:01 2021

@author: Thomas
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

################## Calibration Data ###########################
CalibrationFolder = 'data/Calibration'  # Path to calibation data
files = os.listdir(CalibrationFolder)  # File names in calibration folder
CalibrationData = pd.DataFrame({'X_Value': [], 'Voltage': [], 'U': []})  # Empty dataframe

U_list = np.linspace(0, 20, 11)

for file in files:  # Loop over files in folder, read file, specify velocity in df, concat to main df
    FilePath = CalibrationFolder + '/' + file  # Create path
    df = pd.read_csv(FilePath, sep=('\t'), skiprows=(22), usecols=[0, 1])
    df['U'] = float(file[-2:])
    CalibrationData = pd.concat([CalibrationData, df], ignore_index=True)

# Obtain polyfit coefficients 4th order
coef = np.polyfit(CalibrationData['Voltage'], CalibrationData['U'], 4)

# plot polyfit
voltages = np.linspace(1.1, 1.9, 100)
plt.figure(4, constrained_layout=True, dpi=150)
fig, ax = plt.subplots(1, 1, constrained_layout=True, dpi=150)
ax.plot(voltages, np.polyval(coef, voltages), label=r"$4^{th}$-order polynomial fit", c='C00')
ax.scatter(CalibrationData['Voltage'][::10000], CalibrationData['U'][::10000], label="measurements", c='C01', zorder=1)
ax.grid()
ax.legend(prop={"size": 14})
ax.set_xlabel("E [V]", fontsize=14)
ax.set_ylabel("U [m/s]", fontsize=14)
plt.savefig('HWA_Calibration.png', bbox_inches='tight')

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
    ZeroAoAData = pd.concat([ZeroAoAData, df], ignore_index=True)

# Compute velocity from voltage measurement and polyfit coefficients, add to new column in df
ZeroAoAData['U'] = np.polyval(coef, ZeroAoAData['Voltage'])
ZeroAoAData = ZeroAoAData[::2]

# Create empty lists to append mean and rms
ZeroAoA_Mean = []
ZeroAoA_rms = []
ZeroAoA_stdev = []

for height in HeightList:  # Loop over heights
    subset = ZeroAoAData.loc[ZeroAoAData['height'] == height]  # filter specific height from df
    ZeroAoA_Mean.append(np.mean(subset['U']))  # Calculate and append mean
    ZeroAoA_rms.append(np.sqrt(np.mean(subset['U'] ** 2)))  # Calculate and append rms
    subset['UminusMean2'] = (subset['U'] - np.mean(subset['U'])) ** 2  #
    # subtract mean from entries
    ZeroAoA_stdev.append(np.sqrt((1 / (subset['UminusMean2'].size - 1)) *
                                 subset[
                                     'UminusMean2'].sum()))  # compute standard deviation

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
plt.legend(loc=2)
plt.grid()
plt.savefig('HWA_0AoA.pdf', bbox_inches='tight')

########################### 5 AOA ################################3
FiveAOAFolder = 'data/5 aoa'
files = os.listdir(FiveAOAFolder)

FiveAoAData = pd.DataFrame({'X_Value': [], 'Voltage': [], 'height': []})

# read all files and append to single df
for file in files:
    FilePath = FiveAOAFolder + '/' + file
    df = pd.read_csv(FilePath, sep=('\t'), skiprows=(22), usecols=[0, 1])
    df['height'] = float(file[12:15])  # define height from specific data file
    FiveAoAData = pd.concat([FiveAoAData, df], ignore_index=True)

# Compute velocity from voltage measurement and polyfit coefficients, add to new column in df
FiveAoAData['U'] = np.polyval(coef, FiveAoAData['Voltage'])
FiveAoAData = FiveAoAData[::2]

# Create empty lists to append mean and rms
FiveAoA_Mean = []
FiveAoA_rms = []
FiveAoA_stdev = []
for height in HeightList:  # Loop over heights
    subset = FiveAoAData.loc[FiveAoAData['height'] == height]  # filter height from df
    FiveAoA_Mean.append(np.mean(subset['U']))  # Calculate and append mean
    FiveAoA_rms.append(np.sqrt(np.mean(subset['U'] ** 2)))  # Calculate and append rms
    subset['UminusMean2'] = (subset['U'] - np.mean(subset['U'])) ** 2  # subtract mean from entries
    FiveAoA_stdev.append(np.sqrt((1 / (subset['UminusMean2'].size - 1)) * subset['UminusMean2'].sum()))  # compute
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
plt.savefig('HWA_5AoA.pdf', bbox_inches='tight')

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

# Create empty lists to append mean and rms
FifteenAoA_Mean = []
FifteenAoA_rms = []
FifteenAoA_stdev = []

for height in HeightList:  # Loop over heights
    subset = FifteenAoAData.loc[FifteenAoAData['height'] == height]  # filter specific height data from df
    FifteenAoA_Mean.append(np.mean(subset['U']))  # Calculate and append mean
    FifteenAoA_rms.append(np.sqrt(np.mean(subset['U'] ** 2)))  # Calculate and append rms
    subset['UminusMean2'] = (subset['U'] - np.mean(subset['U'])) ** 2  # subtract mean from entries
    FifteenAoA_stdev.append(np.sqrt((1 / (subset['UminusMean2'].size - 1)) * subset['UminusMean2'].sum()))  # compute
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
plt.savefig('HWA_15AoA.pdf', bbox_inches='tight')

plt.show()

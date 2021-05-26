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
CalibrationFolder = 'data/Calibration'  #Path to calibation data
files = os.listdir(CalibrationFolder)   # File names in calibration folder
CalibrationData = pd.DataFrame({'X_Value': [], 'Voltage':[], 'U':[]}) #Empty dataframe

U_list = np.linspace(0,20,11)

for file in files: #Loop over files in folder, read file, specify velocity in df, concat to main df
    FilePath = CalibrationFolder + '/' + file  # Create path
    df = pd.read_csv(FilePath, sep=('\t'), skiprows=(22), usecols=[0,1])  
    df['U'] = float(file[-2:])
    CalibrationData = pd.concat([CalibrationData,df], ignore_index=True)

# Obtain polyfit coefficients 4th order
coef = np.polyfit(CalibrationData['Voltage'], CalibrationData['U'], 4)

# plot polyfit
voltages = np.linspace(1.1, 1.9, 100)
fig, ax = plt.subplots(1, 1, constrained_layout=True, dpi=150)
ax.plot(voltages, np.polyval(coef, voltages), label=r"$4^{th}$-order polynomial fit", c='C00')
ax.scatter(CalibrationData['Voltage'][::10000], CalibrationData['U'][::10000], label="measurements", c='C01', zorder=1)
ax.grid()
ax.legend(prop={"size": 14})
ax.set_xlabel("E [V]", fontsize=14)
ax.set_ylabel("U [m/s]", fontsize=14)
#################### 0 AOA ###############################
ZeroAOAFolder = 'data/0 aoa'
files = os.listdir(ZeroAOAFolder)

#List of measurement heights
HeightList = np.arange(-40,44,4)

# create empty df
ZeroAoAData = pd.DataFrame({'X_Value': [], 'Voltage':[], 'height':[]})

# read all files and append to single df
for file in files:
    FilePath = ZeroAOAFolder + '/' + file
    df = pd.read_csv(FilePath, sep=('\t'), skiprows=(22), usecols=[0,1])
    df['height'] = float(file[12:15])       # define height from specific data file
    ZeroAoAData = pd.concat([ZeroAoAData, df], ignore_index=True)

# Compute velocity from voltage measurement and polyfit coefficients, add to new column in df
ZeroAoAData['U'] = np.polyval(coef,ZeroAoAData['Voltage'])

# Create empty lists to append mean and rms
ZeroAoA_Mean = []
ZeroAoA_rms = []
for height in HeightList: # Loop over heights
    subset = ZeroAoAData.loc[ZeroAoAData['height']==height]     # filter specific height from df
    ZeroAoA_Mean.append(np.mean(subset['U']))                   # Calculate and append mean
    ZeroAoA_rms.append(np.sqrt(np.mean(subset['U']**2)))        # Calculate and append rms

plt.figure(1)
plt.plot(ZeroAoA_Mean, HeightList, marker='D', label='mean')
plt.plot(ZeroAoA_rms, HeightList, marker='X', linestyle='--', label='rms')
plt.xlabel('U [m/s]')
plt.ylabel('Height [mm]')
plt.title('AoA=0[$^\circ$]')
plt.legend()

########################### 5 AOA ################################3
ZeroAOAFolder = 'data/5 aoa'
files = os.listdir(ZeroAOAFolder)

ZeroAoAData = pd.DataFrame({'X_Value': [], 'Voltage':[], 'height':[]})

# read all files and append to single df
for file in files:
    FilePath = ZeroAOAFolder + '/' + file
    df = pd.read_csv(FilePath, sep=('\t'), skiprows=(22), usecols=[0,1])
    df['height'] = float(file[12:15])   # define height from specific data file
    ZeroAoAData = pd.concat([ZeroAoAData, df], ignore_index=True)
   
# Compute velocity from voltage measurement and polyfit coefficients, add to new column in df
ZeroAoAData['U'] = np.polyval(coef,ZeroAoAData['Voltage'])

# Create empty lists to append mean and rms
ZeroAoA_Mean = []
ZeroAoA_rms = []
for height in HeightList: # Loop over heights
    subset = ZeroAoAData.loc[ZeroAoAData['height']==height]     # filter height from df
    ZeroAoA_Mean.append(np.mean(subset['U']))                   # Calculate and append mean
    ZeroAoA_rms.append(np.sqrt(np.mean(subset['U']**2)))        # Calculate and append rms

plt.figure(2)
plt.plot(ZeroAoA_Mean, HeightList, marker='D', label='mean')
plt.plot(ZeroAoA_rms, HeightList, marker='X', linestyle='--', label='rms')
plt.xlabel('U [m/s]')
plt.ylabel('Height [mm]')
plt.title('AoA=5$^\circ$')
plt.legend()


######################## 15 AOA ########################################
ZeroAOAFolder = 'data/15 aoa'
files = os.listdir(ZeroAOAFolder)

ZeroAoAData = pd.DataFrame({'X_Value': [], 'Voltage':[], 'height':[]})

# read all files and append to single df
for file in files:
    FilePath = ZeroAOAFolder + '/' + file
    df = pd.read_csv(FilePath, sep=('\t'), skiprows=(22), usecols=[0,1])
    df['height'] = float(file[12:15])       # define height from specific data file
    ZeroAoAData = pd.concat([ZeroAoAData, df], ignore_index=True)

# Compute velocity from voltage measurement and polyfit coefficients, add to new column in df    
ZeroAoAData['U'] = np.polyval(coef,ZeroAoAData['Voltage'])

# Create empty lists to append mean and rms
ZeroAoA_Mean = []
ZeroAoA_rms = []
for height in HeightList: # Loop over heights
    subset = ZeroAoAData.loc[ZeroAoAData['height']==height]     # filter specific height data from df
    ZeroAoA_Mean.append(np.mean(subset['U']))                   # Calculate and append mean
    ZeroAoA_rms.append(np.sqrt(np.mean(subset['U']**2)))        # Calculate and append rms

plt.figure(3)
plt.plot(ZeroAoA_Mean, HeightList, marker='D', label='mean')
plt.plot(ZeroAoA_rms, HeightList, marker='X', linestyle='--', label='rms')
plt.xlabel('U [m/s]')
plt.ylabel('Height [mm]')
plt.title('AoA=15$^\circ$')
plt.legend()




import pandas as pd
import numpy as np
import re
import matplotlib as mpl
import matplotlib.pyplot as plt

#filelists =['temp20.csv', 'temp10.csv','temp5.csv', 'temp0.csv']
#templists = ['30','25','20','15','12','10','5','2','0']
filelists =['temp20.csv', 'temp10.csv', 'temp0.csv']
templists = ['20','10','0']

"""
for i in range(len(filelists)):
    text = re.search('[0-9]?', filelists[i]).group
    templists.append(str(text)+"[degrees Celsius]")
    print(text)
    print(templists)
"""


#import the measured value by kikusuiBPChecker   #check csv-name
for i in range(len(filelists)):
    exec("df_"+str(i)+" = pd.read_csv("+'"'+filelists[i]+'"'+", names=\
        ('Capacity','Power','Voltage'), skiprows=61,header=None,usecols=\
        [4,5,7], dtype={'Capacity': float, 'Power': float, 'Voltage': float})")

#make pandas dataframe list
dfs=[]
for i in range(len(filelists)):
    exec("dfs.append(df_"+str(i)+")")


#remove outliers and redundant row including NaN
for df in dfs:
    df.dropna(subset=['Voltage'],inplace=True)
    df.reset_index(inplace=True,drop=True)          
    for i in range(len(df)):
        if i == len(df):
            break 
        if df.iloc[i,2] <= 2.75 :
            df.drop(df.index[i],inplace=True)
            df.reset_index(inplace=True,drop=True)

'''
for df in dfs:
    for i in range(len(df)):
        if i == len(df):
            break 
        if df.iloc[i,2] > 3.8995 and df.iloc[i,2] < 3.9005:
            print(df.iloc[i,2])
            print("i=%d" % i)
'''
"""
for df in dfs:
    for i in range(len(df)):
        if i == len(df):
            break 
        if df.iloc[i,2] > 3.914999 and df.iloc[i,2] < 3.91501:
            print(df.iloc[i,2])
            print("i=%d" % i)

"""
'''
print(df_0.loc[766])
print(df_0.loc[len(df_0)-1])
print(df_0.iloc[766,1]/df_0.iloc[len(df_0)-1,1]*100)
'''

DOD_Voltage_row_index = []

for df in dfs:
    DOD_Threshold_Power = df.iloc[len(df)-1,1]*df_0.iloc[766,1]/df_0.iloc[len(df_0)-1,1]
    for i in range(len(df)):
        if i == len(df):
            break 
        if df.iloc[i,1] > DOD_Threshold_Power-0.001 and \
                df.iloc[i, 1] < DOD_Threshold_Power+0.001:
            #print(df.iloc[i,1])
            #print("i=%d" % i)
            DOD_Voltage_row_index.append(i)
            break 

Same_DOD_Catalogs = [[0 for i in range(3)] for j in range(len(DOD_Voltage_row_index))]
i=0
for df in dfs:
    for j in range(3):
        Same_DOD_Catalogs[i][j] = df.iloc[DOD_Voltage_row_index[i],j]
    i=i+1


i=0
for df in dfs:
    print('\n'+templists[i]+'[degree]')
    print(df.loc[DOD_Voltage_row_index[i]])
    #print(df.iloc[DOD_Voltage_row_index[i],2])
    i=i+1

############
#↓graph plot
i=0
for df in dfs:
    exec("x1"+str(i)+"_list = df['Capacity'].tolist()")
    exec("x2"+str(i)+"_list = df['Power'].tolist()")
    exec("y1"+str(i)+"_list = df['Voltage'].tolist()")
    exec("y2"+str(i)+"_list = df['Voltage'].tolist()")
    i=i+1

MeasurementTargetName = 'Temperature Characteristics'    #check

fig = plt.figure()
fig.suptitle(MeasurementTargetName)
colors = ['orangered', 'cornflowerblue', 'limegreen', 'pink',\
     'violet', 'red', 'blue', 'green']


# row:2 column:1 upper
ax1 = fig.add_subplot(211, xlabel = 'discharge [mAh]', ylabel = 'Voltage [V]',xlim= (0,1750), ylim= (2.75,4.2))
for i in range(len(filelists)):
    exec("ax1.plot(x1"+str(i)+"_list, y1"+str(i)+'_list, lw=2, marker="", color =\
         colors['+str(i)+"], label = templists["+str(i)+"])")
ax1.legend()

plt.hlines(y=[3.29, 3.39, 3.50], xmin=0, xmax=1750, lw=1, linestyles='dashdot', label='sleep-in')
for i in range(len(Same_DOD_Catalogs)):
    plt.hlines(y=Same_DOD_Catalogs[i][2], xmin=0, xmax=1750, lw=0.8, linestyles='dotted', label='sleep-in')
    plt.vlines(x=Same_DOD_Catalogs[i][0], ymin=2.75, ymax=4, lw=0.8, linestyles='dotted', label='sleep-in')
    ax1.scatter(Same_DOD_Catalogs[i][0], Same_DOD_Catalogs[i][2], c='red', s=10)
plt.grid()


# row:2 column:1 lower
plotarea_x_max = 6.62273456
ax2 = fig.add_subplot(212,  xlabel = 'discharge [Wh]', ylabel = 'Voltage [V]',xlim= (0,plotarea_x_max), ylim= (2.75,4.2))
for i in range(len(filelists)):
    exec("ax2.plot(x2"+str(i)+"_list, y2"+str(i)+'_list, lw=2, marker="", color =\
         colors['+str(i)+"], label = templists["+str(i)+"])")
ax2.legend()


plt.hlines(y=[3.29, 3.39, 3.50], xmin=0, xmax=plotarea_x_max, lw=1, linestyles='dashdot', label='sleep-in')
for i in range(len(Same_DOD_Catalogs)):
    plt.hlines(y=Same_DOD_Catalogs[i][2], xmin=0, xmax=plotarea_x_max, lw=0.8, linestyles='dotted', label='sleep-in')
    plt.vlines(x=Same_DOD_Catalogs[i][1], ymin=2.75, ymax=4, lw=0.8, linestyles='dotted', label='sleep-in')
    ax2.scatter(Same_DOD_Catalogs[i][1], Same_DOD_Catalogs[i][2], c='red', s=10)
plt.grid()


plt.show()

"""
text = f"Power Consumption = {powerConsumption/measuredTimeSum} [W]\nConsumption = {powerConsumption/3600.0} [Wh]\nMeasurment Time = {measuredTimeSum} [s]"
print(text)

"""
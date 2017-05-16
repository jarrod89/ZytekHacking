# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 18:30:23 2016

@author: Jarrod
IDs=IDcounts.index.values.tolist() #[2, 110, 115, 125, 120, 165, 130]
IDsToMotor=[2, 102, 110, 112, 115] #IDs that control the motor
IDsFromMotor=[120, 125, 130, 135, 140, 145, 165, 185] #IDs that the motor generates
IDsOther=[101, 202] #other ids?

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#df=pd.read_csv('REVERSE With Digital Toggle SMART ED Drivetrain Slow Drive Long  Enable SMART 352.2vSeven 323.5V 0x01 switch byte.csv')
#df=df.drop('nan',1)
dataConverters = {
    "Time Stamp": lambda x: int(x,10),
    "D1": lambda x: int(x, 16),
    "D2": lambda x: int(x, 16),
    "D3": lambda x: int(x, 16),
    "D4": lambda x: int(x, 16),
    "D5": lambda x: int(x, 16),
    "D6": lambda x: int(x, 16),
    "D7": lambda x: int(x, 16),
    "D8": lambda x: int(x, 16)
}
df=pd.read_csv('With Digital Toggle SMART ED Drivetrain Slow Drive Enable 324.6v 0x101 .csv', converters=dataConverters)
#convert from microseconds to seconds  
T0=df['Time Stamp'][0]
df['Time'] = [(i-T0)/1.0E6 for i in df['Time Stamp']]

#print the id counts
IDcounts=df['ID'].value_counts()
print(IDcounts)

#IDs to plot
df002=df[df['ID'] == 2 ]
df102=df[df['ID'] == 102 ]
df110=df[df['ID'] == 110 ] #crc in D5
df112=df[df['ID'] == 112 ]
df115=df[df['ID'] == 115 ] #crc in D7
#motor produced messages
df130=df[df['ID'] == 130 ] #D2+D3 equal voltage

df101=df[df['ID'] == 101 ]
ignTime=df101.Time.iloc[0]
#CRC width=8  poly=0x1d  init=0xff  refin=false  refout=false  xorout=0xff  check=0x4b  residue=0xc4  name="CRC-8/SAE-J1850"
l1=14.5
l2=26.0
#size of figures
figs=(16,4)
if 1:
    df1=df130
    #process Bytes
    D34=df1['D3']*256 + df1['D4'] # Bus voltage, integer volts, verified with DC supply.
    D12=df1['D1']*256 + df1['D2'] - int(0x8000)#signed int, motor current? no, appears to be a 20ms delay replica of D34 in 0x115
    D5=df1['D5'] #Status register? maybe not an integer
    
    D6=df1['D6'] #up ctr
    D7=df1['D7'] #CRC
    
    #extract time stamps from messages for plotting
    T=df1['Time']
    #set up figure size
    fig=plt.figure(figsize = figs)
    ax1 = fig.add_subplot(111)
    ax2 = fig.add_subplot(111, sharex=ax1, frameon=False)
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    
    #plot data against time and label the line
    ax1.plot(T,D34,'r-',markersize=2,label='D34')
    ax1.plot(T,D5,'g-',markersize=10,label='D5')
    ax2.plot(T,D12,'-',markersize=2,label='D12')
    
    #Title the plot
    plt.title("Message ID: " + str(df1.iloc[0]["ID"]))
    #show legend
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    plt.xlim(l1,l2)
    plt.axvline(x=ignTime)
    plt.show()

if 1:
    df1=df115
    
    #process Bytes
    D34=df1['D3']*256 + df1['D4'] - int(0x8000)# signed int, commanded current?
    D12=df1['D1']*256 + df1['D2'] - int(0x8000)# signed int, enable signal?
    
    D5=df1['D5'] #always zero?
    D6=df1['D6'] #up ctr
    D7=df1['D7'] #CRC
    
    #extract time stamps from messages for plotting
    T=df1['Time']
    #set up figure size
    fig=plt.figure(figsize = figs)
    ax1 = fig.add_subplot(111)
    ax2 = fig.add_subplot(111, sharex=ax1, frameon=False)
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    
    #plot data against time and label the line
    ax1.plot(T,D34,'r-',markersize=2,label='D34')
    ax2.plot(T,D12,'-',markersize=2,label='D12')
    #ax2.plot(T,D5,'-',markersize=2,label='D5')
    #ax1.plot(T,D5,'.',markersize=10,label='D5')
    
    #Title the plot
    plt.title("Message ID: " + str(df1.iloc[0]["ID"]))
    #show legend
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")   
    plt.xlim(l1,l2)
    plt.axvline(x=ignTime)
    plt.show()

if 1:    
    df1=df110
    
    #extract time stamps from messages for plotting
    T=df1['Time']
    
    D1=df1['D1']#*256 + df1['D2']# - int(0x8000)#32768 signed int
    D2=df1['D2']
    D3=df1['D3'] #bit0 disable signal?
    
    D4=df1['D4'] #up ctr
    D5=df1['D5'] #CRC
    data=np.zeros((D1.size,8),np.int8)
    for n in range(D1.size):
        binstr=bin(D1.iloc[n])
        strlen=len(binstr)
        for m in range(strlen-2):
            i=strlen-m-1
            data[n][7-m] = int(binstr[i]) + 2*(7-m)
    
    #set up figure size
    fig=plt.figure(figsize = figs)
    ax1 = fig.add_subplot(111)
    ax2 = fig.add_subplot(111, sharex=ax1, frameon=False)
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    
    #plot data against time and label the line
    ax1.plot(T,data,'-',markersize=2,label='D1')
    #ax2.plot(T,D2,'.',markersize=2,label='D2')
    #ax2.plot(T,D3,'.',markersize=2,label='D3')
    #ax1.plot(T,D5,'.',markersize=10,label='D5')
    
    #Title the plot
    plt.title("Message ID: " + str(df1.iloc[0]["ID"]))
    #show legend
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")   
    plt.xlim(l1,l2)
    plt.show()

"""
#Data bytes to plot]#
Ds=['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8']
#Ds=['D1','D2','D3','D4']
def plotCan(df1):
    fig=plt.figure(figsize = (16,8))
    #extract time stamps from messages for plotting
    T=[int(i,10) for i in df1['Time Stamp'].astype(str)]
    #convert from microseconds to seconds    
    T= [(i-T[0])/1E6 for i in T]
    #set up figure size
    #fig=plt.figure(figsize = (16,10))
    #iterate through data bytes in messages and plot each on the same graph
    D34=[int(i,16) for i in (df1['D3']+df1['D4']) ]
    D12=[int(i,16) for i in (df1['D1']+df1['D2']) ]
    
    D6=[int(i,16) for i in df1['D6'] ]
    D7=[int(i,16) for i in df1['D7'] ]
    
    #plot data against time and label the line
    plt.plot(T,D12,'-',markersize=2,label='D12')
    plt.plot(T,D34,'-',markersize=2,label='D34')
    #plt.plot(T,D6,'.',markersize=10,label='D6')
    #plt.plot(T,D7,'.',markersize=10,label='D7')
    #D6D7=[b*a for a,b in zip(D6,D7)]
    
    #Title the plot
    plt.title("Message ID: " + str(id))
    #plt.title("0-15 counters")
    #show legend
    plt.legend()
    #limit the range
    #plt.xlim(0, 10)
    #plt.ylim(0, 16)
    #display the plot
    plt.show()

plotCan(df[df['ID'] == 115 ])
plotCan(df[df['ID'] == 110 ])
plotCan(df[df['ID'] == 120 ])
"""

"""
ID5=[125]
ID6=[115, 130]
ID7=[120, 165]
ID8=[110]

    #for d in Ds:
    if id in ID5:
        d='D5'
    elif id in ID6:
        d='D6'
    elif id in ID7:
        d='D7'
    elif id in ID8:
        d='D8'
    else:
        d='D8'
    print(id)
    print(d)

    df2=df1[df1[d] == '0F']
    T=[int(i,10) for i in df2['Time Stamp'].astype(str)]
    print('length',len(T))
    if id == 110:
        Tdf=pd.DataFrame(data={'T110': T})
    else:
        Tdf[id]=T
"""
"""
    #extract data column
    D=[int(i,16) for i in df1[d]]
    #plot data against time and label the line
    plt.plot(T,D,'-',markersize=2,label=str(id)+' '+d)
"""    
"""
    for n in range(0,16):
        print(n)
        D6D7=[]
        for a,b in zip(D6,D7):
            if(a == n):
                D6D7.extend([b])
        plt.plot(D6D7,label=n)
"""

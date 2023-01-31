# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 19:22:30 2022

@author: osjac
"""

import matplotlib.pyplot as plt
import pydarn
import bz2
import datetime
import numpy as np
import pandas as pd
import os
#fitacf_file = r"C:\Users\osjac\Documents\UNI\Masters\Code\20020208.1600.00.pgr.fitacf.bz2"

#fitacf_file = r"C:\Users\osjac\Documents\19960117.2000.00.han.fitacf.bz2"


def DataProcessing(fitacf_FilePath):

    with bz2.open(fitacf_FilePath) as fp:
        fitacf_stream = fp.read()
        
    reader = pydarn.SuperDARNRead(fitacf_stream, True)
    ord_list = reader.read_fitacf()
    
    parameters = ["p_l",
                  "v",
                  "w_l"]
    
    maxRangeGate = 70
    minRangeGate = 0
    
    dataPoints = np.array([0,0,0,0,0,0,0])
    
    for beam in ord_list: 
        
        bmnum = beam["bmnum"]
        bmazm = beam["bmazm"]
        rsep  = beam["rsep"]
        frang = beam["frang"]
        time  = beam["time.hr"] + beam["time.mt"]/60 + beam["time.sc"]/360
        #time = beam["time.mt"] + beam["time.sc"]/60 + beam["time.us"]/360
        badGates = False
        
        try:
            goodGates = beam['slist']
            goodGatesNum = len(goodGates)
        except:
            badGates = True
            goodGatesNum = 0
        
        if not badGates:
            temp = []
            temp.append(((goodGates*rsep)+frang))
            
            for parm in parameters:
                temp.append(beam[parm])
                
            temp = np.transpose(temp)   
            temp = np.hstack((temp , np.full((goodGatesNum,1),time)))
            temp = np.hstack((temp , np.full((goodGatesNum,1),bmazm)))
            temp = np.hstack((temp , np.full((goodGatesNum,1),bmnum)))
            
            dataPoints = np.vstack((dataPoints,temp))
            
    
    dataPoints = np.delete(dataPoints, 0, 0)
    dataPoints = dataPoints[dataPoints[:,4].argsort()]
    
    return dataPoints


def SaveDataToCSV(data_np,fileName):
    df = pd.DataFrame(data_np,columns=["r (km)","Power (dB)","Velocity (m/s)","Spectral width (m/s)","time (hr)","beam azmimuth (deg)","beam number (int)"])
    df.to_csv(fileName)

#===============================================================================

# fitacf_file = r"C:\Users\osjac\OneDrive - University of Southampton\Masters\Code\20020208.1600.00.pgr.fitacf.bz2"
# ProcessedData_np = DataProcessing(fitacf_file)

# SaveDataToCSV(ProcessedData_np, "processedData.csv")



StartingDir = r"C:\Users\osjac\OneDrive - University of Southampton\Masters\Data\2015"
EndingDir = r"C:\Users\osjac\OneDrive - University of Southampton\Masters\Data_Processed_RCC\2015"

for filename in os.listdir(StartingDir):
    f = os.path.join(StartingDir, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print("Processing",f)
        fitacf_file = f
        ProcessedData_np = DataProcessing(fitacf_file)
        SaveDataToCSV(ProcessedData_np, EndingDir + "\\" + os.path.basename(f)[:-10]+"processedRCC.csv")
        
        















import csv,time,ast,sys,os
import graph
import collections

# detemine mininum gas cost for (fix_minimum type)
def minimunFixGas(csv_reader):
    (g, _, _, _, _) = graph.seperateTxStatus(csv_reader)
    return g[0]

# receive list of tuple (gas,count) in reverse to process tx count after the gas point
# return list of gas (x-axis) and count (y-axis)
def calOverhead(counter):
    totalTx = 0
    tick = 0
    for i in counter:
        totalTx += i[1]
    overhead,overheadCount = [],[]
    for i in range(len(counter)):
        overhead.append(counter[i][0])
        overheadCount.append(totalTx-counter[i][1]-tick)
        tick += counter[i][1]
    return (overhead,overheadCount)

def overheadTx(csv_reader):
    (g, s, _, _, _) = graph.seperateTxStatus(csv_reader)
    gCounter = sorted(collections.Counter(g).items())
    sCounter = sorted(collections.Counter(s).items())

    gOH = calOverhead(gCounter)
    sOH = calOverhead(sCounter)
    return gOH,sOH

def successFromOH(gOH,sOH):
    (g,gc,s,sc) = (gOH[0][:],gOH[1][:],sOH[0][:],sOH[1][:])  
    sIndex = 0
    rate = []
    
    for i in range(len(g)):
        try:
            while(g[i] > s[sIndex]):
                sIndex += 1
            rate.append(round((sc[sIndex]/(gc[i]+sc[sIndex]))*100,2))
        except:
            rate.append(0.00)
        #print(g[i],gc[i],'\t',s[i],sc[i])
    return rate

def cumulativeTimpstamp(tList):
    result = []
    tmp = 0
    count = 0
    for item in range(len(tList)):
        count += 1
        if(tList[item] != tmp):
            if(tmp != 0): result.append([tList[item],count])
            tmp = item
    return result
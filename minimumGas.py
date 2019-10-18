import csv,time,ast,sys,os
import graph
import collections
import catagorize as cat
from termcolor import colored

# detemine mininum gas cost for (fix_minimum type)
# return first success
def minimunFixGas_fix_oneGasFail(cm):
    file = 'cm\\' +  cm[0] + '_' + cm[1] + '.csv'
    csv_file = open(file, 'r')
    csv_reader = csv.reader(csv_file, delimiter=',')
    (_, s, _, _, _) = graph.seperateTxStatus(csv_reader)
    csv_file.close()
    return s[0]

#this one return gas at error point
def minimunFixGas_uncatagorized(cm):
    file = 'cm\\' +  cm[0] + '_' + cm[1] + '.csv'
    csv_file = open(file, 'r')
    csv_reader = csv.reader(csv_file, delimiter=',')
    goh,soh = overheadTx(csv_reader)
    rate = successFromOH(goh,soh)
    csv_file.close()

    thershold = goh[0][-1]
    recommend = 0
    for sGas in soh[0]:
        if(sGas >= thershold):
            recommend = sGas
            break

    #start above 80
    if(rate[0] > 80): return ("Above 80%", goh[0][0], recommend)

    #jump pass 70 and diff=3
    diffRate = []
    start  = 0
    for i in rate:
        diffRate.append(round((i-start),2))
        start = i
    for i in range(1,len(rate)):
        if(diffRate[i]>3.00 and rate[i]>=70):
            #print(colored(str(rate[i])+'\t'+str(diffRate[i])+'\t'+str(goh[0][i]), 'red'))
            return ('Pass 70% Jump 3%', goh[0][i], recommend)
        else:
            pass
            #print(colored(str(rate[i])+'\t'+str(diffRate[i])+'\t'+str(goh[0][i]), 'white'))

    #slightly pass 75%
    for i in range(1,len(rate)):
        if(rate[i] > 75):
            return ('Slightly pass 75%', goh[0][i], recommend)
    
    #Pass
    maxRate = (-1,0)
    for i in range(1,len(rate)):
        if(rate[i] > maxRate[1]):
            maxRate = (i,rate[i])
    return ('Max rate', goh[0][maxRate[0]], goh[0][maxRate[0]])

# return type, minimum_gas, recommend_gas
def calMinimumGas(cm,txStatus):
    typee = cat.checkType(txStatus)
    if(typee == 'Only_out_of_gas' or typee == 'Never_Success'): 
        result = (typee, -1, -1)
    elif(typee == 'One_gas_fail' or typee == 'Fix_minimum'): 
        minimum = minimunFixGas_fix_oneGasFail(cm)
        result = (typee, minimum, minimum)
    elif(typee == 'uncategorized'): 
        result = minimunFixGas_uncatagorized(cm)
    return result

# receive list of tuple (gas,count) to process tx count after the gas point
# return list of gas (x-axis) and count of tx after this point of gas (y-axis)
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
    #divide argument
    (g,gc,s,sc) = (gOH[0][:],gOH[1][:],sOH[0][:],sOH[1][:])  
    sIndex = 0
    rate = []
    print(s)
    print(sc)
    #compare n round when n is number of distinct amount of gas
    for i in range(len(g)):
        try:
            while(g[i] > s[sIndex]):
                sIndex += 1
            #rate is [success/(success+out_of_gas)] when success has gas equal or more than out_of_gas's gas
            rate.append(round((sc[sIndex]/(gc[i]+sc[sIndex]))*100,2))
            #print(g[i],gc[i],'\t',s[sIndex],sc[sIndex])
        except:
            rate.append(0.00)
        
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
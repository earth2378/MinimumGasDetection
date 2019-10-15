import matplotlib.pyplot as plt
import csv,time,ast,sys,os
from termcolor import colored

# read a line from csv in format (contract, method, list of txStatus)
# then add to file named 'contract_method' which store error and gas cost
def splitTxStatToCsv():
    csv.field_size_limit(100000000)
    csv_file = open('contractMethodTxStatus_Filter.csv', 'r')
    csv_reader = csv.reader(csv_file, delimiter=',')
    start_time = time.time()
    c = 0
    for row in csv_reader:
        if(c%100 == 0):
            print(c,time.time()-start_time)
        dst_file = 'cm\\'+ row[0] + "_"+ row[1] + '.csv'
        csv_write = open(dst_file,'w+',newline = '')
        csv_writer = csv.writer(csv_write, delimiter=',')
        txList = ast.literal_eval(row[2])
        list(map(lambda tx : csv_writer.writerow(tx), txList))    
        csv_write.close()
        c += 1

    print(time.time()-start_time)
    csv_file.close()


def readFile(filename):
    csv.field_size_limit(100000000)
    csv_file = open(filename, 'r')
    csv_reader = csv.reader(csv_file, delimiter=',')

    data = dict()
    for row in csv_reader:
        data[(row[0],row[1])] = ast.literal_eval(row[2])
    csv_file.close()
    return data

def createDirectory(dst):
    try:# Create target Directory
        os.mkdir(dst)
    except FileExistsError:
        pass

def filterOogRate(data,percentage):
    delList = []
    for cm in data:
        g,s,t = 0,0,0
        for tx in data[cm]:
            if(tx[0] == 'G'): g += tx[3]
            elif(tx[0] == 'S'): s += tx[3]
            t += tx[3]
        if(g/t*100 < percentage): delList.append(cm)
    for cm in delList: del data[cm]
    return data
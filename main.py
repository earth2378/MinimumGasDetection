import graph as g
import util as util
import catagorize as cat
import time, csv
import minimumGas as mg

start = time.time()
data = util.readFile('cmStatus_src\\result\\contractMethodTxStatusRange_Filter.csv')
#data = util.filterOogRate(data,30)

print("Data Loaded")

dst = 'cmPic2'
util.createDirectory(dst)
dst += '\\Step'
util.createDirectory(dst)
util.createDirectory(dst+'\\byMethod')
util.createDirectory(dst+'\\byType')

csv_write = open('cmPic2\\minimumGas.csv','w+',newline = '')
csv_writer = csv.writer(csv_write, delimiter=',')
#csv_writer.writerow(['No', 'Contract', 'Method', 'Type', 'Minimum Gas', 'Recommend Gas'])

index = 0
for cm in data:
    _ = g.plotAll(cm,data[cm],index,dst+'\\')
    result = mg.calMinimumGas(cm,data[cm])
    #csv_writer.writerow([index, cm[0], cm[1], result[1], result[0], ])
    index += 1
    if(index%20 == 0): 
        print(index, time.time()-start)

print("Done", time.time()-start)
csv_write.close()
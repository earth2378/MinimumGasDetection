import graph as g
import util as util
import catagorize as cat
import time

start = time.time()
data = util.readFile('cmStatus_src\\result\\contractMethodTxStatusRange_Filter.csv')
data = util.filterOogRate(data,30)

print("Data Loaded")

util.createDirectory('cmPic3')
util.createDirectory('cmPic3\\Step')

index = 0
for cm in data:
    _ = g.plotAll(cm,data,index,'cmPic3\\Step\\')
    index += 1
    if(index%20 == 0): 
        print(index, time.time()-start)

print("Done", time.time()-start)

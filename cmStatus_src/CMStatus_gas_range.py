#Process contractMethodTxStatus
import csv,time,ast,sys
import multiprocessing as mp

def init(queue):
    global idx
    idx = queue.get()
    
def f(x):
    global idx
    process = mp.current_process()
    time.sleep(1)
    return (idx, process.pid, x * x)

def compressWithRange(row):
    oldStatus = ''
    data = []
    #for each TxStatus in method
    for item in ast.literal_eval(row[2]):
        if(oldStatus == item[0]):
            data[-1][2] = item[1]
            data[-1][3] += 1
        else:
            data.append([item[0],item[1],item[1],1])
        oldStatus = item[0]
    csv_write = open('result\\contractMethodTxStatusRange.csv','a',newline = '')
    csv_writer = csv.writer(csv_write, delimiter=',')
    csv_writer.writerow([row[0],row[1],data])
    print('finish',row[0],row[1])
    csv_write.close()
    
##########################################################################################################################


if __name__ == '__main__':
    start_time = time.time()
    ids = [i for i in range(mp.cpu_count())]
    manager = mp.Manager()
    idQueue = manager.Queue()
    count = manager.Value('i', 0)
    for i in ids:
        idQueue.put(i)
        
    #Load data source and run each
    csv.field_size_limit(100000000)
    csv_file = open('result\\contractMethodTxStatus.csv', 'r')
    csv_reader = csv.reader(csv_file, delimiter=',')

    pool = mp.Pool(mp.cpu_count(), init,  (idQueue,))
    results = pool.map(compressWithRange, [row for row in csv_reader])
    pool.close()

    csv_file.close()

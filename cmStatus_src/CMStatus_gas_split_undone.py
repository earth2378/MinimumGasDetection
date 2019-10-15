import csv,time,ast,sys,os
import multiprocessing as mp

def splitTxStatToCsv(row):
    start_time = time.time()
    c = 0
    for item in row:
        if(c%1000 == 0):
            print(c,time.time()-start_time)
        if(sys.platform == 'linux'): dst_file = 'cmt/'+ item[0] + "_"+ item[1] + '.csv'
        if(sys.platform == 'win32'): dst_file = 'cmt\\'+ item[0] + "_"+ item[1] + '.csv'
        csv_write = open(dst_file,'w+',newline = '')
        csv_writer = csv.writer(csv_write, delimiter=',')
        txList = ast.literal_eval(item[2])
        list(map(lambda tx : csv_writer.writerow(tx), txList))    
        csv_write.close()
        c += 1

    print(time.time()-start_time)
    csv_file.close()

def init(queue):
    global idx
    idx = queue.get()
    
def f(x):
    global idx
    process = mp.current_process()
    time.sleep(1)
    return (idx, process.pid, x * x)

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
    csv_file = open('contractMethodTxStatus_timestamp.csv', 'r')
    csv_reader = csv.reader(csv_file, delimiter=',')

    pool = mp.Pool(mp.cpu_count(), init,  (idQueue,))
    results = pool.map(splitTxStatToCsv, [row for row in csv_reader])
    pool.close()

    csv_file.close()
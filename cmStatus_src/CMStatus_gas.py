import csv,time,ast,os
from google.cloud import bigquery

client = bigquery.Client()
start_time = time.time()
query_job = client.query("""
SELECT * FROM `ethereum-dataset.EthFailureTx_Result.tx_status`
ORDER BY to_address, method, gas, error
""")
print('query finish')
#results_input = query_job.to_dataframe().values.tolist()
print('Total time: ',time.time()-start_time)
errors = {
    'Out of gas' : 'G',
    'Reverted' : 'R',
    'Bad instruction' : 'I',
    'Bad jump destination' : 'J',
    'Stack underflow' : 'U',
    'Stack Overflow' : 'O',
    'Out of stack' : 'T'
}
cmTxStatus = dict()
count = 0
for row in query_job:
    if(count%100000 == 0):
        print(count, 'Total time: ', time.time()-start_time)
    count += 1
    (to_address, method, gas, receipt_status, error) = row
    cm = (to_address, method)
    if(cm not in cmTxStatus):
        cmTxStatus[cm] = []
    if(error is None):
        cmTxStatus[cm].append(('S',gas))
    else:
        cmTxStatus[cm].append((errors[error],gas))
        
csv_write = open('result\\contractMethodTxStatus.csv','w+',newline = '')
csv_writer = csv.writer(csv_write, delimiter=',')
for cm in cmTxStatus:
    csv_writer.writerow([cm[0],cm[1],cmTxStatus[cm]])
csv_write.close()
print('Total time: ',time.time()-start_time)
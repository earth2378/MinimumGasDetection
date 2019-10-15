import csv
csv.field_size_limit(100000000)
csv_file = open('contractMethodTxStatus_timestamp.csv', 'r')
csv_reader = csv.reader(csv_file, delimiter=',')

csv_write = open('cm\\CMSample.csv','w+',newline = '')
csv_writer = csv.writer(csv_write, delimiter=',')
count = 0
for row in csv_reader:
    if(count == 10  0): break
    csv_writer.writerow(row)
    count += 1
print('done')
csv_file.close()
csv_write.close()
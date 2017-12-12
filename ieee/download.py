import MySQLdb
import csv

db = MySQLdb.connect(host='202.120.36.29', port=3306, user='data',
    passwd='data', db='acemap-xyue1', charset='utf8')
cursor = db.cursor()

cursor.execute('select PaperID, Title, Abstract, Catagory from IeeeAfter2014')
with open('data/IeeeAfter2014.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['PaperID', 'Title', 'Abstract', 'Category'])
    for paperId, title, abstract, category in cursor:
        writer.writerow([paperId, title, abstract, category])

cursor.execute('select * from IeeeAfter2014Reference')
with open('data/IeeeAfter2014Reference.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['CitingPaperID', 'CitedPaperID'])
    for citingPaperId, citedPaperId in cursor:
        writer.writerow([citingPaperId, citedPaperId])
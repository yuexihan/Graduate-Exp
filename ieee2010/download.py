import MySQLdb
import csv

db = MySQLdb.connect(host='202.120.36.29', port=3306, user='data',
    passwd='data', db='acemap-xyue1', charset='utf8')
cursor = db.cursor()

cursor.execute('select PaperID, Title, Abstract, Catagory from IeeeAfter2010')
with open('data/IeeeAfter2010.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['PaperID', 'Title', 'Abstract', 'Category'])
    for paperId, title, abstract, category in cursor:
        assert title
        assert category
        if abstract is None:
            abstract = ''
        writer.writerow([paperId, title.encode('utf-8'), abstract.encode('utf-8'), category])

cursor.execute('select * from IeeeAfter2010Reference')
with open('data/IeeeAfter2010Reference.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['CitingPaperID', 'CitedPaperID'])
    for citingPaperId, citedPaperId in cursor:
        writer.writerow([citingPaperId, citedPaperId])

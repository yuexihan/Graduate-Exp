# coding=utf-8

import csv
import json
import re
import nltk

paperIdToIndex = {}
with open('data/ieee_words', 'wb') as f_out_1:
    with open('data/ieee_category', 'wb') as f_out_2:
        with open('data/IeeeAfter2014', 'rb') as f_in:
            reader = csv.reader(f_in)
            reader.next()
            for i, row in enumerate(reader):
                (paperId, title, abstract, category) = row
                text = re.sub(r'[\r\n]+', ' ', (title + ' ' + abstract).decode('utf-8'))
                words = ' '.join(nltk.word_tokenize(text))
                f_out_1.write((words + '\n').encode('utf-8'))
                f_out_2.write(category + '\n')
                paperIdToIndex[paperId] = i

with open('data/ieee_reference', 'wb') as f_out:
    writer = csv.writer(f_out)
    writer.writerow(['citing_index', 'cited_index'])
    with open('data/IeeeAfter2014Reference.csv') as f_in:
        reader = csv.reader(f_in)
        reader.next()
        for citing_paper_id, cited_paper_id in reader:
            assert citing_paper_id in paperIdToIndex
            assert cited_paper_id in paperIdToIndex
            citing_index = paperIdToIndex[citing_paper_id]
            cited_index = paperIdToIndex[cited_paper_id]
            writer.writerow([citing_index, cited_index])

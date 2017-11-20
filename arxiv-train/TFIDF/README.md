Count.py -> wordCount.json
==========================
We choose words which appear more than 4 times. While the total terms are 297,120, only 103,453 appear more than 4 times.
All words in arxiv are storied in "wordCount.json" as a dictionary. Keys are words and values are their count. The script to calculate it is "Count.py".
The words that appear more 4 times are stored in "wordCountMoreThanFour.json".

idf.py -> wordIDF.json
======================
We only calculate the idf of words in "wordCountMoreThanFour.json".

tfidf.py -> arxivTFIDF.txt
==========================
Then documents' tfidf value are calculated.

pretrained.py -> pretrained.json
================================
The pre-trained word embedding contains 3,000,000 words. But only contains 44,367 of our words. The pre-trained word comes from googlenews-vectors-negative300.bin.gz.
Stored as dict, word: vector. Each vector has 300 dimensions.

arxivVector.py -> arxivVector.txt
=================================
We average word vectors using tfidf information to get document vectors.

arxivVectorOneHot.py -> arxiveVectorOneHot.txt
==============================================
One-hot encoding the category information with position as below: 
['Quantitative Finance', 'Quantitative Biology', 'Statistics', 'Computer Science', 'Mathematics', 'Physics']

statistic.py
============
Each category has number of papers:
[7162, 20979, 20543, 121817, 270501, 861588]

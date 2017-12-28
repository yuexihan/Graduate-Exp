\begin{table}[!htb]
\centering
\bicaption[tab:ieee:compare]{量化比较各算法对IEEE可视化效果}{化比较各算法对IEEE可视化效果}{Table}{Quantitative Comparison of Visualization Results of IEEE}
\begin{tabular}{l@{\quad}c{\quad}c{\quad}r}
\toprule
算法 & 大类聚合度 & 引用聚合度 & 小类聚合度  \\
\midrule
2014-CBCP & 0.319953324036 & 1.70465210202 & 0.510488488488 \\
2010-CBCP & 0.274775147923 & 1.49495038468 & 0.490759683715 \\
CBCP-2steps & 0.241419129346 & 1.26273371333 & 0.422242017816 \\
Paragraph Vector & 0.36921612896 & 1.20790526058 & 0.522282053848 \\
IDF加权预训练词向量 & 0.471673590562 & 1.46190070546 & 0.527214493044 \\
平均预训练词向量 & 0.465372203036 & 1.4469182001 & 0.530060054049 \\
2014-Paperscape & 0.187947798687 & 61.8307968727 & 0.38457866293 \\
2010-Paperscape & 0.249974951324 & 25.7069420183 & 0.41380242218 \\
DeepWalk & 0.0287890414931 & 1.11461124212 & 0.335841673339 \\
\bottomrule
\end{tabular}
\end{table}

# ieee-2014-predict-cite
/home/xyue1/code/Graduate-Exp/ieee/save/ieee_category.txt
/home/xyue1/code/Graduate-Exp/ieee/data/ieee_vectors.txt
/home/xyue1/code/Graduate-Exp/ieee/data/ieee_reference.csv
between_mean => 0.595039038211
between_variance => 0.00807158509097
within_mean => 1.85976826465
within_variance => 0.218262739211
ref_mean => 1.58693401855
ref_variance => 0.256731426777
noref_mean => 2.70517041049
noref_variance => 0.287446845927
precisions => 0.510488488488
precision => 0.519801801802

# ieee-2010-predict-cite
/home/xyue1/code/Graduate-Exp/ieee2010/save/ieee_category.txt
/home/xyue1/code/Graduate-Exp/ieee2010/data/ieee_vectors.txt
/home/xyue1/code/Graduate-Exp/ieee2010/data/ieee_reference.csv
between_mean => 0.577692146314
between_variance => 0.00849164728993
within_mean => 2.10241774295
within_variance => 0.358495053843
ref_mean => 2.04385387703
ref_variance => 0.382559691879
noref_mean => 3.05546013969
noref_variance => 0.459877267688
precisions => 0.490759683715
precision => 0.499955960364

# ieee-2010-order2
/home/xyue1/code/Graduate-Exp/ieee2010order2/save/ieee_category.txt
/home/xyue1/code/Graduate-Exp/ieee2010order2/data/ieee_vectors.txt
/home/xyue1/code/Graduate-Exp/ieee2010order2/data/ieee_reference.csv
between_mean => 0.5686924198
between_variance => 0.010801377392
within_mean => 2.35562285947
within_variance => 1.26558652399
ref_mean => 2.75024289148
ref_variance => 1.57473124084
noref_mean => 3.47282441891
noref_variance => 1.79668467334
precisions => 0.422242017816
precision => 0.426121509358

# ieee-2010-s2v
/home/xyue1/code/Graduate-Exp/ieee2010/save/ieee_category.txt
/home/xyue1/code/Graduate-Exp/ieee2010/sentence2vec/ieee_vector.txt
/home/xyue1/code/Graduate-Exp/ieee2010/data/ieee_reference.csv
between_mean => 0.992473466767
between_variance => 0.0609975887489
within_mean => 2.68805555587
within_variance => 1.09531714374
ref_mean => 3.33254026635
ref_variance => 0.767483832785
noref_mean => 4.02539291882
noref_variance => 1.16794677431
precisions => 0.522282053848
precision => 0.533165849264

# ieee-2010-tfidf
/home/xyue1/code/Graduate-Exp/ieee2010/tfidf/save/ieee_category.txt
/home/xyue1/code/Graduate-Exp/ieee2010/tfidf/ieeeVectorAvg.txt
/home/xyue1/code/Graduate-Exp/ieee2010/data/ieee_reference.csv
between_mean => 0.294280751323
between_variance => 0.0107104691737
within_mean => 0.62390762852
within_variance => 0.0284272408275
ref_mean => 0.63396106693
ref_variance => 0.0236729145802
noref_mean => 0.926788130976
noref_variance => 0.0445503242235
precisions => 0.527214493044
precision => 0.533301971774

# ieee-2010-average
/home/xyue1/code/Graduate-Exp/ieee2010/average/save/ieee_category.txt
/home/xyue1/code/Graduate-Exp/ieee2010/average/ieeeVectorAvg.txt
/home/xyue1/code/Graduate-Exp/ieee2010/data/ieee_reference.csv
between_mean => 0.18765553703
between_variance => 0.00381338019628
within_mean => 0.403237528597
within_variance => 0.00920542894798
ref_mean => 0.412531622058
ref_variance => 0.00939839233391
noref_mean => 0.596899512074
noref_variance => 0.0146369023367
precisions => 0.530060054049
precision => 0.537613852468

# ieee-2014-nbody
/home/xyue1/code/Graduate-Exp/ieee/nbody/ieee_label_nbody.txt
/home/xyue1/code/Graduate-Exp/ieee/nbody/ieee_vector_nbody.txt
/home/xyue1/code/Graduate-Exp/ieee/nbody/ieee_reference_nbody.csv
between_mean => 3942.10286775
between_variance => 5548574.32596
within_mean => 20974.4561803
within_variance => 160735139.993
ref_mean => 446.912497133
ref_variance => 670360.910638
noref_mean => 27632.9558301
noref_variance => 452616472.209
precisions => 0.38457866293
precision => 0.392081665332

# ieee-2010-nbody
/home/xyue1/code/Graduate-Exp/ieee2010/nbody/ieee_label_nbody.txt
/home/xyue1/code/Graduate-Exp/ieee2010/nbody/ieee_vector_nbody.txt
/home/xyue1/code/Graduate-Exp/ieee2010/nbody/ieee_reference_nbody.csv
between_mean => 7913.76764405
between_variance => 16747480.0611
within_mean => 31658.2425645
within_variance => 155192167.204
ref_mean => 1626.69782969
ref_variance => 4362069.23052
noref_mean => 41817.4267892
noref_variance => 619687791.147
precisions => 0.41380242218
precision => 0.421317185466

# ieee-2014-deepwalk
/home/xyue1/code/Graduate-Exp/ieee-deepwalk/sentence2vec/ieee_label_2014_nbody.txt
/home/xyue1/code/Graduate-Exp/ieee-deepwalk/sentence2vec/ieee_vector_2014_nbody.txt
/home/xyue1/code/Graduate-Exp/ieee-deepwalk/sentence2vec/ieee_reference_2014_nbody.csv
between_mean => 0.0718226195782
between_variance => 0.0028155352373
within_mean => 2.49479023452
within_variance => 0.11572039717
ref_mean => 3.1752668134
ref_variance => 1.25051038126
noref_mean => 3.53918808695
noref_variance => 0.158068837588
precisions => 0.335841673339
precision => 0.340798638912

# 小类
/home/xyue1/code/Graduate-Exp/arxiv-fasttext/save/arxiv_label.txt
# 大类
/home/xyue1/code/Graduate-Exp/arxiv-fasttext/save/arxiv_main_category.txt
1216315

# arxiv-fasttext
/home/xyue1/code/Graduate-Exp/arxiv-fasttext/data/arxiv_fasttext_vector.txt
--metric label
between_mean => 0.581469652394
between_variance => 0.0132261255021
within_mean => 0.395313553712
within_variance => 0.0124132436452
--metric category
between_mean => 0.429289546044
between_variance => 0.000513516474755
within_mean => 0.526815820122
within_variance => 0.01755870517
--knn label
precision => 0.54646987709
--knn category
precision => 0.926632989897


# arxiv-s2v
/home/xyue1/code/Graduate-Exp/sentence2vec/arxivSentenceVec.txt
--metric label
between_mean => 1.64983890369
between_variance => 0.139531705023
within_mean => 2.44744404462
within_variance => 0.93631322048
--metric category
between_mean => 1.34344929707
between_variance => 0.0111115832664
within_mean => 2.59187301383
within_variance => 1.16349519473
--knn label
precision => 0.261518234939
--knn category
precision => 0.841989596879

# arxiv-pre-idf
/home/xyue1/code/Graduate-Exp/arxiv-train/TFIDF/arxivVectorTFIDF.txt
--metric label
between_mean => 0.299191108143
between_variance => 0.0103339044697
within_mean => 0.53951949366
within_variance => 0.0210313274738
--metric category
between_mean => 0.274077540015
between_variance => 0.00206419810541
within_mean => 0.566290470425
within_variance => 0.0214378797711
--knn label
precision => 0.18868224864
--knn category
precision => 0.77244573372

# arxiv-pre-average
/home/xyue1/code/Graduate-Exp/arxiv-train/TFIDF/data/arxivVectorAvg.txt
--metric label
between_mean => 0.215930903186
between_variance => 0.00473669390176
within_mean => 0.379384491817
within_variance => 0.011779770079
--metric category
between_mean => 0.203190351456
between_variance => 0.000353263667987
within_mean => 0.398337638778
within_variance => 0.0120123780819
--knn label
precision => 0.183499899254
--knn category
precision => 0.772907872362

# arxiv-self-idf
/home/xyue1/code/Graduate-Exp/sentence2vec/arxivVectorTFIDF.txt
--metric label
between_mean => 0.45582420322
between_variance => 0.0132481254143
within_mean => 0.450608258832
within_variance => 0.0142045220176
--metric category
between_mean => 0.385183340018
between_variance => 0.0007800482056
within_mean => 0.52208874838
within_variance => 0.0163109695919
--knn label
precision => 0.323377997179
--knn category
precision => 0.866973091928

# arxiv-self-average
/home/xyue1/code/Graduate-Exp/sentence2vec/arxivVectorAvg.txt
--metric label
between_mean => 0.259026361344
between_variance => 0.00475636160661
within_mean => 0.285937708858
within_variance => 0.0076318536152
--metric category
between_mean => 0.226733384643
between_variance => 0.000445128834976
within_mean => 0.322005069719
within_variance => 0.00818448206227
--knn label
precision => 0.293077775539
--knn category
precision => 0.856692007602

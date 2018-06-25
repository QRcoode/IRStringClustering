#!/usr/bin/python
import csv
import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
true_k = 196
MERGED_FILE = 'files/merged_data.csv'
CLUSTERS_OUT_FILE = 'files/clusters_v2.csv'


def loadDataset():
    f = open('clusters_only_full.csv','r', encoding='utf-8')
    dataset = []
    for line in f.readlines():
        dataset.append(line)
    f.close()
    return dataset

def transform(dataset,n_features=1000):
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=n_features, min_df=2,use_idf=True)
    X = vectorizer.fit_transform(dataset)
    return X,vectorizer

def train(X,vectorizer,true_k=10,showLable = False):
    km = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1,
                    verbose=False)
    km.fit(X)
    return km.inertia_ 

def test():
    dataset = loadDataset()    
    print("%d documents" % len(dataset))
    X,vectorizer = transform(dataset,n_features=500)
    true_ks = []
    scores = []
    for i in range(3,200,1):        
        score = train(X,vectorizer,true_k=i)/len(dataset)
        #print (i,score)
        true_ks.append(i)
        scores.append(score)
    plt.figure(figsize=(8,4))
    plt.plot(true_ks,scores,label="error",color="red",linewidth=1)
    plt.xlabel("n_features")
    plt.ylabel("error")
    plt.legend()
    plt.show()
#use test() to find out the best number of k


# show keywords of each cluster
'''
print ('Cluster distribution:')
print (dict([(i, result.count(i)) for i in result]))
print ('------------')
print("Top terms per cluster:")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
#print (vectorizer.get_stop_words())
for i in range(true_k):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
    print()
'''

def work():
	print("Configured clusters. Reading review file...") # Console status messages

	with open(MERGED_FILE, "r") as f:
		reviewsAndIssues = f.readlines()

	reviewsAndIssues = [x.strip('\n') for x in reviewsAndIssues]
	reviewsNoSpace = []
	a = 0

	while a < len(reviewsAndIssues): 
		if reviewsAndIssues[a] != '':
			reviewsNoSpace.append(reviewsAndIssues[a])
		a += 1

	print("Assigning clusters...") # Console status messages
	with open(CLUSTERS_OUT_FILE, "w", encoding='utf-8') as f:
		writer = csv.writer(f)

		for x in range(len(reviewsNoSpace)):
			predictLine = [reviewsNoSpace[x]]
			Y = vectorizer.transform(predictLine)
			prediction = km.predict(Y)
			print(prediction)
			if Y.count_nonzero() > 2: # arbitrary number
				writer.writerow((reviewsNoSpace[x], prediction[0], '_')) # Underscore to provide blank for label column
				# Review is not put into a cluster if it doesn't match any issue

	print("Complete.") # Console status messages
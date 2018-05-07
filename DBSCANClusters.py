from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import csv
import os.path
import sys

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler



'''
This code is responsible for organising the data gathered using the google-play scraper and the GitHub Issues scraper 
into clusters. Ensure that you have used the web scrapers, 'githubIssues.py' and 'googlePlayReviews.js', or other
web scrapers, and that you have transferred the appropriate files to the same directory as 'kmeansClusters.py' (this).

@param ISSUES_FILE = File containing all of the issue text retrieved from the GitHub repo.
@param REVIEW_FILE = File containing all of the review text retrieved from the Google Play Store.
@return CLUSTERS_FILE = File containing all of the issues and reviews, with their cluster numbers.
'''

# Change these names if desired
ISSUES_FILE = "./files/vectors.csv"

print("I am working....")
with open(ISSUES_FILE) as f:
	content = f.readlines()
	

content = [x.strip("',\n") for x in content]

fullLines = []
for x in content:
	xArray = x.split(',')
	xArray = [float(y) for y in xArray]
	fullLines.append(xArray)

#print(fullLines)
labelSet = set()

X = StandardScaler().fit_transform(fullLines)
db = DBSCAN(eps=1.9, min_samples=2).fit(fullLines)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# labless = []
for l in labels:
	labelSet.add(l)
	
print(len(labelSet))


# with open('./files/merged_issues_reviews.csv','r',encoding='utf-8') as csvinput:
#     with open('./files/DBSCAN_result.csv', 'w',encoding='utf-8') as csvoutput:
#         writer = csv.writer(csvoutput, lineterminator='\n')
#         reader = csv.reader(csvinput)
#         all = []
#         i = 0
#         for row in reader:
#             temp_row = []
#             temp_row.append(row[0])
#             temp_row.append(row[2])
#             temp_row.append(str(labels[i]))
#             all.append(temp_row)
#             i += 1
#         writer.writerows(all)

print("done")
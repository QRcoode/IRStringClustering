from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn import metrics
import csv
import os.path
import sys

import csv
import numpy as np
import matplotlib.pyplot as plt

'''
This code is responsible for organising the data gathered using the google-play scraper and the GitHub Issues scraper 
into clusters. Ensure that you have used the web scrapers, 'githubIssues.py' and 'googlePlayReviews.js', or other
web scrapers, and that you have transferred the appropriate files to the same directory as 'kmeansClusters.py' (this).

@param ISSUES_AND_REVIEW_FILE = File containing all of the issues and reviews text.
@return CLUSTERS_FILE = File containing all of the issues and reviews, with their cluster numbers.
'''

# Change these names if desired
ISSUES_AND_REVIEW_FILE = "./files/merged.csv"
CLUSTERS_FILE = "./files/clusters_v2.csv"

with open(ISSUES_AND_REVIEW_FILE, "r") as f:
    content = f.readlines()

content = [x.strip('\n') for x in content]
true_k = 0
line = ''
fullLines = []
issueLabels = []

print("Reading issue file...") # Console status messages
for element in content:
    if len(element) > 1: #ignores any blank fields in the csv file, including old '/n' elements
        if element[len(element) - 1] == '+': #checks if labels exist for this row
            labelSeparator = element.rfind(',') #will need revision if one or more labels contain a comma

            if labelSeparator != -1: #does not run if there are labels, but no issue text
                issueLabels.append(element[labelSeparator+1:])
                true_k += 1
                line += element[:labelSeparator]
                fullLines.append(line)
                line = ''

        else: #if the text of the issue somehow made it to multiple rows
            line += element + ' ' #this line builds on the issue text if it is split across multiple rows


# This block of code sets up the clusters for the KMeans algorithm
vectorizer = TfidfVectorizer(stop_words='english') # Here we are using stopwords to preprocess the issue text
X = vectorizer.fit_transform(fullLines)
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)


print("Configured clusters. Reading review file...") # Console status messages

with open(REVIEW_FILE, "r") as f:
    reviews = f.readlines()

reviews = [x.strip('\n') for x in reviews]
reviewsNoSpace = []
a = 0

while a < len(reviews): #ensures that no random blank reviews make it into the clusters
    if reviews[a] != '':
        reviewsNoSpace.append(reviews[a])
    a += 1

print("Assigning clusters...") # Console status messages
with open(CLUSTERS_FILE, "w", encoding='utf-8') as f:
    writer = csv.writer(f)

    for x in range (len(fullLines)):
        predictLine = [fullLines[x]]
        Y = vectorizer.transform(predictLine)
        prediction = model.predict(Y)
        writer.writerow((fullLines[x], prediction[0], issueLabels[x]))

print("Complete.") # Console status messages

#===============================================================
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
        true_ks.append(i)
        scores.append(score)
    plt.figure(figsize=(8,4))
    plt.plot(true_ks,scores,label="error",color="red",linewidth=1)
    plt.xlabel("n_features")
    plt.ylabel("error")
    plt.legend()
    plt.show()
#use test() to find out the best number of k
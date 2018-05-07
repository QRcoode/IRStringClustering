from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn import metrics
import csv
import os.path
import sys

'''
This code is responsible for organising the data gathered using the google-play scraper and the GitHub Issues scraper 
into clusters. Ensure that you have used the web scrapers, 'githubIssues.py' and 'googlePlayReviews.js', or other
web scrapers, and that you have transferred the appropriate files to the same directory as 'kmeansClusters.py' (this).

@param ISSUES_FILE = File containing all of the issue text retrieved from the GitHub repo.
@param REVIEW_FILE = File containing all of the review text retrieved from the Google Play Store.
@return CLUSTERS_FILE = File containing all of the issues and reviews, with their cluster numbers.
'''

# Change these names if desired
ISSUES_FILE = "./files/issues.csv"
REVIEW_FILE = "./files/reviews.txt"
CLUSTERS_FILE = "./files/clusters.csv"

def displayClusters(): # Call this function if you would like to see the top words of each cluster
    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        print("Cluster %d:" % i),
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind]),

if os.path.exists(CLUSTERS_FILE): # Ensurers that we are not overwriting any files
    print("Please ensure that the file '" + CLUSTERS_FILE + "' does not exist, and try again.")
    sys.exit()

with open(ISSUES_FILE, "r") as f:
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

print(true_k,"----")
# This block of code sets up the clusters for the KMeans algorithm
vectorizer = TfidfVectorizer(stop_words='english') # Here we are using stopwords to preprocess the issue text
X = vectorizer.fit_transform(fullLines)
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

#y_pred = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1).fit_predict(X)
#print('the fullLines')
#metrics.calinski_harabaz_score(fullLines, y_pred) 


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
        print(prediction,'-')
        # No need to check if issue fits, as issues created the clusters
        writer.writerow((fullLines[x], prediction[0], issueLabels[x]))

    for x in range(len(reviewsNoSpace)):
        predictLine = [reviewsNoSpace[x]]
        Y = vectorizer.transform(predictLine)
        prediction = model.predict(Y)
        print(prediction)
        if Y.count_nonzero() > 2: # arbitrary number
            writer.writerow((reviewsNoSpace[x], prediction[0], '_')) # Underscore to provide blank for label column
            # Review is not put into a cluster if it doesn't match any issue

print("Complete.") # Console status messages
# IRStringClustering
This project is to find the overlay between reviews and issues of an android APP from google play store and github issues list

### Step 1
To fatch the reviews from google play store, please use googlePlayReviews.js under directory "google-play-scraper"
````
cd path\google-play-scraper
node googlePlayReviews
````
NOTICE: If fatch the reviews data too many times, google might block your IP temporarily

### Step 2
To fatch the issues from github, please use githubIssues.py
````
cd path
python githubIssues.py
````

### K-means clustring method I
````
cd path
python kmeansClusters.py
````

### K-means clustring method II
````
cd path
python kmeansClusters_v2.py
````

### Word2vec + DBSCAN
````
python csv2Arff.py
````
The generated arff files are in "\Wekastring\files".

use Java to run "Wekastring\src\weka\String2Vector.java"
````
python DBSCANClusters.py
````

All the CSV files are included in "files" folder
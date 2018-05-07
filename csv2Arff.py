#!/usr/bin/python

import sys, getopt
import csv, sys, os

# Store input and output file names
ifile='./files/merged_issues_reviews.csv'
ofile='./files/merged_issues_reviews.arff'

file = open(ifile,encoding='utf-8')
reader = csv.reader(file)

fileOut = open(ofile,"w",encoding='utf-8')

fileOut.write("@relation text_files_in_/research/mlstemming/datasets/reuters/top10categories/arffFiles-weka.filters.unsupervised.instance.Randomize-S42-weka.filters.supervised.instance.Resample-B0.0-S1-Z1.0 \n")
fileOut.write("@attribute contents string \n\n")
fileOut.write("@data\n\n")

for line in reader:
	tempStr = line[0].replace("##", "").replace("'", "")
	fileOut.write("' "+tempStr +"', \n")

fileOut.close()

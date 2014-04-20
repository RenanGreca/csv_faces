# csv_faces
# Renan Greca, 2014

import csv
from collections import defaultdict

with open('test.csv', 'rb') as csvfile:
    data = csv.reader(csvfile)
    #for row in spamreader:
    #    print ', '.join(row)

    graph = {}

    for row in data:
        # row[17] is the URL of the first image
        if row[17] not in graph:
            graph[row[17]] = []

        # row[18] is the URL of the second image
        if row[18] not in graph:
            graph[row[18]] = []

        # row[6] contains 'same' or 'not_same'
        if row[6] == 'same':
            graph[row[17]].append(row[18])
            graph[row[18]].append(row[17])

    print graph 
    #for node in graph:
    #print '[',node,']'
# csv_faces
# Renan Greca, 2014

import csv
import urllib
import os

# Is it better to use objects? Not sure.
class Node(object):
    def __init__(self, url):
        self._url = url
        self._edges = set()

    @property
    def url(self):
        return self._url
    
    @property
    def edges(self):
        return self._edges
    
    def link(self, other, weight):
        self._edges.add((other, weight))
        other._edges.add((self, weight))

def find_components(graph):
    visited = []
    components = []
    cno = 0
    
    # this goes through the nodes in the graph and adds all connected ones to one component
    for key, node in graph.items():
        ino = 0
        if not os.path.exists("output/"+str(cno)):
            os.makedirs("output/"+str(cno))
        if key not in visited:
            visited.append(key)
            component = [key]
            queue = [key]
            while queue:
                n = graph[queue.pop(0)];
                for (link, weight) in n:
                    if link not in visited: 
                        visited.append(link)
                        if link not in component:
                            component.append(link)
                            urllib.urlretrieve(link, "output/"+str(cno)+"/"+str(ino)+".jpg")
                            ino+=1
                            if link not in queue:
                                queue.append(link)

            components.append(component)
            cno+=1

    return components


with open('a402549.csv', 'rb') as csvfile:
#with open('test.csv', 'rb') as csvfile:
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
        # row[7] is the confidence
        #print row[6], row[7]
        if (row[6] == 'same') and (float(row[7]) == 1.0):
            graph[row[17]].append((row[18],row[7]))
            graph[row[18]].append((row[17],row[7])) 

    #print graph
    print find_components(graph)
    
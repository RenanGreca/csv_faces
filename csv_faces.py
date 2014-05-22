# csv_faces
# Renan Greca, 2014

import csv
import urllib
import os
from PIL import Image
import posixpath
import urlparse

# Is it better to use objects? Not sure.
"""
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
"""

def find_path(self, source, sink, path):
    if source == sink:
        return path
    for edge in self.get_edges(source):
        residual = edge.capacity - self.flow[edge]
        if residual > 0 and edge not in path:
            result = self.find_path( edge.sink, sink, path + [edge]) 
            if result != None:
                return result    
 
def max_flow(self, source, sink):
    path = self.find_path(source, sink, [])
    while path != None:
        residuals = [edge.capacity - self.flow[edge] for edge in path]
        flow = min(residuals)
        for edge in path:
            self.flow[edge] += flow
            self.flow[edge.redge] -= flow
        path = self.find_path(source, sink, [])
    return sum(self.flow[edge] for edge in self.get_edges(source))


def find_components(graph):
    visited = []
    components = []
    cno = 0
    
    # this goes through the nodes in the graph and adds all connected ones to one component
    for key, node in graph.items():
        #print key
        #print xy
        #print node
        ino = 0
        if key not in visited:
            visited.append(key)
            component = [key]
            queue = [key]
            while queue:
                #print queue.pop(0)
                n = graph[queue.pop(0)]
                #print n
                for (link, rect, weight) in n:
                    if (link, rect) not in visited: 
                        visited.append((link, rect))
                        if (link, rect) not in component:
                            component.append((link, rect))
                            if not os.path.exists("output/"+str(cno)):
                                os.makedirs("output/"+str(cno))

                            path = urlparse.urlsplit(link).path
                            # gets just the file name, no directories nor extension
                            filename = posixpath.basename(posixpath.splitext(path)[0])
                            #print filename

                            urllib.urlretrieve(link, "output/"+str(cno)+"/"+filename+".jpg")

                            image = Image.open("output/"+str(cno)+"/"+filename+".jpg")
                            width, height = image.size
                            
                            #print(link[1])
                            x1 = int(width*rect[0]) #left edge
                            x2 = int(width*rect[1]) #right
                            y1 = int(height*rect[2]) #upper
                            y2 = int(height*rect[3]) #lower

                            box = (x1, y1, x2, y2)
                            #print box
                            #print width, height
                            region = image.crop(box)
                            region.save("output/"+str(cno)+"/"+filename+"_"+str(x1)+"_"+str(y1)+"_"+str(x2)+"_"+str(y2)+".jpg", "JPEG")

                            ino+=1
                            if (link, rect) not in queue:
                                queue.append((link, rect))

            components.append(component)
            cno+=1

    return components

with open('a402549.csv', 'rb') as csvfile:
    data = csv.reader(csvfile)
    #for row in spamreader:
    #    print ', '.join(row)

    graph = {}

    for row in data:
        x1_1 = float(row[19]) #left edge
        x2_1 = float(row[21]) #right
        y1_1 = float(row[23]) #upper
        y2_1 = float(row[25]) #lower

        row[17] = row[17].lstrip() #strips leading spaces that show up sometimes
        # row[17] is the URL of the first image
        if (row[17], (x1_1,x2_1,y1_1,y2_1)) not in graph:
            graph[(row[17], (x1_1,x2_1,y1_1,y2_1))] = []


        x1_2 = float(row[20]) #left edge
        x2_2 = float(row[22]) #right
        y1_2 = float(row[24]) #upper
        y2_2 = float(row[26]) #lower

        row[18] = row[18].lstrip() #strips leading spaces that show up sometimes
        # row[18] is the URL of the second image
        if (row[18], (x1_2,x2_2,y1_2,y2_2)) not in graph:
            graph[(row[18], (x1_2,x2_2,y1_2,y2_2))] = []

        # row[6] contains 'same' or 'not_same'
        # row[7] is the confidence
        #print row[6], row[7]
        if (row[6] == 'same') and (float(row[7]) == 1.0):
            #print (row[17], (x1_1,x2_1,y1_1,y2_1)), ' and ', (row[18], (x1_2,x2_2,y1_2,y2_2)), ' are the same face'
            graph[(row[17], (x1_1,x2_1,y1_1,y2_1))].append((row[18], (x1_2,x2_2,y1_2,y2_2), row[7]))
            graph[(row[18], (x1_2,x2_2,y1_2,y2_2))].append((row[17], (x1_1,x2_1,y1_1,y2_1), row[7]))

    #print graph[('http://farm6.static.flickr.com/5047/5263446926_6a22710e0e_b.jpg', (0.322108, 0.828697, 0.155273, 0.493164))]
    print graph
    #find_components(graph)
    
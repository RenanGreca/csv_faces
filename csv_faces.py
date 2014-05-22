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

# find_path and max_flow were mostly copied from Wikipedia
# they are the sample implementation of the Ford-Fulkerson algorithm

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
    visited = [] # stores visited nodes to avoid redundancy
    components = [] # stores the list of components that will be returned
    cno = 0 # increments for each component
    
    # this goes through the nodes in the graph and adds all connected ones to one component
    for key, node in graph.items():
        if key not in visited:
            visited.append(key)
            component = [key]
            queue = [key] # queue of images that will be checked for this component
            while queue:
                n = graph[queue.pop(0)]
                for (img_url, rect, weight) in n:
                    img_key = (img_url, rect)
                    if img_key not in visited:
                        visited.append(img_key)
                        if img_key not in component:
                            component.append(img_key)

                            # this creates directories if necessary
                            if not os.path.exists("output/"+str(cno)):
                                os.makedirs("output/"+str(cno))

                            # gets just the file name, no directories nor extension
                            path = urlparse.urlsplit(img_url).path
                            filename = posixpath.basename(posixpath.splitext(path)[0])

                            # downloads and opens the image file
                            urllib.urlretrieve(img_url, "output/"+str(cno)+"/"+filename+".jpg")
                            image = Image.open("output/"+str(cno)+"/"+filename+".jpg")
                            width, height = image.size
                            
                            # finds the int pixel values for the face rectangle
                            x1 = int(width*rect[0]) #left edge
                            x2 = int(width*rect[1]) #right
                            y1 = int(height*rect[2]) #upper
                            y2 = int(height*rect[3]) #lower

                            # cuts the face rectangle and stores it in a new file
                            box = (x1, y1, x2, y2)
                            region = image.crop(box)
                            region.save("output/"+str(cno)+"/"+filename+"_"+str(x1)+"_"+str(y1)+"_"+str(x2)+"_"+str(y2)+".jpg", "JPEG")

                            if img_key not in queue:
                                queue.append(img_key)

            components.append(component)
            cno+=1

    return components

with open('a402549.csv', 'rb') as csvfile:
    data = csv.reader(csvfile)
    #for row in spamreader:
    #    print ', '.join(row)

    graph = {}

    for row in data:
        img1_url = row[17] # row[17] is the URL of the first image
        img2_url = row[18] # row[18] is the URL of the second image

        x1_1 = float(row[19]) #left edge
        x2_1 = float(row[21]) #right
        y1_1 = float(row[23]) #upper
        y2_1 = float(row[25]) #lower

        img1_url = img1_url.lstrip() #strips leading spaces that show up sometimes
        img1_key = (img1_url, (x1_1,x2_1,y1_1,y2_1)) 
        if img1_key not in graph:
            graph[img1_key] = []


        x1_2 = float(row[20]) #left edge
        x2_2 = float(row[22]) #right
        y1_2 = float(row[24]) #upper
        y2_2 = float(row[26]) #lower

        img2_url = img2_url.lstrip() #strips leading spaces that show up sometimes
        img2_key = (img2_url, (x1_2,x2_2,y1_2,y2_2))
        if img2_key not in graph:
            graph[img2_key] = []

        # row[6] contains 'same' or 'not_same'
        # row[7] is the confidence
        if (row[6] == 'same') and (float(row[7]) == 1.0):
            graph[img1_key].append((img2_key, row[7])) #not sure if we need to store the confidence if we're just getting 1.0
            graph[img2_key].append((img1_key, row[7]))

    print graph
    #components = find_components(graph)
    
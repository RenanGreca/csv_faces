import csv
from PIL import Image
import numpy as np
import urllib
import os
import posixpath
import urlparse

with open('a402549.csv', 'rb') as csvfile:
    data = csv.reader(csvfile)
    if not os.path.exists("output/"):
        os.makedirs("output/")
    for row in data:
        link = row[17]
        path = urlparse.urlsplit(link).path
        filename = posixpath.basename(posixpath.splitext(path)[0])

        if not os.path.exists("output/"+filename+".jpg"):
            urllib.urlretrieve(link, "output/"+filename+".jpg")

            image = Image.open("output/"+filename+".jpg")
            width, height = image.size
            #print row[19]
            
            x1 = int(width*float(row[19])) #left edge
            x2 = int(width*float(row[21])) #right
            y1 = int(height*float(row[23])) #upper
            y2 = int(height*float(row[25])) #lower (I think)

            box = (x1, y1, x2, y2)
            region = image.crop(box)
            region.save("output/"+filename+"_"+str(x1)+"_"+str(y1)+"_"+str(x2)+"_"+str(y2)+".jpg", "JPEG")

            #array = np.array(image)
            #array.shape
            #array[:100,:100,:] # use data from CSV to cut face rectangles

        link = row[18]
        path = urlparse.urlsplit(link).path
        filename = posixpath.basename(posixpath.splitext(path)[0])

        if not os.path.exists("output/"+filename+".jpg"):
            urllib.urlretrieve(link, "output/"+filename+".jpg")

            image = Image.open("output/"+filename+".jpg")
            width, height = image.size
            #print row[19]
            
            x1 = int(width*float(row[20])) #left edge
            x2 = int(width*float(row[22])) #right
            y1 = int(height*float(row[24])) #upper
            y2 = int(height*float(row[26])) #lower (I think)

            box = (x1, y1, x2, y2)
            region = image.crop(box)
            region.save("output/"+filename+"_"+str(x1)+"_"+str(y1)+"_"+str(x2)+"_"+str(y2)+".jpg", "JPEG")




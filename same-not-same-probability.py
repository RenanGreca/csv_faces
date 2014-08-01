import csv
from IPython import embed;

"""
Uses golden data from the gallagher set to compute the probability of humans 
getting an answer wrong (saying two faces are the same when they're not or 
vice-versa)
"""

with open('f402549.csv', 'rb') as csvfile:
    data = csv.reader(csvfile)

    total_same = 0.0
    total_not_same = 0.0
    same_when_not_same = 0.0
    not_same_when_same = 0.0

    rno = 1
    for row in data:
    	# row[2] is TRUE when the data is golden
    	if (row[2] == 'true'):
    		# row[15] is the judge's answer - row[19] is the golden data
    		if (row[19] == 'same'):
    			total_same += 1.0
    			if (row[15] == 'not_same'):
    				not_same_when_same += 1.0
    		else:
    			total_not_same += 1.0
    			if (row[15] == 'same'):
    				same_when_not_same += 1.0
        rno += 1

    print "Number of rows used: ", rno
    print "Total of faces that are the same: ", total_same
    print "Total of faces that are not the same: ", total_not_same
    print "Number of false positives: ", same_when_not_same
    print "Number of false negatives: ", not_same_when_same

    print "p(same | !same) = "+str(same_when_not_same/total_not_same)
    print "p(!same | same) = "+str(not_same_when_same/total_same)
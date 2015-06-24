
#Get elevation (Z coordinate) for a node X,Y from USGS
#"C:\Python26\python.exe" getElevations.py --nodes nodes.csv --nodes_out nodesZ.csv
#Ben Stabler, ben.stabler@rsginc.com, 03/08/15

############################################################

import urllib2, csv
import xml.etree.ElementTree as et
import time, sys

#parameters
file_name= sys.argv[2] #id,x,y
file_name_out = sys.argv[4] #id,x,y,z

#geocode service address
url = 'http://nationalmap.gov/epqs/pqs.php?x=%s&y=%s&units=Feet&output=xml'

#read nodes
nodes = []
with open(file_name, 'rb') as csvfile:
	freader = csv.reader(csvfile, skipinitialspace=True)
	for row in freader:
		nodes.append(row)
	nodes_col_names = nodes.pop(0)

#get zcoord
i = 0
for node in nodes:
  
	id = int(node[0])
	x = float(node[1])
	y = float(node[2])
	
	retries = 0
	while (retries < 5):
		try:
			req = urllib2.Request(url % (x,y))
			response = urllib2.urlopen(req)
			break
		except:
			retries += 1
			time.sleep(30) #wait 30 seconds and try again
		else:
			raise Exception("Server not available")
	
	tree = et.fromstring(response.read())
	elevation = tree[0][1].text
	z = float(elevation)
	node.append(str(z))
	print(str(i) + " " + node[0] + " " + node[1] + " " + node[2] + " " + node[3])
	i=i+1

#write result
fout = open(file_name_out,'wb')
f_writer=csv.writer(fout)
f_writer.writerow(["id","x","y","z"])

for node in nodes:
	f_writer.writerow([node[0],node[1],node[2],node[3]])
fout.close() 

# MapGenerator.py

# This script generate plots of the quotient data for background
# analysis of the LANL groundwater dataset.  

# Scripted by Casey Gierke of Lee Wilson & Associates
# 2/5/2019

# With Notepad++, use F5 then copy this into box
# C:\Python27\python.exe -i "$(FULL_CURRENT_PATH)"
# C:\Users\Casey\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"
# C:\Users\Casey\Anaconda3\envs\Mapping\python.exe -i "$(FULL_CURRENT_PATH)"
# C:\Users\Casivio\Anaconda3\envs\Mapper\python.exe -i "$(FULL_CURRENT_PATH)"

# ----------------------------------------
# IMPORTS
# ----------------------------------------

from mpl_toolkits.basemap import Basemap, pyproj 
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pylab import * 
import os
import glob

# ----------------------------------------
# DEFINE FUNCTIONS
# ----------------------------------------

# Define last position finder
def find_last(s,t):
	last_pos = -1
	while True:
		pos = s.find(t, last_pos +1)
		if pos == -1:
			return last_pos
		last_pos = pos

def drawRect(x1,y1,x,y, color, width):
	poly = Polygon([[x1,y1], [x1+x,y1], [x1+x,y1+y], [x1,y1+y]],facecolor='w',edgecolor=color,linewidth=width)
	plt.gca().add_patch(poly)

# add drawscale method to Basemap class. 
class Basemap2(Basemap):
	def drawscale(self,length, yoffset=None):
		"""draw a simple map scale from x1,y to x2,y in map projection 
		coordinates, label it with actual distance in km""" 
		
		# Define dimensions
		x1,y1,x2,y,extra = 0.03*map.xmax, 0.03*map.xmax, 0.03*map.xmax+length, 0.05*map.xmax, 0.01*map.xmax
		
		# Call rectangle function for bounding box
		drawRect(x1-extra,y1-extra,length+2*extra+1300,y1+2*extra, 'k', 1)
		
		# Get info for scale bar
		yoffset = 0.01*map.ymax
		lon1,lat1 = self(x1,y,inverse=True) 
		lon2,lat2 = self(x2,y,inverse=True) 
		# Convert to map projection units
		gc = pyproj.Geod(a=self.rmajor,b=self.rminor) 
		
		# This gets the distance on a level plane (inv), to get distance on the plane, use sqrt()
		az12,az21,dist = gc.inv(lon1,lat1,lon2,lat2)
		
		# These are the pieces of the scale bar
		map.plot([x1,x2],[y,y],linewidth=1,color='k') 
		# Vertical ticks
		map.plot([x1,x1],[y-yoffset,y+yoffset],linewidth=1,color='k') 
		map.plot([x1+length/6.0,x1+length/6.0],[y-yoffset,y+yoffset],linewidth=1,color='k') 
		map.plot([x1+length/3.0,x1+length/3.0],[y-yoffset,y+yoffset],linewidth=1,color='k') 
		map.plot([x1+2*length/3.0,x1+2*+length/3.0],[y-yoffset,y+yoffset],linewidth=1,color='k') 
		map.plot([x2,x2],[y-yoffset,y+yoffset],linewidth=1,color='k') 
		# Label after converting to miles
		# 0
		text(x1,y-yoffset-0.5*extra,'%d' % (dist*0*0.621371,),
		verticalalignment='top', horizontalalignment='center',fontsize=9, color= 'k', fontweight='normal') 
		# 0.5
		text(x1+length/6.0,y-yoffset-0.5*extra,'%g' % (round(dist/6/1000.*0.621371,1),),
		verticalalignment='top', horizontalalignment='center',fontsize=9, color= 'k', fontweight='normal') 
		# 1
		text(x1+length/3.0,y-yoffset-0.5*extra,'%d' % (dist/3/1000.*0.621371,),
		verticalalignment='top', horizontalalignment='center',fontsize=9, color= 'k', fontweight='normal') 
		# 2
		text(x1+length*2/3.0,y-yoffset-0.5*extra,'%d' % (dist*2/3/1000.*0.621371,),
		verticalalignment='top', horizontalalignment='center',fontsize=9, color= 'k', fontweight='normal') 
		# 3
		text(x1-200+length,y-yoffset-0.5*extra,'%d miles' % (dist/1000.*0.621371,),
		verticalalignment='top', horizontalalignment='left',fontsize=9, color= 'k', fontweight='normal') 

	def drawLegend(self,y1, yoffset=None):
		# Define dimensions
		x1 = 0.03*map.xmax
		extra = 0.01*map.xmax
		
		# Make a list of items
		Items = ['LANL Boundary', 'Quotient <= 1', 'Quotient > 1']
		Markers = ['rectangle', 'lime', 'r']
		markerColor = ['k', 'orangered', 'lime']
		
		# Define height and width
		vertLineSpace = 1000
		vertSpace = vertLineSpace*len(Items)+100
		horSpace = max([len(item) for item in Items])*550
		symbolSpace = 1500
		
		# Call rectangle function for bounding box
		drawRect(x1-extra,y1,horSpace,vertSpace, 'k',1)
		
		# Populate legend
		j = 0
		for item in Items:
			# Write text
			text(x1+symbolSpace,y1+0.75*vertLineSpace+j*vertLineSpace, item,
			verticalalignment='top', horizontalalignment='left',fontsize=11, color= 'k', fontweight='normal') 
			
			# Draw symbols
			if Markers[j] == 'rectangle':
				drawRect(x1+0.25*symbolSpace,y1+0.25*vertLineSpace+j*vertLineSpace,0.5*symbolSpace, 0.5*vertLineSpace, markerColor[j],1.5)
			else:
				map.plot(x1+0.5*symbolSpace,y1+0.5*vertLineSpace+j*vertLineSpace, 
				marker='o', color = Markers[j], markersize=5, markeredgewidth=1)
			j = j + 1

	def northArrow(self):
		# Define dimensions
		x1,y1 = 0.97*map.xmax, 0.03*map.xmax
		x,y,extra = 3000, 4000, 0.01*map.xmax
		inset = 600
		rOut = 800
		rIn = 650
		xy = (x1-inset,y1+inset)
		
		# Make circles
		circleOut = matplotlib.patches.CirclePolygon(xy, radius=rOut, facecolor='none', edgecolor='k', linewidth=2)
		plt.gca().add_patch(circleOut)
		circleIn = matplotlib.patches.CirclePolygon(xy, radius=rIn, facecolor='none', edgecolor='k', linewidth=1)
		plt.gca().add_patch(circleIn)
		
		# Overlay pointer
		poly = Polygon([[x1-inset,(y1+2*rOut)*1.1], [x1+extra*.5,y1-extra], [x1-inset,y1+inset-extra], [x1-2*inset-extra*.5,y1-extra]],facecolor='white',edgecolor='k',linewidth=1)
		plt.gca().add_patch(poly)
		
		# Add text
		text(x1-inset,y1+inset,'N' ,
		verticalalignment='center', horizontalalignment='center', fontname='Times New Roman', fontsize=12, color= 'k', fontweight='heavy') 
	
# ------------------------------------------------------
# INPUTS
# ------------------------------------------------------

# Define path
path = os.path.abspath(os.path.dirname(__file__))
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]

# Define what you will be plotting
Category = 'Maximum'
# Category = 'Average'

# Make a code dictionary
codeIn = open(path+os.sep+'Basemap Mapper'+os.sep+'Python'+os.sep+'CodeDict.txt','r')
codeDict = {}
for line in codeIn:
	Columns = line.split('\t')
	codeDict[Columns[0]] = Columns[1]
codeIn.close()

# Make a label dictionary
labelIn = open(path+os.sep+'Basemap Mapper'+os.sep+'Python'+os.sep+'labelDict.txt','r')
labelDict = {}
for line in labelIn:
	Columns = line.split('\t')
	labelDict[Columns[0]] = [float(Columns[1]), float(Columns[2][:-1])]
labelIn.close()

# # Get list of files to map
# Create array to store names
Files = []
if Category == 'Maximum':
	Q = 'max'
	for file in glob.glob(path+os.sep+'Basemap Mapper'+os.sep+'Data'+os.sep+'GBIR Location Files'+os.sep+'Shapefiles- Maxes'+os.sep+'*.shp'):
		Files.append(file)
else:
	Q = 'ave'
	for file in glob.glob(path+os.sep+'Basemap Mapper'+os.sep+'Data'+os.sep+'GBIR Location Files'+os.sep+'Shapefiles- Aves'+os.sep+'*.shp'):
		Files.append(file)

# # Short circuit for testing
# # Files = [Files[0], Files[41]]
# Files = [Files[-3]]

# Loop through files
# ------------------------------------------------------
for file in Files:

	# Define the bounds of the map area
	LongLeft = -106.4
	LongRight = -106.15
	LatBottom = 35.75
	LatTop = 35.90
	midLat = (LatBottom+LatTop)/2.0
	midLong = (LongLeft+LongRight)/2.0

	# Opent a figure for plotting
	plt.figure(figsize=(10, 8))

	# Create the map object
	map = Basemap2(llcrnrlon= LongLeft,llcrnrlat= LatBottom,urcrnrlon=LongRight,urcrnrlat=LatTop, projection='tmerc', lat_0 = midLat, lon_0 = midLong, epsg=3857)

	# Get imagery
	map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)

	# Read in the shp files
	# ------------------------------------------------------
	
	# # Monitoring areas
	# map.readshapefile(path+os.sep+'Mapping Files'+os.sep+'shp Files'+os.sep+'Monitoring Groups- Lat Long', 'MonitoringGroups', drawbounds = True, color='orangered', linewidth=1)

	# # Pueblo boundary
	# map.readshapefile(path+os.sep+'Mapping Files'+os.sep+'shp Files'+os.sep+'US Tribal Land'+os.sep+'LANL Pueblo Land- LatLong', 'Pueblo Boundary', drawbounds = True, color='orangered', linewidth=2)

	# # Bandelier boundary
	# map.readshapefile(path+os.sep+'Mapping Files'+os.sep+'shp Files'+os.sep+'Bandelier'+os.sep+'BandelierWilderness- LatLong', 'Bandelier', drawbounds = True, color='lime', linewidth=2, zorder=1)

	# LANL boundary
	map.readshapefile(path+os.sep+'Basemap Mapper'+os.sep+'shp Files'+os.sep+'LANL Boundary- LatLong', 'LANL Boundary', drawbounds = True, color='k', linewidth=2)

	# Define parameter from filename
	Parameter = file[find_last(file,os.sep)+1:-4]
	
	# Open data file
	param_info = map.readshapefile(file[:-4], 'Param')

	# Initiate a list to populate
	locationList = []
	# Loop through data file and plot data
	for info, Location in zip(map.Param_info, map.Param):
		# Make info into a list of dictionaries
		locationList.append({'Location': info['Location'], 'x': Location[0], 'y': Location[1], 'Q': info['Q'+Q]})
	
	# Sort list by Q values
	locationList = sorted(locationList, key = lambda i: abs(1-i['Q']), reverse=True)
	
	# Loop through sorted list
	for item in locationList:
		if float(item['Q']) > 1:
			color = 'r'
		else:
			color = 'lime'
		# map.plot(Location[0], Location[1], marker='o', color=color, markersize=(abs(1-float(item['Q'+Q]))*8+5), markeredgewidth=1)
		map.plot(item['x'], item['y'], marker='o', color=color, markersize=(abs(1-float(item['Q']))*8+5), markeredgewidth=1)

		# Determine if label is above or below point for arrows
		if labelDict[item['Location']][1] > 0:
		
			# Label points with Location
			plt.annotate(item['Location'], xy=(item['x'],item['y']), 
			xycoords='data',
			xytext=(item['x']+labelDict[item['Location']][0], item['y']+labelDict[item['Location']][1]), 
			textcoords='data', fontsize = 8, color = 'w', weight='heavy', 
			verticalalignment='bottom', horizontalalignment='center'
			)
			
			# Label points with Data
			plt.annotate(round(item['Q'],2), xy=(item['x'],item['y']), 
			xycoords='data',
			xytext=(item['x']+labelDict[item['Location']][0], item['y']+labelDict[item['Location']][1]), 
			textcoords='data', fontsize = 8, color = 'w', weight='normal', 
			verticalalignment='top', horizontalalignment='center',
			arrowprops=dict(arrowstyle="->", color='w')
			)
		else:
			# Labels below points 
			plt.annotate(item['Location'], xy=(item['x'],item['y']), 
			xycoords='data',
			xytext=(item['x']+labelDict[item['Location']][0], item['y']+labelDict[item['Location']][1]), 
			textcoords='data', fontsize = 8, color = 'w', weight='heavy', 
			verticalalignment='bottom', horizontalalignment='center',
			arrowprops=dict(arrowstyle="->", color='w')
			)
			
			# Label points with Data
			plt.annotate(round(item['Q'],2), xy=(item['x'],item['y']), 
			xycoords='data',
			xytext=(item['x']+labelDict[item['Location']][0], item['y']+labelDict[item['Location']][1]), 
			textcoords='data', fontsize = 8, color = 'w', weight='normal', 
			verticalalignment='top', horizontalalignment='center',
			)

		
	# ------------------------------------------------------
	# ADD MAP ITEMS
	# ------------------------------------------------------

	# Define the length (in meters?)
	length = 5950

	# Add scale bar
	map.drawscale(length) 

	# Add legend
	map.drawLegend(2500)

	# Add north arrow
	map.northArrow()

	# Make a title
	plt.title(Category+' Quotient Values for '+codeDict[Parameter[Parameter.find('-')+2:]][:-1]+' in the '+Parameter[:Parameter.find('-')]+' Aquifer.', fontname='Times New Roman', y=1.08, fontsize=14, color= 'k', fontweight='bold')

	# # Make footnotes
	# text(0.02*map.xmax,-700,'- Data acquired from Intellus (https://www.intellusnm.com/).' ,
			# verticalalignment='center', horizontalalignment='left', fontname='Times New Roman', fontsize=12, color= 'k', fontweight='normal') 
	# text(0.02*map.xmax,-1700,'- Quotients were derived by dividing '+Category.lower()+' measured concentrations by the respective UTL for the \n'+Parameter[:Parameter.find('-')].lower()+' aquifer.' ,
			# verticalalignment='center', horizontalalignment='left', fontname='Times New Roman', fontsize=12, color= 'k', fontweight='normal') 
	# text(0.02*map.xmax,-3000,'- Basemap (ESRI_Imagery_World_2D) Sources: Esri, DigitalGlobe, Earthstar Geographics, CNES/Airbus DS, \nGeoEye, USDA FSA, USGS, Aerogrid, IGN, IGP, and the GIS User Community.' ,
			# verticalalignment='center', horizontalalignment='left', fontname='Times New Roman', fontsize=12, color= 'k', fontweight='normal') 
		
	# Check to make sure directory exists for writing data file
	if not os.path.exists(path+os.sep+'Basemap Mapper'+os.sep+'Mapping'+os.sep+Category+os.sep):
		os.makedirs(path+os.sep+'Basemap Mapper'+os.sep+'Mapping'+os.sep+Category+os.sep)
	
	# Save figure
	plt.savefig(path+os.sep+'Basemap Mapper'+os.sep+'Mapping'+os.sep+Category+os.sep+Parameter+'.png',dpi=500)

	# plt.show()

	plt.close()
	
	
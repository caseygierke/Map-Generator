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
import zipfile

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

# def drawRect(x1,y1,x,y, color, width):
	poly = Polygon([[x1,y1], [x1+x,y1], [x1+x,y1+y], [x1,y1+y]],facecolor='w',edgecolor=color,linewidth=width)
	plt.gca().add_patch(poly)

# # add drawscale method to Basemap class. 
# class Basemap2(Basemap):
	def drawscale(self,length, yoffset=None):
		"""draw a simple map scale from x1,y to x2,y in map projection 
		coordinates, label it with actual distance in miles""" 
		
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

# Unzip the zipped static shp files
for file in glob.glob(path+os.sep+'Static Files'+os.sep+'*.zip'):
	zip_ref = zipfile.ZipFile(file, 'r')
	zip_ref.extractall(path+os.sep+'Static Files'+os.sep)
	zip_ref.close()

# Get the name of the static file
staticFile = glob.glob(path+os.sep+'Static Files'+os.sep+'*.shp')
staticFile = staticFile[0]

# Unzip the zipped dynamic shp files
for file in glob.glob(path+os.sep+'Data'+os.sep+'*.zip'):
	zip_ref = zipfile.ZipFile(file, 'r')
	zip_ref.extractall(path+os.sep+'Data'+os.sep)
	zip_ref.close()

# Create array to store names
Files = []
# Get list of files to map
for file in glob.glob(path+os.sep+'Data'+os.sep+'*.shp'):
	Files.append(file)

# # Short circuit for testing
# # Files = [Files[0], Files[41]]
# Files = [Files[-3]]

# Loop through files
# ------------------------------------------------------
for file in Files:
	
	# Define the bounds of the map area
	LongLeft = -110
	LongRight = -102.5
	LatBottom = 31
	LatTop = 38
	midLat = (LatBottom+LatTop)/2.0
	midLong = (LongLeft+LongRight)/2.0

	# Open a figure for plotting
	plt.figure(figsize=(8, 9))
	
	# Create the map object
	map = Basemap(llcrnrlon= LongLeft,llcrnrlat= LatBottom,urcrnrlon=LongRight,urcrnrlat=LatTop, projection='tmerc', lat_0 = midLat, lon_0 = midLong, epsg=3857)

	# Get imagery
	map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)

	# Read in the static shp files
	map.readshapefile(staticFile[:-4], staticFile[find_last(staticFile,os.sep)+1:-4], drawbounds = True, color='k', linewidth=3)

	# Get the dynamic file name for naming and handling
	fileName = file[find_last(file,os.sep)+1:-4]
	print(fileName)
	# Open data file
	dynamicFile = map.readshapefile(file[:-4], fileName, drawbounds = True, color='w', linewidth=1.5)
		
	# Make a title
	plt.title(fileName, fontname='Times New Roman', y=1.08, fontsize=14, color= 'k', fontweight='bold')
		
	# Check to make sure directory exists for saving figure
	if not os.path.exists(path+os.sep+'Output'+os.sep):
		os.makedirs(path+os.sep+'Output'+os.sep)
	
	# Save figure
	plt.savefig(path+os.sep+'Output'+os.sep+fileName+'.png',dpi=500)

	plt.close()
	
	
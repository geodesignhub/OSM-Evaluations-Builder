import json, geojson, requests
import random, os, sys, shutil
import GeodesignHub, ShapelyHelper, config
from shapely.geometry.base import BaseGeometry
from shapely.geometry import shape, mapping, shape, asShape
from shapely.geometry import MultiPolygon, MultiPoint, MultiLineString
from shapely.ops import unary_union
from urllib.parse import urlparse
from os.path import splitext, basename
import fiona
import json
import geojson
from fiona.crs import from_epsg
from shapely.geometry import box
from shapely.ops import unary_union

class DataSplitter():
	"""
	This class splits the input file into three files points, lines and polygons. 

	"""
	def __init__(self, osmfile):
		self.points = []
		self.polygons = []
		self.lines = []
		self.osmfile = osmfile
		self.fctemplate = { "type":"FeatureCollection", "features":[] }

	def splitData(self):
		# clip the data to the bounds
		with open(self.osmfile, 'r+') as osmgeojson:
			allOSMData = json.loads(osmgeojson.read())
			
		featLookup = {'Point': self.points, 'MultiPoint':self.points,'LineString':self.lines, 'MultiLineString':self.lines, 'Polygon':self.polygons, 'MultiPolygon':self.polygons }

		for curData in allOSMData['features']:
			featLookup[curData['geometry']['type']].append(curData)
	

	def writeFiles(self):
		allfiles = []
		workingdirpath = os.path.join(os.getcwd(), config.settings['workingdirectory'])
		if not os.path.exists(workingdirpath):
			os.mkdir(workingdirpath)

		if self.points:
			pointfilename = os.path.join(workingdirpath ,  "points.geojson")
			allfiles.append({'location':pointfilename, 'type':'points'})
			fc = self.fctemplate
			fc['features'] = self.points
			with open(pointfilename, 'w') as pointfile:
				pointfile.write(json.dumps(fc))

	
		if self.polygons:
			
			polygonfilename = os.path.join(workingdirpath , "polygons.geojson")
			allfiles.append({'location':polygonfilename, 'type':'polygons'})
			fc = self.fctemplate
			fc['features'] = self.polygons
			with open(polygonfilename, 'w') as polygonfile:
				polygonfile.write(json.dumps(fc))

	
		if self.lines:
			linefilename = os.path.join(workingdirpath , "lines.geojson")
			allfiles.append({'location':linefilename, 'type':'lines'})
			fc = self.fctemplate
			fc['features'] = self.lines
			with open(linefilename, 'w') as linefile:
				linefile.write(json.dumps(fc))

		return allfiles

	
	def clipFile(self):
		# OSM file will always be clipped no need for this method
		pass


class EvaluationBuilder():
	def __init__(self, systemname):

		self.redFeatures = []
		self.yellowFeatures = []
		self.greenFeatures = []
		self.systemname = systemname
		self.symdifference = 0
		self.colorDict = {'red':self.redFeatures, 'yellow':self.yellowFeatures, 'green':self.greenFeatures}

	def processFile(self, color, rawfiledetails, propertyrules):
		curfeatures = self.colorDict[color]

		allfields = []
		curfeatures = []
		for k, v in propertyrules.items():
			allfields.append(k.lower())

		with fiona.open(rawfiledetails['location']) as source:
			for feature in source: 
				try: 
					for curfield in allfields:
						
						if feature['properties'][curfield] in propertyrules[curfield.lower()]:
							if rawfiledetails['type'] == 'points':
								props = feature['properties']
								try:
									pt = asShape(feature['geometry'])
								except Exception as e: 
									pass
								else:
									if pt.is_valid:
										poly = pt.buffer(0.0004)
										bufferedpoly = json.loads(ShapelyHelper.export_to_JSON(poly))
										feature['geometry'] = bufferedpoly
										curfeatures.append({'geometry':bufferedpoly})

							elif rawfiledetails['type'] == 'lines':
								props = feature['properties']
								try:
									pt = asShape(feature['geometry'])
								except Exception as e: 
									pass
								else: 
									if pt.is_valid:
										poly = pt.buffer(0.0002)
										bufferedpoly = json.loads(ShapelyHelper.export_to_JSON(poly))
										feature['geometry'] = bufferedpoly
										curfeatures.append({'geometry':bufferedpoly})
							else:
								curfeatures.append(feature)
				except KeyError as ke:
					pass
					
		self.colorDict[color] = curfeatures




	def createSymDifference(self):
		prjbbox = config.settings['aoibounds']
		bbox= box(prjbbox[0],prjbbox[1], prjbbox[2], prjbbox[3])
		allExistingFeatures = []

		for color, colorfeatures in self.colorDict.items():
			for curcolorfeature in colorfeatures:
				if curcolorfeature['geometry']['type'] == 'GeometryCollection':
					pass
				else:
					try:
						s = asShape(curcolorfeature['geometry'])
					except Exception as e: 
						pass
					else:
						if s.is_valid:
							allExistingFeatures.append(s)
		allExistingFeaturesUnion = unary_union(allExistingFeatures)

		difference = bbox.difference(allExistingFeaturesUnion)
		self.symdifference = difference

	def dissolveColors(self):
		colorDict = self.colorDict
		try:
			cd = {}
			for color, colorFeatures in colorDict.items():
				allExistingcolorfeatures = []
				for curcolorfeature in colorFeatures:
					try:
						s = asShape(curcolorfeature['geometry'])
					except Exception as e: 
						pass
					else:
						if s.is_valid:
							allExistingcolorfeatures.append(s)
				allExistingcolorfeaturesUnion = unary_union(allExistingcolorfeatures)
				if allExistingcolorfeaturesUnion.geom_type == 'MultiPolygon':
					tmpfs = []
					allExistingColorUnion = [polygon for polygon in allExistingcolorfeaturesUnion]
					for existingUnionPolygon in allExistingColorUnion:
						g = json.loads(ShapelyHelper.export_to_JSON(existingUnionPolygon))
						tmpf = {'type':'Feature','properties':{'areatype':color}, 'geometry':g }
						tmpfs.append(tmpf)
					cd[color] = tmpfs

				else:
					g = json.loads(ShapelyHelper.export_to_JSON(allExistingcolorfeaturesUnion))
					tmpf = {'type':'Feature','properties':{'areatype':color}, 'geometry':g }
					cd[color] = [tmpf]
		except Exception as e: 
			# if the unary union fails fail gracefully 
			pass
		else:
			self.colorDict = cd

	def writeEvaluationFile(self):
		opgeojson = self.systemname + '.geojson'
		cwd = os.getcwd()
		outputdirectory = os.path.join(cwd,config.settings['outputdirectory'])
		if not os.path.exists(outputdirectory):
			os.mkdir(outputdirectory)
		opfile = os.path.join(outputdirectory, opgeojson)
		fc = {"type":"FeatureCollection", "features":[]}
		for color, colorfeatures in self.colorDict.items():
			for curcolorfeature in colorfeatures:
				# print curcolorfeature
				f = json.loads(ShapelyHelper.export_to_JSON(curcolorfeature))
				f['properties']={}
				f['properties']['areatype'] = color.lower()
				fc['features'].append(f)

		if self.symdifference:
			geom_type= self.symdifference.geom_type
			if geom_type =='MultiPolygon':
				for geom in self.symdifference.geoms:
					symdiffindfeat = ShapelyHelper.export_to_JSON(geom)
					tmpf = {'type':'Feature','properties':{'areatype':'yellow'}, 'geometry':json.loads(symdiffindfeat)}
					fc['features'].append((tmpf))
			elif geom_type == 'Polygon':
				symdiffindfeat = ShapelyHelper.export_to_JSON(self.symdifference)
				tmpf = {'type':'Feature','properties':{'areatype':'yellow'}, 'geometry':json.loads(symdiffindfeat)}
				fc['features'].append(tmpf)
	
		with open(opfile, 'w') as output_evaluation:
			output_evaluation.write(json.dumps(fc))

	def cleanDirectories(self):
		cwd = os.getcwd()

		folders = [os.path.join(cwd,config.settings['workingdirectory'])]
		for folder in folders:
			for the_file in os.listdir(folder):
			    file_path = os.path.join(folder, the_file)
			    try:
			        if os.path.isfile(file_path):
			            os.unlink(file_path)
			        elif os.path.isdir(file_path): shutil.rmtree(file_path)
			    except Exception as e:
			        pass

if __name__ == '__main__':
	
	osmdataloc = config.settings['osmdata']
	systems = config.settings['systems']
	myDataSplitter = DataSplitter(osmdataloc)
	myDataSplitter.splitData()
	filelist = myDataSplitter.writeFiles()


	for system in systems: 
		processchain = config.processchains[system]
		print("Processing %s .." % system)
		myEvaluationBuilder = EvaluationBuilder(system)
		for evaluationcolor, f in processchain.items():
			try:
				allfiles = f['files']
			except KeyError as ke:
				# no property speficied 
				pass
			else:
				for curfile in allfiles:
					for filekey, filemetadata in curfile.items():
						rawfiledetails = [d for d in filelist if os.path.basename(d['location']).split('.')[0] == filekey.lower()]
						
						for rawfile in rawfiledetails:
							myEvaluationBuilder.processFile(evaluationcolor,rawfile,filemetadata['fields'])	

		myEvaluationBuilder.dissolveColors()
		myEvaluationBuilder.createSymDifference()
		myEvaluationBuilder.writeEvaluationFile()

	
	# myEvaluationBuilder.cleanDirectories()



import json, geojson, requests
import random, os, sys, shutil
import GeodesignHub, ShapelyHelper, config
from shapely.geometry.base import BaseGeometry
from shapely.geometry import shape, mapping, shape, asShape
from shapely.geometry import MultiPolygon, MultiPoint, MultiLineString
from shapely.ops import unary_union
from urlparse import urlparse
from os.path import splitext, basename
import zipfile		
import fiona
from fiona.crs import from_epsg
from shapely.geometry import box
from shapely.ops import unary_union

class DataDownloader():
	def downloadFiles(self, urls):
		for url in urls: 
			disassembled = urlparse(url)
			filename = basename(disassembled.path)
			ext = os.path.splitext(disassembled.path)[1]
			cwd = os.getcwd()
			outputdirectory = os.path.join(cwd,config.settings['workingdirectory'])
			if not os.path.exists(outputdirectory):
				os.mkdir(outputdirectory)
			local_filename = os.path.join(outputdirectory, filename)
			if not os.path.exists(local_filename):
				print "Downloading from %s..." % url
				r = requests.get(url, stream=True)
				with open(local_filename, 'wb') as f:
				    for chunk in r.iter_content(chunk_size=1024): 
				        if chunk: # filter out keep-alive new chunks
				            f.write(chunk)
				            #f.flush() commented by recommendation from J.F.Sebastian
			if ext == '.zip':
				shapefilelist = self.unzipFile(local_filename)

		return shapefilelist

			
	def unzipFile(self, zippath):
		# zip_ref = zipfile.ZipFile(zippath, 'r')
		print "Unzipping archive.. %s" % zippath
		cwd = os.getcwd()
		outputdirectory = os.path.join(cwd,config.settings['workingdirectory'])
		shapefilelist = []
		fh = open(zippath, 'rb')
		z = zipfile.ZipFile(fh)
		for name in z.namelist():
			basename= os.path.basename(name)
			filename, file_extension = os.path.splitext(basename)
			if file_extension == '.shp' and 'MACOSX' not in name:

				clipkey = filename.split('_')[0]

				if 'polygon' in filename:
					filetype = 'polygon'
				elif 'line' in filename:
					filetype = 'lines'
				elif 'point' in filename:
					filetype = 'point'
				else: 
					filetype = 'polygon'
				shapefilelist.append({'filekey':clipkey.lower(),'clipkey': '','type':filetype,'location':name})
			z.extract(name, outputdirectory)
		fh.close()

		return shapefilelist


class AOIClipper():
	''' A class clip source data to AOI'''
	def clipFile(self, aoibbox, osmfile, clipkey, filetype):
		# print aoibbox, osmfile, clipkey
		# schema of the new shapefile
		
		# creation of the new shapefile with the intersection

		opshp = clipkey+'_'+filetype+'.shp'
		cwd = os.getcwd()
		clippeddirectory = os.path.join(cwd,config.settings['workingdirectory'], 'clipped')
		if not os.path.exists(clippeddirectory):
			os.mkdir(clippeddirectory)

		outputdirectory = os.path.join(cwd,config.settings['workingdirectory'])
		opfile = os.path.join(clippeddirectory, opshp)

		osmfile = os.path.join(outputdirectory, osmfile)
	
		with fiona.open(osmfile) as source:
			schema = source.schema
			with fiona.open(opfile, 'w',crs=from_epsg(4326), driver='ESRI Shapefile', schema=schema) as sink:
				# Process only the records intersecting a box.
				for f in source.filter(bbox=aoibbox):  
					prop = f['properties']
					
					sink.write({'geometry':mapping(shape(f['geometry'])),'properties': prop})


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
		cwd = os.getcwd()
		tmpk = []
		for k, v in propertyrules.iteritems():
			tmpk.append(k.upper())
		allfields = tmpk
		filekey = rawfiledetails['filekey']
		filetype = rawfiledetails['type']

		rawfilepath = os.path.join(cwd,config.settings['workingdirectory'], 'clipped', filekey+'_'+filetype+'.shp')
		
		with fiona.open(rawfilepath) as source:
			for feature in source: 
				try: 
					for curfield in allfields:
						if feature['properties'][curfield] in propertyrules[curfield.lower()]:
							if filetype == 'point':
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

							elif filetype == 'lines':
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

		for color, colorfeatures in self.colorDict.iteritems():
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
			for color, colorFeatures in colorDict.iteritems():
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
		for color, colorfeatures in self.colorDict.iteritems():
			for curcolorfeature in colorfeatures:
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
	
	osmdataurl = config.settings['osmdata']
	systems = config.settings['systems']

	myFileDownloader = DataDownloader()
	shapefilelist = myFileDownloader.downloadFiles([osmdataurl])


	myClipper = AOIClipper()
	for curshapefiledict in shapefilelist:	

		myClipper.clipFile(config.settings['aoibounds'], curshapefiledict['location'], curshapefiledict['filekey'], curshapefiledict['type'])

	# for system, processchain in config.processchains.iteritems():
	for system in systems: 
		processchain = config.processchains[system]
		print "Processing %s .." % system
		myEvaluationBuilder = EvaluationBuilder(system)
		for evaluationcolor, f in processchain.iteritems():
			try:
				allfiles = f['files']
			except KeyError as ke:
				# no property speficied 
				pass
			else:
				for curfile in allfiles:
					for filekey, filemetadata in curfile.iteritems():
						rawfiledetails = [d for d in shapefilelist if d['filekey'] == filekey.lower() and d['type']== filemetadata['type']]
						
						for rawfile in rawfiledetails:
							# print evaluationcolor, rawfile,filemetadata['fields']
							myEvaluationBuilder.processFile(evaluationcolor,rawfile,filemetadata['fields'])

	# 	# All colors procesed
	# 	# Create sym difference 
		myEvaluationBuilder.dissolveColors()
		myEvaluationBuilder.createSymDifference()
		myEvaluationBuilder.writeEvaluationFile()

	
	myEvaluationBuilder.cleanDirectories()



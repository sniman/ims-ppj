
#This is a log to read.
#file = open('C:\oracle-staging\proc\log.queue.dat','r')
#file = open('/mxd/proc/log.queue.dat','r')
file = open('/oracle-staging/proc/log.queue.dat','r')
fileContent = file.read()
print "1"

import sys
print "2"
#this funtion is for geoprocessing 
def geoprosessing():	
	import os, sys
	os.environ["DISPLAY"]=":1"
	import datetime
	#sys.path.append("/arcgis10/arcgis/server10.0/python26/lib/python2.6/site-packages/arcpy/")
	sys.path.append("/opt/arcgis/server10.0/python26/lib/python2.6/site-packages/arcpy/")
	import arcpy

	##os.environ['ESRI_SOFTWARE_CLASS'] = 'Professional'
	##gp = arcgisscripting.create(9.3)

	# Check for ArcGIS License type
	##if arcpy.CheckProduct("ArcInfo") == "Available":
	##    arcpy.SetProduct("ArcInfo")
	##elif arcpy.CheckProduct("ArcEditor") == "Available":
	##    arcpy.SetProduct("ArcEditor")
	##else:
	##    print "-- WARNING: ArcGIS ArcEditor or ArcInfo license not found! Process halted."
	##    print "-- WARNING: This tool requires ArcEditor or ArcInfo license to be installed."
	##    print "-- WARNING: Please check with the Server Administrator."
	##    sys.exit()
	print  "-- License available: " + arcpy.ProductInfo()
	# Prompt user to select Folder
	##import Tkinter, tkFileDialog
	##root = Tkinter.Tk()
	##root.withdraw()

	# replace below line with IMS' directory //oracle-staging/shape/
	#dirname = tkFileDialog.askdirectory(parent=root, initialdir="/", title='Select a map folder..')
	
	

	#windows
	dirname =r"/oracle-staging" 
	logpath=r"/oracle-staging/proc/log.dat"
	quelogpath=r"/oracle-staging/proc/log.queue.dat"

	print "-- local file script "
	#clear que
	#file = open(quelogpath,"w")
	#file.write(datetime.datetime.now().ctime()+":")
	#file.truncate() 
	
	# Set main workspace
	if len(dirname) > 0:
		Workspace = dirname
		print Workspace
	else:
		print "-- No folder selected. Process cancelled."
		sys.exit()

	# Check for dxf and shape folders
	dxfWorkspace = os.path.join(Workspace, "dxf")
	shpWorkspace = os.path.join(Workspace, "shape")
	print dxfWorkspace
	if os.path.exists(dxfWorkspace) == False:
		print "-- WARNING: 'dxf' folder not found in: " + Workspace
		print "-- WARNING: Process halted."
		sys.exit()
	elif os.path.exists(shpWorkspace) == False:
		print "-- WARNING: 'shape' folder not found in: " + Workspace
		print "-- WARNING: Process halted."
		sys.exit()

	# Check for dxf file in folder
	dxffiles = 0
	for f in os.listdir(dxfWorkspace):
		if f.endswith(".dxf"):
			dxffiles += 1
			dxffilename = f
		elif f.endswith(".DXF"):
			dxffiles +=1
			dxffilename = f
		elif f.endswith(".dwg"):
			dxffiles +=1
			dxffilename = f
		elif f.endswith(".DWG"):
			dxffiles +=1
			dxffilename = f

	if dxffiles == 0:
		print "-- WARNING: No dxf file found in: " + dxfWorkspace
		print "-- WARNING: Process halted"
		sys.exit()
	elif dxffiles > 1:
		print "-- WARNING: There are " + dxffiles + " found in: " + dxfWorkspace
		print "-- WARNING: Process halted"
		sys.exit()

	# Check for Shapefiles in the 'shape' folder
	shpfiles = 0
	for f in os.listdir(shpWorkspace):
		if f.endswith(".shp"):
			shpfiles += 1

	if shpfiles == 0: # If not Shp file is found, exit.
		print "-- ERROR: No Shapefile (shp) is found in " + Workspace
		sys.exit()

	##WsFolderName = os.path.split(Workspace)[1] # set the folder name according to the selected path above
	WsFolderName = os.path.splitext(dxffilename)[0] # set the gdb name to follow the dxf name
	WsPrefix = WsFolderName + "_"
	WsGDBName = WsFolderName + ".gdb"
	WsGDBPath = os.path.join(shpWorkspace, WsGDBName)
	FDName = "PB_LAYER" # Feature Dataset name
	WsFDName = os.path.join(WsGDBPath, FDName)
	TopoName = FDName + "_TOPO" # Topology Name
	Coordinate_System = "PROJCS['Putrajaya Grid',GEOGCS['GCS_Kertau',DATUM['D_Kertau',SPHEROID['Everest_1830_Modified',6377304.063,300.8017]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Cassini'],PARAMETER['False_Easting',390191.5405],PARAMETER['False_Northing',407215.3658],PARAMETER['Central_Meridian',101.5082444],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',3.680344444],UNIT['Meter',1.0]];-4618700 -10000700 450317182.604702;#;#;0.001;#;#;IsHighPrecision"

	logfilename = WsFolderName + ".log"
	logfile = open(os.path.join(shpWorkspace, logfilename), "w")

	#web module monitoring log
	file = open(logpath,"w")
	file.write(datetime.datetime.now().ctime()+":")
	file.write(WsFolderName+"-PROCESSING");
	
	#web module monitoring log que
	file = open(quelogpath,"w")
	file.write(datetime.datetime.now().ctime()+":")
	file.write(WsFolderName+"-JOB PROCESSING");


	# Delete GDB if exists
	if os.path.exists(WsGDBPath):
		try:
			MyMsg = "-- Existing " + WsGDBName + " found. Deleting.."
			print MyMsg
			logfile.write(MyMsg + "\n")
			arcpy.Delete_management(WsGDBPath, "Workspace")
		except:
			MyMsg =  "-- Error deleting " + WsGDBPath
			print MyMsg
			logfile.write(MyMsg + "\n")
			sys.exit()
		finally:
			MyMsg =  arcpy.GetMessages()
			print MyMsg
			logfile.write(MyMsg + "\n")

	# Create GDB
	MyMsg =  "-- Creating File Geodatabase process started.."
	print MyMsg
	logfile.write(MyMsg + "\n")
	
	#web module monitoring log
	file = open(logpath,"w")
	file.write(datetime.datetime.now().ctime()+":")
	file.write(WsFolderName+"-CREATEGDB [0%]");



	try:
		arcpy.CreateFileGDB_management(shpWorkspace, WsGDBName)
		#web module monitoring log
		file = open(logpath,"w")
		file.write(datetime.datetime.now().ctime()+":")
		file.write(WsFolderName+"-CREATEGDB [10%]");
	except:
		MyMsg =  "-- Error creating " + WsGDBName
		print MyMsg
		logfile.write(MyMsg + "\n")
		sys.exit()
	finally:
		MyMsg =  arcpy.GetMessages()
		print MyMsg
		logfile.write(MyMsg + "\n")

	# Create FeatureDataset in GDB
	#web module monitoring log
	file = open(logpath,"w")
	file.write(datetime.datetime.now().ctime()+":")
	file.write(WsFolderName+"-CREATEFEATUREDATASET [20%]");

	try:
		arcpy.CreateFeatureDataset_management(WsGDBPath, FDName, Coordinate_System)
		#web module monitoring log
		file = open(logpath,"w")
		file.write(datetime.datetime.now().ctime()+":")
		file.write(WsFolderName+"-CREATEFEATUREDATASET [30%]");
	finally:
		MyMsg = arcpy.GetMessages()
		print MyMsg
		logfile.write(MyMsg + "\n")

	for file in os.listdir(shpWorkspace):
		if file.endswith(".shp"):
			try:
				fcname = file.partition(WsPrefix)[2]
				fcname = fcname.replace(".shp","")
				##arcpy.FeatureClassToFeatureClass_conversion(os.path.join(shpWorkspace, file), WsFDName, fcname)
				arcpy.FeatureClassToGeodatabase_conversion(os.path.join(shpWorkspace, file), WsFDName)
			except:
				arcpy.AddMessage(arcpy.GetMessages(2))
			finally:
				MyMsg = arcpy.GetMessages()
				print MyMsg
				logfile.write(MyMsg + "\n")

	# Create Topology
	#web module monitoring log
	file = open(logpath,"w")
	file.write(datetime.datetime.now().ctime()+":")
	file.write(WsFolderName+"-CREATETOPOLOGY [40%]")
	try:
		arcpy.CreateTopology_management(WsFDName, TopoName, "0.01")
		#web module monitoring log
		file = open(logpath,"w")
		file.write(datetime.datetime.now().ctime()+":")
		file.write(WsFolderName+"-CREATETOPOLOGY [50%]")
	except:
		arcpy.AddMessage(arcpy.GetMessages(2))
		sys.exit()
	finally:
		MyMsg = arcpy.GetMessages()
		print MyMsg
		logfile.write(MyMsg + "\n")

	# Add Feature Class to the Topology, Add Topology Rules and Validate Topology
	# add check for Exclusive Lock!
	#
	# ArcGIS Topology Rules:
	# --
	# Must Not Have Gaps (Area) * $
	# Must Not Overlap (Area) * $
	# Must Be Covered By Feature Class Of (Area-Area) * $
	# Must Cover Each Other (Area-Area) * $
	# Must Be Covered By (Area-Area) * $
	# Must Not Overlap With (Area-Area)
	# Must Be Covered By Boundary Of (Line-Area) * ?? $
	# Must Be Covered By Boundary Of (Point-Area) *
	# Must Be Properly Inside (Point-Area)
	# Must Not Overlap (Line) * $
	# Must Not Intersect (Line) * $
	# Must Not Have Dangles (Line) * $
	# Must Not Have Pseudo-Nodes (Line) * $
	# Must Be Covered By Feature Class Of (Line-Line) * ?? $
	# Must Not Overlap With (Line-Line) * $
	# Must Be Covered By (Point-Line)
	# Must Be Covered By Endpoint Of (Point-Line)
	# Boundary Must Be Covered By (Area-Line) * $
	# Boundary Must Be Covered By Boundary Of (Area-Area) $$$ nak tambah
	# Must Not Self-Overlap (Line) * $
	# Must Not Self-Intersect (Line) * $
	# Must Not Intersect Or Touch Interior (Line) * $
	# Endpoint Must Be Covered By (Line-Point)
	# Contains Point (Area-Point)
	# Must Be Single Part (Line) * $

	MyMsg = "-- Adding Topology rules process begin. Please wait.."
	print MyMsg
	logfile.write(MyMsg + "\n")

	#web module monitoring log
	file = open(logpath,"w")
	file.write(datetime.datetime.now().ctime()+":")
	file.write(WsFolderName+"-ADDTOPORULES [60%]")

	from arcpy import env
	env.workspace = WsGDBPath
	WsTopoName = os.path.join(WsFDName, TopoName)
	fds = arcpy.ListFeatureClasses("", "", FDName)
	#web module monitoring log
	file = open(logpath,"w")
	file.write(datetime.datetime.now().ctime()+":")
	file.write(WsFolderName+"-ADDTOPORULES [65%]")
	# Phase 1 (Single Layer topology)
	for fc in fds:
		desc = arcpy.Describe(fc)
		if desc.ShapeType == "Polygon":
			try:
				arcpy.AddFeatureClassToTopology_management(WsTopoName, fc, "1","1")
				arcpy.AddRuleToTopology_management(WsTopoName, "Must Not Have Gaps (Area)", fc)
				arcpy.AddRuleToTopology_management(WsTopoName, "Must Not Overlap (Area)", fc)
			except:
				##arcpy.AddError("Unable to add Topology rule")
				arcpy.AddMessage(arcpy.GetMessages(2))
			finally:
				MyMsg = arcpy.GetMessages()
				print MyMsg
				logfile.write(MyMsg + "\n")
		elif desc.ShapeType == "Polyline":
			try:
				arcpy.AddFeatureClassToTopology_management(WsTopoName, fc, "1", "1")
				arcpy.AddRuleToTopology_management(WsTopoName, "Must Not Overlap (Line)", fc)
				arcpy.AddRuleToTopology_management(WsTopoName, "Must Not Intersect (Line)", fc)
				arcpy.AddRuleToTopology_management(WsTopoName, "Must Not Have Dangles (Line)", fc)
				arcpy.AddRuleToTopology_management(WsTopoName, "Must Not Have Pseudo-Nodes (Line)", fc)
				arcpy.AddRuleToTopology_management(WsTopoName, "Must Not Self-Overlap (Line)", fc)
				arcpy.AddRuleToTopology_management(WsTopoName, "Must Not Self-Intersect (Line)", fc)
				arcpy.AddRuleToTopology_management(WsTopoName, "Must Not Intersect Or Touch Interior (Line)", fc)
				arcpy.AddRuleToTopology_management(WsTopoName, "Must Be Single Part (Line)", fc)
			except:
				##arcpy.AddError("Unable to add Topology rule")
				arcpy.AddMessage(arcpy.GetMessages(2))
			finally:
				MyMsg = arcpy.GetMessages()
				print MyMsg
				logfile.write(MyMsg + "\n")

	# Phase 2 (Multiple Layer Topology)
	#web module monitoring log
	file = open(logpath,"w")
	file.write(datetime.datetime.now().ctime()+":")
	file.write(WsFolderName+"-ADDTOPORULES [70%]")
	for fc in fds:
		lyr1 = str.upper(str(fc)).partition(WsPrefix.replace("-","_"))[2] # convert Unicode to String
		desc = arcpy.Describe(fc)
		for fc2 in fds:
			lyr2 = str.upper(str(fc2)).partition(WsPrefix.replace("-","_"))[2] # convert Unicode to String
			desc2 = arcpy.Describe(fc2)
			if fc2 <> fc:
				# Polygon with Polygon
				if desc.ShapeType == "Polygon" and desc2.ShapeType == "Polygon":
					if lyr1 == "SUBMN_POLY":
						##lyrs = WsPrefix + "SUB_PARCEL_POLY " + WsPrefix + "SUBP_ELE_POLY " + WsPrefix + "PLANNG_CTL_SYM " + WsPrefix + "BLDG_SETBACK"
						if lyr2 in "SUB_PARCEL_POLY SUBP_ELE_POLY PLANNG_CTL_SYM BLDG_SETBACK":
							try:
								arcpy.AddRuleToTopology_management(WsTopoName, "Must Be Covered By Feature Class Of (Area-Area)", fc, "", fc2, "")
								if lyr2 <> "SUBP_ELE_POLY":
									if lyr2 <> "PLANNG_CTL_SYM":
										arcpy.AddRuleToTopology_management(WsTopoName, "Must Be Covered By (Area-Area)", fc2, "", fc, "")
									else:
										arcpy.AddRuleToTopology_management(WsTopoName, "Must Be Covered By (Area-Area)", fc, "", fc2, "")
							except:
								##arcpy.AddError("Unable to add Topology rule")
								arcpy.AddMessage(arcpy.GetMessages(2))
							finally:
								MyMsg = arcpy.GetMessages()
								print MyMsg
								logfile.write(MyMsg + "\n")
					elif lyr1 == "SUB_PARCEL_POLY":
						##lyrs = WsPrefix + "SUBP_ELE_POLY " + WsPrefix + "BLDG_SETBACK"
						if lyr2 in "SUBP_ELE_POLY BLDG_SETBACK":
							try:
								arcpy.AddRuleToTopology_management(WsTopoName, "Must Be Covered By Feature Class Of (Area-Area)", fc, "", fc2, "")
								if lyr2 == "BLDG_SETBACK":
									arcpy.AddRuleToTopology_management(WsTopoName, "Must Be Covered By (Area-Area)", fc2, "", fc, "")
							except:
								##arcpy.AddError("Unable to add Topology rule")
								arcpy.AddMessage(arcpy.GetMessages(2))
							finally:
								MyMsg = arcpy.GetMessages()
								print MyMsg
								logfile.write(MyMsg + "\n")
						elif lyr2 == "SUBMN_POLY":
							try:
								arcpy.AddRuleToTopology_management(WsTopoName, "Must Cover Each Other (Area-Area)", fc, "", fc2, "")
								arcpy.AddRuleToTopology_management(WsTopoName, "Boundary Must Be Covered By Boundary Of (Area-Area)", fc, "", fc2, "")
							except:
								##arcpy.AddError("Unable to add Topology rule")
								arcpy.AddMessage(arcpy.GetMessages(2))
							finally:
								MyMsg = arcpy.GetMessages()
								print MyMsg
								logfile.write(MyMsg + "\n")
					elif lyr1 == "SUBP_ELE_POLY":
						##lyrs = WsPrefix + "SUB_PARCEL_POLY " + WsPrefix + "SUBMN_POLY"
						if lyr2 in "SUB_PARCEL_POLY SUBMN_POLY":
							try:
								arcpy.AddRuleToTopology_management(WsTopoName, "Must Cover Each Other (Area-Area)", fc, "", fc2, "")
								arcpy.AddRuleToTopology_management(WsTopoName, "Must Be Covered By (Area-Area)", fc, "", fc2, "")
								arcpy.AddRuleToTopology_management(WsTopoName, "Boundary Must Be Covered By Boundary Of (Area-Area)", fc, "", fc2, "")
							except:
								##arcpy.AddError("Unable to add Topology rule")
								arcpy.AddMessage(arcpy.GetMessages(2))
							finally:
								MyMsg = arcpy.GetMessages()
								print MyMsg
								logfile.write(MyMsg + "\n")
					elif lyr1 == "BLDG_SETBACK":
						##lyrs = WsPrefix + "SUB_PARCEL_POLY " + WsPrefix + "SUBMN_POLY"
						if lyr2 in "SUB_PARCEL_POLY SUBMN_POLY":
							try:
								arcpy.AddRuleToTopology_management(WsTopoName, "Boundary Must Be Covered By Boundary Of (Area-Area)", fc, "", fc2, "")
							except:
								##arcpy.AddError("Unable to add Topology rule")
								arcpy.AddMessage(arcpy.GetMessages(2))
							finally:
								MyMsg = arcpy.GetMessages()
								print MyMsg
								logfile.write(MyMsg + "\n")
					elif lyr1 == "PLANNG_CTL_SYM":
						##lyrs = WsPrefix + "SUB_PARCEL_POLY " + WsPrefix + "SUBMN_POLY"
						if lyr2 in "SUB_PARCEL_POLY SUBMN_POLY":
							try:
								arcpy.AddRuleToTopology_management(WsTopoName, "Boundary Must Be Covered By Boundary Of (Area-Area)", fc, "", fc2, "")
							except:
								##arcpy.AddError("Unable to add Topology rule")
								arcpy.AddMessage(arcpy.GetMessages(2))
							finally:
								MyMsg = arcpy.GetMessages()
								print MyMsg
								logfile.write(MyMsg + "\n")

				# Polygon with Polyline
				elif desc.ShapeType == "Polygon" and desc2.ShapeType == "Polyline":
					if lyr1 == "SUBP_ELE_POLY" and lyr2 == "BLDG_SETBACK_LINE":
						try:
							arcpy.AddRuleToTopology_management(WsTopoName, "Boundary Must Be Covered By Boundary Of (Area-Area)", fc, "", fc2, "")
						except:
							##arcpy.AddError("Unable to add Topology rule")
							  arcpy.AddMessage(arcpy.GetMessages(2))
						finally:
							MyMsg = arcpy.GetMessages()
							print MyMsg
							logfile.write(MyMsg + "\n")

				# Polyline with Polyline
				elif desc.ShapeType == "Polyline" and desc2.ShapeType == "Polyline":
					if lyr1 == "BLDG_SETBACK_LINE":
						try:
							if lyr2 == "SUBP_ELE_INTER_DETL":
								arcpy.AddRuleToTopology_management(WsTopoName, "Must Not Overlap With (Line-Line)", fc, "", fc2, "")
								arcpy.AddRuleToTopology_management(WsTopoName, "Must Be Covered By Feature Class Of (Line-Line)", fc, "", fc2, "")
						except:
							##arcpy.AddError("Unable to add Topology rule")
							  arcpy.AddMessage(arcpy.GetMessages(2))
						finally:
							MyMsg = arcpy.GetMessages()
							print MyMsg
							logfile.write(MyMsg + "\n")

				# Polyline with Polygon
				elif desc.ShapeType == "Polyline" and desc2.ShapeType == "Polygon":
					if lyr1 == "BLDG_SETBACK_LINE":
						try:
							##lyrs = WsPrefix + "SUBMN_POLY " + WsPrefix + "SUB_PARCEL_POLY"
							if lyr2 in "SUBMN_POLY SUB_PARCEL_POLY":
								arcpy.AddRuleToTopology_management(WsTopoName, "Must Be Covered By Boundary Of (Line-Area)", fc, "", fc2, "")
						except:
							##arcpy.AddError("Unable to add Topology rule")
							  arcpy.AddMessage(arcpy.GetMessages(2))
						finally:
							MyMsg = arcpy.GetMessages()
							print MyMsg
							logfile.write(MyMsg + "\n")

	# Validate Topology
	MyMsg = "-- Validating Topology (Full Extent).."
	print MyMsg
	logfile.write(MyMsg + "\n")

	#web module monitoring log
	file = open(logpath,"w")
	file.write(datetime.datetime.now().ctime()+":")
	file.write(WsFolderName+"-VALIDATETOPO [80%]")

	try:
		arcpy.ValidateTopology_management(WsTopoName) # WsTopoName, "Full_Extent"
	except:
		arcpy.AddMessage(arcpy.GetMessages(2))
	finally:
		MyMsg = arcpy.GetMessages()
		print MyMsg
		logfile.write(MyMsg + "\n")

	# Zip File Geodatabase
	import zipfile, glob
	#web module monitoring log
	file = open(logpath,"w")
	file.write(datetime.datetime.now().ctime()+":")
	file.write(WsFolderName+"-FINALIZING [90%]")
	WsZipFile = os.path.join(shpWorkspace, WsFolderName + ".zip")

	print "-- Zipping process started.."
	def zipGDB(inGDB, outZIP):
		if not (os.path.exists(inGDB)):
			return False

		if (os.path.exists(outZIP)): # Delete existing Zip file
			MyMsg = "-- Existing ZIP file found - deleting.."
			print MyMsg
			logfile.write(MyMsg + "\n")
			os.remove(outZIP)

		zipobj = zipfile.ZipFile(outZIP,'w')
		MyMsg = "-- Zipping: " + WsGDBName
		print MyMsg
		logfile.write(MyMsg + "\n")
		for WsZipFile in glob.glob(inGDB + "/*"):
			zipobj.write(WsZipFile, os.path.basename(inGDB) + "/" + os.path.basename(WsZipFile), zipfile.ZIP_DEFLATED)

		zipobj.close()

		return True

	#web module monitoring log
	file = open(logpath,"w")
	file.write(datetime.datetime.now().ctime()+":")
	file.write(WsFolderName+"-FINALIZING [95%]")	
	zipGDB(WsGDBPath, WsZipFile)
	
	
	file = open(logpath,"w")
	file.write(datetime.datetime.now().ctime()+":")
	file.write(WsFolderName+"-PENDINGMAIL       ")


	#clear que
	file = open(quelogpath,"w")
	#file.write(datetime.datetime.now().ctime()+":")
	file.truncate() 

	MyMsg = "-- File Geodatabase has been Zipped. see: " + os.path.basename(WsZipFile)
	print MyMsg
	logfile.write(MyMsg + "\n")
	logfile.close()

print "3";
#scrip version
def scriptVersion():
	print 'Copyright 2012 OrenBytes Malaysia'
	print 'Version : 1.2'
	print 'Client :IMS Malaysia'
print "4"
#remove process marker
def removeProcessMarker():
	import os
	path='/oracle-staging/shape/' 
	dirList=os.listdir(path)
	for fname in dirList:
		print fname
		if fname.endswith(".OB"):
			removepath = os.path.join(path,fname)
			print removepath
			os.remove(removepath)
				
	
print "5";	
print fileContent
#to check if the geo are on que to processed and main execute point
for word in fileContent.split():
	print word
	if 'QUEUE' in word:
		print word
		print 'Geoprocessing start'
		geoprosessing()
		print 'Initializing process'
		print 'Geoprocessing end'
	else:
		scriptVersion()


		




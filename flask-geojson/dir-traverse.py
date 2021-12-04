# -*- coding: utf-8 -*-
"""Aplicacion python embebida en C++"""
__author__      = "Diego Cadogan"
__copyright__   = "Copyright 2018, sss.com"
__version__ = "0.5"
__license__ = "GPL"

import sys
import os
import fnmatch
import platform
import time
import xml.dom.minidom
from random import seed
seed(12345)

def traverseDir(currdir):
	""" Traverse estructura de directorios """

	target_dirs = []
	if os.path.isdir(currdir):
		#print("Directorio correcto -> " , currdir)
		for d in os.listdir(currdir):
			p = os.path.join(currdir,d)
			if os.path.isdir(p):
				target_dirs.append(p)
	else:
		print("Directorio incorrecto -> ", currdir)
	return target_dirs

class ccnetProject:
	""" Clase del modelo"""

	projectName = None
	solutionFilename = None
	description = None
	queue = None
	categoryType = None
	targets = None
	properties = None

class ccnetProjectList:
	""" Agrega nuevos proyectos a una clase existente """
	""" STATUS: Test """
	projects = dict()

	def __init__(self, projects):
		pass

	def addNew(self, p):
		if p.projectName not in projects:
			projects[p.projectName] = p

	def remove(self, p):
		if p.projectName in projects:
			projects[p.projectName].pop()

def saveXml(p, f, document):
	f = os.path.join(p, f)
	fo = open(f, 'w')
	fo.write(document.toprettyxml())
	fo.close()

def usage():
	"""Uso: \n\n
	<options> [target_src_directory] [xml_save_dir] [xml_file] [project_type]\n
	Opciones:\n
	\t -v\t verboso\n
	\t -V\t modo debug\n
	\t -demo\t modo demo"""
	print(__doc__)
	print(usage.__doc__)

if __name__ == "__main__":
	sys.argv.remove(sys.argv[0])
	print("Argumentos: ", sys.argv)
	if(len(sys.argv)==0):
		usage()
		sys.exit(1)
	if(len(sys.argv)>0):
		if ['-v']  in sys.argv:
			sys.argv.remove('-v')
			verbose=True
		if ['-V'] in sys.argv:
			sys.argv.remove('-V')
			debug=True
		if '-demo' in sys.argv:
			sys.argv.remove('-demo')
		if (len(sys.argv)>3):
			target_src = sys.argv[0]
			xml_save_dir = sys.argv[1]
			xml_file = sys.argv[2]
			proj_type = sys.argv[3]
			if proj_type=='cmake':
				sys.exit(0)
	sys.exit(0)
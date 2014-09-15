"""
Program to parse the files from the topmost directory
"""
#!/bin/python
import os 
import fnmatch 

#Function to generate the xml filenames from the topmost directory
def locate (pattern,root=os.curdir):
	for path,dirs,files,in os.walk(os.path.abspath(root)):
		for filename in fnmatch.filter(files,pattern):
			yield os.path.join(path,filename)
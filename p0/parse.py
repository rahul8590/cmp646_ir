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

#Function to count the tokens seperated by whitespace / tab in file
def count_words(filename):
	num_words = 0 
	with open(filename,'r') as f:
		for line in f:
			words = line.split(' ')
			num_words += len(words)
	return num_words


if __name__ == '__main__':
	token_count = 0 
	for filename in locate("*.xml"):
		token_count += count_words(filename)
		print "for ",filename , "token count =>",token_count
	print "the final token count is ", token_count


"""
The file is response for parsing xml and compiling statistics 
"""

#!/bin/python
import xml.etree.cElementTree as cxml
import re
import os 
import fnmatch


"""
dict_word['word'] = [[(book_name,[page_nos]),
                      (book_name,page_no)],
                      count]
"""

#All the global variables will be declared in here 
dword = {}
#-------------------------------------------------


#Function to generate the xml filenames from the topmost directory
def locate (pattern,root=os.curdir):
  for path,dirs,files,in os.walk(os.path.abspath(root)):
    for filename in fnmatch.filter(files,pattern):
      yield os.path.join(path,filename)

#Word Count
def populate_dict(word):
  dword[word] = dword.get(word,0) + 1


#line is a simple string which can get junk characters
def sanitize_line(line_n):
   if line_n == None or line_n == ' ': return None
   line1 = str(line_n)
   line1 = line1.lower()
   #print "the line is ", line1
   rx = re.compile('\W+') #Getting only alphanumeric letters first
   #rnos = re.compile('[0-9]')
   rline = rx.sub(' ',line1).strip()
   #nline = rnos.subl(' ',rline).strip() #Only words and possible extra whitespaces. 
   #re.sub(' +', ' ',nline)
   return rline #string 


def parse_xml(filename):
  for event,elem in cxml.iterparse(filename):
    if elem.tag == 'page':
      print elem.attrib
      for node in elem.findall('./region/section/line'):
        # node.text  will have unsanitized <line> information.  
        san_string = sanitize_line(node.text)
        if san_string == None or san_string == ' ': continue
        for i in san_string.split(' '): #populating the dictionary of words
          populate_dict(i)


if __name__ == '__main__':
  for filename in locate("*.xml"):
    parse_xml(filename)
  print "The Word Count dictionary is "
  print  dword 

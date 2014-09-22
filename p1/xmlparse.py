"""
The file is response for parsing xml and compiling statistics 
"""

#!/bin/python
import xml.etree.cElementTree as cxml
import re
import os 
import fnmatch
import multiprocessing as mp
#import bsddb
#import itertools 
import collections 
import pickle

from pympler import summary
from pympler import muppy

"""
dict_word['word'] = [[(book_name,[page_nos]),
                      (book_name,page_no)],
                      count]
"""

#All the global variables will be declared in here 
dword = {}
itvalue = 0
#-------------------------------------------------


#Function to generate the xml filenames from the topmost directory
def locate (pattern,root=os.curdir):
  for path,dirs,files,in os.walk(os.path.abspath(root)):
    for filename in fnmatch.filter(files,pattern):
      yield os.path.join(path,filename)

"""
#Word Count
def populate_dict(word):
  dword[word] = dword.get(word,0) + 1
"""


#line is a simple string which can get junk characters
def sanitize_line(line_n):
   if line_n == None or line_n == ' ': return None
   line1 = str(line_n)
   line1 = line1.lower()
   #print "the line is ", line1
   rx = re.compile('\W+') #Getting only alphanumeric letters first
   line_ascii = re.sub(r'[^\x00-\x7F]+',' ', line1)  #Remove non-ascii elements from string
   #rnos = re.compile('[0-9]')
   rline = rx.sub(' ',line_ascii).strip()
   #nline = rnos.subl(' ',rline).strip() #Only words and possible extra whitespaces. 
   #re.sub(' +', ' ',nline)
   return rline #string 


def parse_xml(filename):
  dword = {}
  global itvalue
  try:
    itvalue += 1
    for event,elem in cxml.iterparse(filename):
      if elem.tag == 'page':
        #print elem.attrib
        for node in elem.findall('./region/section/line'):
          # node.text  will have unsanitized <line> information.  
          san_string = sanitize_line(node.text)
          if san_string == None or san_string == ' ': continue
          for i in san_string.split(' '): #populating the dictionary of words
            dword[i] = dword.get(i,0) + 1
  except:
    print filename , "is having Encoding problems or parsing errors"
  #all_objects = muppy.get_objects()
  #sum1 = summary.summarize(all_objects)
  print "Iteration " , itvalue
  #summary.print_(sum1)
  return dword




if __name__ == '__main__':
  numthreads = 2  
  pool = mp.Pool(processes=numthreads)
  dword_list = pool.map(parse_xml, (locate("*.xml")))
  #final_dword = bsddb.btopen('wordc','c')
  #final_dword = collections.Counter()
  #map(final_dword.update,dword_list)
  #final_dword = dict(kv for d in dictlist for kv in d.iteritems())
  #for i in dword_list:
  #  final_dword.update(i)
  print "dumping dword_list into pickle format"
  with open('word_count_list.pickle', 'wb') as handle:
    pickle.dump(dword_list, handle)
  print "The final Word Count List is calculated and dumped"



#/rahul_extra/books-big/D3FA3CC0C1631327/maistrepierrepat00pathuoft_ocrml.xml

"""
To find the maximum elements of the final_dword aka fwc 
import operator
max(fwc.iterkeys(), key=(lambda key:fwc[key]))

"""
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
import cPickle as pickle
import tokenize , token
import logging

from xml.sax.saxutils import unescape
from pympler import summary
from pympler import muppy
from operator import itemgetter



#Initializing Logger in here
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('./xml_parse.log')
formatter = logging.Formatter('rar small %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

#All the global variables will be declared in here 
itvalue = 0
#-------------------------------------------------


#Function to generate the xml filenames from the topmost directory
def locate (pattern,root=os.curdir):
  for path,dirs,files,in os.walk(os.path.abspath(root)):
    for filename in fnmatch.filter(files,pattern):
      yield os.path.join(path,filename)


#line is a simple string which can get junk characters
def sanitize_line(line_n):
   if line_n == None or line_n == ' ': return None
   line1 = str(line_n)
   line1 = line1.replace('-','').replace('`','')
   line1 = unescape(line1,{"&quot;": " "})
   rline = re.sub('\W+',' ',line1).strip().lower()
   return rline #string 

#Main file for xml parsing
def parse_xml(filename):
  dword = {}
  global itvalue
  try:
    itvalue += 1
    for event,elem in cxml.iterparse(filename):
      if elem.tag == 'page':
        #print elem.attrib
        pgid = elem.attrib['id']
        #print "page no is" , pgid
        for node in elem.findall('./region/section/line'):
          # node.text  will have unsanitized <line> information.
          for line in node.itertext():
            #commenting the regular procedure to sanitize string
            #print "node to be sanitizes =>" , node.text
            san_string = sanitize_line(line)
            #print "after sanitization =>", san_string
            if san_string == None or san_string == ' ': continue
            else:
              """
              The list is a value of dictionary which holds
              l = [word count , page count , book count]
              """
              for i in san_string.split(' '): #populating the dictionary of words
                if dword.has_key(i):
                  dword[i][0] += 1 
                  dword[i][1].add(pgid)
                else:
                  dword[i] = [1,set([pgid]),1]
  except:
    logger.error(filename + "is having Encoding problems or parsing errors")
    return {}
  #all_objects = muppy.get_objects()
  #sum1 = summary.summarize(all_objects)
  print "Iteration " , itvalue
  #summary.print_(sum1)
  #Counting the length of all the pages the word has occured and sending only the total
  #count  of it
  for k,v in dword.items():
    temp = dword[k]
    temp[1] = len(temp[1])
    dword[k] = temp

  return dword




if __name__ == '__main__':
  numthreads = 2  
  pool = mp.Pool(processes=numthreads)
  #dword_list = pool.imap(parse_xml, (locate("*.xml")))
  #final_dword = bsddb.btopen('wordc','c')
  final_dword = collections.Counter()
  #map(final_dword.update,dword_list)
  #final_dword = dict(kv for d in dictlist for kv in d.iteritems())
  #final_dword = {}
  for d in pool.imap(parse_xml, (locate("*.xml"))):
    for k,v in d.items():
      if final_dword.has_key(k):
        dv = final_dword[k]
        final_dword[k] = [sum(i) for i in zip(v,dv)]
      else:
        final_dword[k] = v
  

  tu = len(final_dword)
  to = sum(l[0] for l in final_dword.values())
  #print final_dword
  logger.info("TO "+str(tu))
  logger.info("TU "+str(to))
  most_common_list = final_dword.most_common(50)
  for i in range(0,len(most_common_list)):
    s = str(i+1)+" "+str(most_common_list[i][0])+" "+str(most_common_list[i][1][2])+" "+str(most_common_list[i][1][1])+" "+str(most_common_list[i][1][0])
    logger.info(s)

  print "The final Word Count List is calculated ", tu
  print "total no of tokens" , to
  print "most common words are ", final_dword.most_common(50)
  
  l = ['powerful' , 'strong' , 'butter' , 'salt', 'washington', 'james', 'church']
  
  #Sorting the entire dictionary to get the values of elements of l
  sorted_word = sorted(final_dword.items(),key=itemgetter(1), reverse=True)

  for i in range(0,len(sorted_word)):
    for w in l:
      if sorted_word[i][0] == w:
        print w , "=>" , sorted_word[i] , "index =>" , i
        s = str(i)+" "+str(w)+" "+str(sorted_word[i][1][2]) + " " + str(sorted_word[i][1][1]) + " " + str(sorted_word[i][1][0])
        logger.info(s)



#/rahul_extra/books-big/D3FA3CC0C1631327/maistrepierrepat00pathuoft_ocrml.xml
"""
To find the maximum elements of the final_dword aka fwc 
import operator
max(fwc.iterkeys(), key=(lambda key:fwc[key]))

"""

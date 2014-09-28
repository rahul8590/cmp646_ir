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
import ast
import shelve


from pympler import summary
from pympler import muppy
from operator import itemgetter



#All the global variables will be declared in here 
#dword = {}
itvalue = 0
tempdb = shelve.open('cache')
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
   #line1 = line1.lower()
   #print "the line is ", line1
   #rx = re.compile('\W+') #Getting only alphanumeric letters first
   #line_ascii = re.sub(r'[^\x00-\x7F]+',' ', line1)  #Remove non-ascii elements from string
   #rnos = re.compile('[0-9]')
   rline = re.sub('\W+',' ',line1).strip().lower()
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
        #print_nt elem.attrib
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
          """
          for t in tokenize.generate_tokens(iter([node.text]).next):
            if token.tok_name[t[0]] == 'STRING':
              dword[t[1]] = dword.get(t[1],0) + 1
              print t[1]
          """
  except:
    print filename , "is having Encoding problems or parsing errors"
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



  
import sys

if __name__ == '__main__':
  numthreads = 2  
  pool = mp.Pool(processes=numthreads)
  #dword_list = pool.map(parse_xml, (locate("*.xml")))
  #final_dword = bsddb.btopen('wordc','c')
  final_dword = collections.Counter()
  #map(final_dword.update,dword_list)
  #final_dword = dict(kv for d in dictlist for kv in d.iteritems())
  #a = locate("*.xml")
  #for x in :
  #  d = parse_xml(x)
  for d in pool.imap(parse_xml, (locate("*.xml"))):
    for k,v in d.items():
      if final_dword.has_key(k):
        dv = final_dword[k]
        final_dword[k] = [sum(i) for i in zip(v,dv)]
      else:
        final_dword[k] = v
  """
  for i in dword_list:
    final_dword.update(i)
  """
  





  """
  print "dumping dword_list into pickle format"
  with open('word_count_big_list.pickle', 'wb') as handle:
    pickle.fast = True 
    pickle.dump(dword_list, handle)
  """
  #print final_dword
  print "The final Word Count List is calculated ", len(final_dword)
  print "total no of tokens" , sum(l[0] for l in final_dword.values())
  print "most common words are ", final_dword.most_common(50)
  
  l = ['powerful' , 'strong' , 'butter' , 'salt', 'washington', 'james', 'church']
  
  #Sorting the entire dictionary to get the values of elements of l
  sorted_word = sorted(final_dword.items(),key=itemgetter(1), reverse=True)

  for i in range(0,len(sorted_word)):
    for w in l:
      if sorted_word[i][0] == w:
        print w , "=>" , sorted_word[i] , "index =>" , i





#/rahul_extra/books-big/D3FA3CC0C1631327/maistrepierrepat00pathuoft_ocrml.xml

"""
To find the maximum elements of the final_dword aka fwc 
import operator
max(fwc.iterkeys(), key=(lambda key:fwc[key]))

"""

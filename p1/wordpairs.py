"""
The file is for computing word pairs statistics  
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
import nltk

import logging

from xml.sax.saxutils import unescape
from pympler import summary
from pympler import muppy
from operator import itemgetter



#All the global variables will be declared in here 
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('./xml_parse.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

itvalue = 0
#-------------------------------------------------


#Function to
def locate (pattern,root=os.curdir):
  for path,dirs,files,in os.walk(os.path.abspath(root)):
    for filename in fnmatch.filter(files,pattern):
      yield os.path.join(path,filename)
  
#line is a simple string which can get junk characters
def sanitize_line(line_n):
   if line_n == None or line_n == ' ': return None
   line1 = str(line_n)
   line1 = unescape(line1,{"&quot;": " "})
   rline = re.sub('\W+',' ',line1).strip().lower()
   return rline #string 

def page_stat(filename):
  dword = {}
  wp = ['powerful' , 'strong' , 'butter' , 'salt', 'washington', 'james', 'church']
  try:
    for event,elem in cxml.iterparse(filename):
       if elem.tag == 'page':
         #print elem.attrib
         #pgid = elem.attrib['id']
         #print "page no is" , pgid
         page_buffer = ' '
         for node in elem.findall('./region/section/line'):
           # node.text  will have unsanitized <line> information.
           for line in node.itertext():
             #commenting the regular procedure to sanitize string
             #print "node to be sanitizes =>" , node.text
             san_string = sanitize_line(line)
             #print "after sanitization =>", san_string
             if san_string == None or san_string == ' ': continue
             else:
               page_buffer += san_string + ' '

         #if any(sword in page_buffer for sword in wp):
         for sword in wp:
            if sword in page_buffer:
              for word in page_buffer.split(' '):
                if word in stop_list or word == sword or word == '': continue
                dword[(sword,word)] = dword.get((sword,word),0) + 1
  except:
    print "There is been an parsing error for the file" , filename
    logger.error(filename +"is having Encoding problems or parsing errors")
    
  return dword

def chunk_stat(filename):
  dword = {}
  sword = "powerful"
  try:

    for event,elem in cxml.iterparse(filename):
       if elem.tag == 'page':
         #print elem.attrib
         pgid = elem.attrib['id']
         #print "page no is" , pgid
         page_buffer = ' '
         for node in elem.findall('./region/section/line'):
           # node.text  will have unsanitized <line> information.
           for line in node.itertext():
             #commenting the regular procedure to sanitize string
             #print "node to be sanitizes =>" , node.text
             san_string = sanitize_line(line)
             #print "after sanitization =>", san_string
             if san_string == None or san_string == ' ': continue
             else:
              word_list  = san_string.split(' ')
              l20 = [word_list[i:i + 20] for i in range(0, len(word_list), 20)]

              for chunk in l20:
                if sword in chunk:
                  for word in chunk:
                    if word in stop_list or word == sword or word == '': continue
                    dword[word] = dword.get(word,0) + 1
  except:
    print "There is been an parsing error for the file" , filename
    logger.error(filename , "is having Encoding problems or parsing errors")

  return dword

def parse_xml(filename):
  dword = {}
  global itvalue
  ddist = {} #Frequence distribution of the word

  #print "the stop_list is ", stop_list
  
  try:
    itvalue += 1
    
    for event,elem in cxml.iterparse(filename):
      if elem.tag == 'page':
        #print elem.attrib
        pgid = elem.attrib['id']
        #print "page no is" , pgid
        page_buffer = ''
        for node in elem.findall('./region/section/line'):
          # node.text  will have unsanitized <line> information.
          for line in node.itertext():
            #commenting the regular procedure to sanitize string
            #print "node to be sanitizes =>" , node.text
            san_string = sanitize_line(line)
            #print "after sanitization =>", san_string
            if san_string == None or san_string == ' ': continue
            else:
              page_buffer += san_string 
              """
              The list is a value of dictionary which holds
              l = [word count , page count , book count]
              """
              """
              for i in san_string.split(' '): #populating the dictionary of words
                if dword.has_key(i):
                  dword[i][0] += 1 
                  dword[i][1].add(pgid)
                else:
                  dword[i] = [1,set([pgid]),1]          
              """
        wordlist = page_buffer.split(' ')
        pairs = nltk.bigrams(wordlist)
        fdist = nltk.FreqDist(pairs)

        for w1,w2 in fdist.items():
          for i in wp:
            if w1[0] in stop_list or w1[1] in stop_list or w1[1] == i:
              continue
            else:
              if i in w1:
                ddist[w1] = ddist.get(w1,w2) + w2


        """
        find adjacent word 

        for i in range(0,len(wordlist)):
          if wordlist[i] in wp:
            print "word found" , wordlist[i] , "adjacent word" , wordlist[i+1]
            print "the page is ----"
            print page_buffer

        ---- ends here -----
        """




  except:
    print filename , "is having Encoding problems or parsing errors"
    #return dword
  

  #all_objects = muppy.get_objects()
  #sum1 = summary.summarize(all_objects)
  #print "Iteration " , itvalue
  #summary.print_(sum1)
  #Counting the length of all the pages the word has occured and sending only the total
  #count  of it
  
  """
  for k,v in dword.items():
    temp = dword[k]
    temp[1] = len(temp[1])
    dword[k] = temp
  """
  #print "the Frequence distribution is ", ddist

  #return dword
  return ddist


if __name__ == '__main__':
  
  wp = ['powerful' , 'strong' , 'butter' , 'salt', 'washington', 'james', 'church']
  
  stop_list = []
  
  #populating pair dictionaries to store counter collections
  pair_dict = {i:[] for i in wp}

  file_stop_list = open('stopwords.list.sorted' ,'r')
  for i in file_stop_list:
    i = i.strip('\n')
    stop_list.append(i)
  

  numthreads = 2  
  pool = mp.Pool(processes=numthreads)
  
  #dword_list = pool.map(parse_xml, (locate("*.xml")))
  #dword_list = pool.map(chunk_stat, (locate("*.xml")))
  #sword = "church"
  dword_list = pool.map(page_stat, (locate("*.xml")))
  final_dword = collections.Counter()
  for i in dword_list:
    final_dword.update(i)
  

  #sorted_word = sorted(final_dword.items(),key=itemgetter(1), reverse=True)

  for cword in wp:
    clist = [i for i in final_dword.items() if i[0] == cword]
    #clist = sorted(final_dword.items(),key=lambda(k,v): k[0] == cword)
    #print clist
    print "the pairs in ",cword 
    print clist[0:5],
  """
  most_common = final_dword.most_common(200)
  print "the most common words are", most_common

  for cword in wp:
    count = 0
    for i in most_common:
      if count > 5: continue
      if i[0][0] == cword:
        print i
        count += 1
  """

  #map(final_dword.update,dword_list)
  #final_dword = dict(kv for d in dictlist for kv in d.iteritems())
  """
  for d in dword_list:
    for k,v in d.items():
      if final_dword.has_key(k):
        dv = final_dword[k]
        final_dword[k] = [sum(i) for i in zip(v,dv)]
      else:
        final_dword[k] = v 
  """
  
  




  """
  print "dumping dword_list into pickle format"
  with open('word_count_big_list.pickle', 'wb') as handle:
    pickle.fast = True 
    pickle.dump(dword_list, handle)
  """
  #print final_dword

  """
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
  """





#/rahul_extra/books-big/D3FA3CC0C1631327/maistrepierrepat00pathuoft_ocrml.xml

"""
To find the maximum elements of the final_dword aka fwc 
import operator
max(fwc.iterkeys(), key=(lambda key:fwc[key]))

"""

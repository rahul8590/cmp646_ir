"""
The file is response for parsing xml and compiling statistics 
"""

#!/bin/python
import xml.etree.cElementTree as cxml
import re


"""
dict_word['word'] = [[(book_name,[page_nos]),
                      (book_name,page_no)],
                      count]
"""

dword = {}

def populate_dict(word):
  dword[word] = d.get(w,0) + 1 



#line is a simple string which can get junk characters
def sanitize_line(line):
   rx = re.compile('\W+') #Getting only alphanumeric letters first
   #rnos = re.compile('[0-9]')
   rline = rx.sub(' ',line).strip()
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
        for i in san_string.split(' '): #populating the dictionary of words
          populate_dict(i)

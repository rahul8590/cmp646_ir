"""
The file is response for parsing xml and compiling statistics 
"""

#!/bin/python

import xml.etree.cElementTree as cxml



"""
dict_word['word'] = [[(book_name,page_no),
                      (book_name,page_no)],
                      count]
"""


def parse_line(line):
  #Code to parse line returned from parse_xml 


def parse_xml(filename):
  for event,elem in cxml.iterparse(filename):
    if elem.tag == 'page':
      print elem.attrib
      for node in elem.findall('./region/section/line'):
        print node.text

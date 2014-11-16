#!/bin/python
import sys
import re 
import collections as c

#Relevance Calculator
def relcal(v):
  if v >= 2: return 'r'
  else: return 'n'



if __name__ == '__main__':
  fqrel = open(sys.argv[1],'r') #qrel sets
  fbt = open(sys.argv[2],'r')

  f3 = open('mod_robust_results_ordered.txt' , 'a')

  dram = c.OrderedDict() #stores books-title.tr100 as a result <qno , [docname(s)]>
  for i in fbt:
    i = re.sub(' +',' ',i)
    i = i.strip(' \n').split(' ')
    if dram.has_key(int(i[0])):
        rno = dram[int(i[0])]
        rno.append(i[2])
        dram[int(i[0])] = rno
    else:
      dram[int(i[0])] = [i[2]]

  print "length of dram is ", len(dram)

  dqrel = c.OrderedDict()
  for i in fqrel:
    i = re.sub(' +',' ',i)
    i = i.strip(' \n').split(' ')
    relv = int(i[2])
    if dqrel.has_key(int(i[0])):
      fnames = dqrel[int(i[0])]
      fnames[str(i[1])] = i[2]
      dqrel[int(i[0])] = fnames
    else:
      dqrel[int(i[0])] = {str(i[1]): i[2]}


  for query_no in dqrel:
    flist = dram[int(query_no)]
    drel = dqrel[int(query_no)]
    for fname in flist:
      if fname in drel.keys():
        f3.writelines(str(query_no)+" "+str(fname)+" "+str(drel[fname])+"\n")
      else:
        f3.writelines(str(query_no)+" "+str(fname)+" "+"0"+"\n")

  f3.close()
      

   


#!/bin/python
import sys
import re 


#Graph relevant imports
import pandas
import matplotlib.pyplot as plt
import numpy as np


def graph(label,yaxis=['q1','q2','q3', 'q4','q5',' q6'],xaxis=[3, 5, 2,3 ,5 , 2]):
  df = pandas.DataFrame(dict(graph=yaxis,
                           n=xaxis))
  ind = np.arange(len(df))
  width = 0.4
  opacity = 0.4
  fig, ax = plt.subplots()
  ax.barh(ind, df.n, width, alpha=opacity, color='b', label=label)
  ax.set(yticks=ind, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
  #ax.legend()
  plt.xlabel('Percentage of Relevant Document Retreived by Indri')
  plt.ylabel('Query Number')
  plt.title('Percentage Match of relevant doc')
  plt.show()


def abs_graph(qname,j20,i20):
  df = pandas.DataFrame(dict(graph=qname,
                           n=j20, m=i20))
  ind = np.arange(len(df))
  width = 0.4
  fig, ax = plt.subplots()
  ax.barh(ind, df.n, width, alpha=0.4,color='red', label='Qrel20')
  ax.barh(ind + width, df.m, width, alpha=0.4,color='green', label='Indri20')
  ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
  ax.set_xlim([0,20])
  ax.legend()
  plt.xlabel('No of Relevant Documents')
  plt.ylabel('Query No')
  plt.title('Absolute No of Relevant Documents Retrieved in Top20')
  plt.show()







#Relevance Calculator
def relcal(v):
  if v >= 2: return 'r'
  else: return 'n'

def cmplist(l1,l2):
  ans = set(l1) & set(l2)
  return ans

if __name__ == '__main__':
  f1 = open(sys.argv[1],'r') #qrel sets
  f2 = open(sys.argv[2],'r')

  dqrel = {}
  dqiter = {}
  #rno is the filename which is stored against query.
  
  for i in f1:
    i = re.sub(' +',' ',i)
    i = i.strip(' \n').split(' ')
    relv = int(i[2])
    dqiter[int(i[0])] = dqiter.get(int(i[0]),0) + 1

    if dqiter[int(i[0])] > 20:
      continue
    if relcal(relv) == 'n': continue #Uncomment if you only want relevant documents from comset.
    if dqrel.has_key(int(i[0])):
      rno = []
      rno = dqrel[int(i[0])]
      rno.append(i[1])
      dqrel[int(i[0])] = rno
    else:
      dqrel[int(i[0])] = [i[1]]

  dram = {}
  dramiter = {}
  for i in f2:
    i = re.sub(' +',' ',i)
    i = i.strip(' \n').split(' ')
    dramiter[int(i[0])] = dramiter.get(int(i[0]),0) + 1
    if dramiter[int(i[0])] > 20:
      continue
    if dram.has_key(int(i[0])):
        rno = dram[int(i[0])]
        rno.append(i[2])
        dram[int(i[0])] = rno
    else:
      dram[int(i[0])] = [i[2]]

  qkeys = dqrel.keys()
  print "queries in dqrel are " , qkeys
  pmatch = []
  qname =[] #name of the query
  j20 = []
  i20 = []
  for k in dqrel:
    print "the dqrel is ", dqrel[k] 
    #print "the dram is " , dram
    cmp5 = cmplist(dqrel[k],dram[k])
    print "Common results", k ,"=>" , len(cmp5) , "%match" , ((len(cmp5) + 0.0) / len(dqrel[k])) * 100
    #pmatch.append(((len(cmp5) + 0.0) / len(dqrel[k])) * 100)
    i20.append(len(cmp5))
    j20.append(len(dqrel[k]))
    qname.append('q'+str(k))

  #graph(sys.argv[1],qkeys,pmatch)
  abs_graph(qname,j20,i20)

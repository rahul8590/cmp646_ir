#!/bin/python
import sys
import re 
import math

#Relevance Calculator
def relcal(v):
  if v >= 2: return 'r'
  else: return 'n'

#Takes a list of numbers and calculates avg precesion for >=2 
def cal_avgp(l):
  avgp = 0.0
  count = 0.0 
  rcount = 0.0
  for i in l:
    count += 1
    if relcal(i) == 'r':
      rcount += 1
      avgp += rcount / count
  if rcount == 0: return 0.0
  return avgp/rcount

#def precesion@10
def p10(l):
  l10 = l[0:10]
  rcount = 0.0
  for i in l10:
    if relcal(i) == 'r':
      rcount += 1.0
  return rcount/10.0

#ndcg@20 
def ndcg20(l,sort='no'):
  #print "length is ",len(l)
  #Adding case if the length of the rereived documents is less than 20
  #I am padding those values with 0.
  if len(l) < 20:
    pad = 20 - len(l)
    for i in range(0,pad):
      l.append(0)

  if sort == 'sort':
    l = l[:20]
    l.sort(reverse=True)

  nval =  float(l[0]) + 0.0 #Initializing to r1 value
  for i in range(1,20):
      nval += l[i] / (math.log10(i+1.0) / math.log10(2.0) )
  return nval

#Calc MeanAvg Precesion
def mean_avg_prec(d):
  avgp = {}
  for k in d:
    avgp[k] = cal_avgp(d[k])
  print "the avg precsion is " , avgp
  
  meanavg = 0 
  for k in avgp:
    meanavg += avgp[k]
  meanavg /= len(avgp)
  print "mean avg precesion is " , meanavg


if __name__ == '__main__':  
  f = open(sys.argv[1] , 'r')
  d = {}
  for i in f:
    i = re.sub(' +',' ',i)
    i = i.strip(' \n').split(' ')
    #print i
    if d.has_key(int(i[0])):
      rno = []
      rno = d[int(i[0])]
      rno.append(int(i[2]))  #i[3] for robust04. else its i[2]
      d[int(i[0])] = rno
    else:
      d[int(i[0])] = [int(i[2])] #i[3] for robust04. else its i[2]

  print d 
  mean_avg_prec(d)

  print "precesion @ 10 is "
  for k in d:
    print k," =>" , p10(d[k])

  print "ndcg@20 is "
  for k in d:
    print k , "=>" , ndcg20(d[k],'sort')


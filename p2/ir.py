#!/bin/python
import sys
import re 

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
    i = i.strip(' ').split(' ')
    print i
    if d.has_key(int(i[0])):
      rno = []
      rno = d[int(i[0])]
      rno.append(int(i[2]))
      d[int(i[0])] = rno
    else:
      d[int(i[0])] = [int(i[2])]

  print d 
  mean_avg_prec(d)

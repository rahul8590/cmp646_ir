#!/bin/python
import sys
import re 

def relcal(v):
  if v >= 2: return 'r'
  else: return 'n'

#Takes a list of numbers and calculates avg precesion for >=2 
def cal_avgp(l):
  avgp = 0.0
  count = 1.0 
  rcount = 1.0
  for i in l:
    if relcal(i) == 'r':
      avgp += rcount / count
      rcount += 1
    count += 1
  return avgp/rcount




f = open(sys.argv[1] , 'r')
d = {}
for i in f:
  i = re.sub(' +',' ',i)
  i = i.strip(' ').split(' ')
  print i
  if d.has_key(int(i[0])):
    rno = d[int(i[0])]
    rno.append(int(i[2]))
  else:
    d[int(i[0])] = [int(i[2])]

print d 
avgp = {}

for k in d:
  avgp[k] = cal_avgp(d[k])

print "the avg precsion is " , avgp

meanavg = 0 
for k in avgp:
  meanavg += avgp[k]
meanavg /= len(avgp)

print "mean avg precesion is " , meanavg




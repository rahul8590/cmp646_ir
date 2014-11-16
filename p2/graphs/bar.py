import pandas
import matplotlib.pyplot as plt
import numpy as np

'''
df = pandas.DataFrame(dict(graph=['q1','q2','q3', 'q4','q5',' q6'],
                           n=[3, 5, 2,3 ,5 , 2])) 

'''
values = [[1,2,3],[2,20,2],[3,3,3]]
graph=['q1','q2','q3']

df = pandas.DataFrame( 
	#dict('q1' = [1,2,3], 'b' = [2,20,2],'c' = [3,3,3]),

	
	dict(graph=['q1','q2','q3', 'q4','q5',' q6'],
                           q1=[3, 5, 2,3 ,5 , 2])
	)
#plt.figure()
opacity = 0.4
'''

print len(df)
ind = np.arange(len(df))
width = 0.4

fig, ax = plt.subplots()



ax.barh(ind, df.n, width, alpha=opacity, color='b', label='Existing')
#ax.barh(ind + width, df.m, width, alpha=opacity,color='b', label='Community')
#ax.barh(ind + 2*width, df.o, width, alpha=opacity,color='g', label='Robust')
ax.set(yticks=ind, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
ax.legend()


plt.xlabel('Queries')
plt.xlabel('Precesion')
plt.title('Precesion for these  queries')

'''
ax = df.set_index(graph).plot(kind='barh',color= ['r','g', 'b'],alpha=opacity,title='Precesion queries values')
ax.set_xlabel("x axis")
ax.set_ylabel("query numbers")


plt.show()

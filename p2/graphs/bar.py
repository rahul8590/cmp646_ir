import pandas
import matplotlib.pyplot as plt
import numpy as np

df = pandas.DataFrame(dict(graph=['q1','q2','q3' , 'q4','q5',' q6'],
                           n=[3, 5, 2,3 ,5 , 2], m=[6, 1, 3, 6 , 1 , 3])) 

ind = np.arange(len(df))
width = 0.4
opacity = 0.4
fig, ax = plt.subplots()


ax.barh(ind, df.n, width, alpha=opacity, color='r', label='Existing')
ax.barh(ind + width, df.m, width, alpha=opacity,color='b', label='Community')

ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
ax.legend()



#plt.xlabel('Queries')
plt.xlabel('Precesion')
plt.title('Precesion for these  queries')

plt.show()
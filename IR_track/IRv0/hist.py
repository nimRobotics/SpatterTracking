import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

x = [6, 4, 7, 5, 6, 5, 2, 4, 2, 4, 6, 4, 6, 4, 3, 4, 5, 6, 5, 4, 2, 6, 2, 4, 3, 6, 7, 5, 6, 4, 5, 2, 4, 8, 2, 6, 3, 2, 5, 4, 6, 4, 2, 5, 6, 2, 4, 6, 2, 7, 5, 4, 5, 2, 3, 5, 6]
num_bins = 7
n, bins, patches = plt.hist(x, bins='auto', color='#0504aa',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Size (in pixels)')
plt.ylabel('Frequency')
plt.title('Size distribution using method 1')
plt.show()

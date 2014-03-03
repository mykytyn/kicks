import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

f = open('first_sim.txt', 'r')

total = eval(f.read())
print total
for a in total:
    plt.plot(a)


plt.savefig('first_sim.png')

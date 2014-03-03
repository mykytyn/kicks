import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

f = open('steps2.txt')

circles = []
steps = []
times = []
for line in f:
    c,s,t = line.split()
    circles.append(int(c))
    steps.append(float(s))
    times.append(float(t))
    print c
plt.plot(circles,steps,'+')
plt.savefig('steps_new.png')


from scipy import * 
from scipy import linalg 
import matplotlib.pyplot as plt 
import argparse 
import os
import time 

parser = argparse.ArgumentParser()
parser.add_argument("--N", default=10, type=int)
parser.add_argument("--dt", default=0.001, type=float)
parser.add_argument("--D", default=1.0, type=float)
parser.add_argument("--T", default=1.0, type=float)
parser.add_argument("--plot", default="False", type=str)
args = parser.parse_args()
t0 = time.process_time() 


def initial_condition(x):
  if abs(x-0.5) <= 0.1: return 1
  else: return 0

mesh = linspace(0, 1, args.N) 
u0 = [initial_condition(x) for x in mesh]
u_prev = u0.copy()
u = u0.copy()

t = 0 
h = 1/args.N
dt = args.dt 
N = args.N 
D = args.D

A = zeros([N,N])
for i,x in enumerate(mesh):  
  if i > 0 and i < args.N-1:
    A[i,i]    = 1+2*D*dt/(h**2)  
    A[i,i-1]  = -D*dt/(h**2) 
    A[i,i+1]  = -D*dt/(h**2) 

  if i == 0: 
    A[i,i] = 1+2*D*dt/(h**2)  
    A[i,i+1] = -2*D*dt/(h**2)   
  if i == args.N-1:
    A[i,i] =  1+2*D*dt/(h**2)  
    A[i,i-1] = -2*D*dt/(h**2)  


"""
# debug 
e, v  = linalg.eig(A)
e.sort()
print (e) 
"""


while t<args.T:   
    t += args.dt
    u_prev[:] = u[:]
    u[:] = linalg.solve(A, u_prev)

    print ("max value ", max(u), " time ", t)
    if args.plot == "True": plt.plot(u)


t1 = time.process_time() 
cpu_time = "%2.0e" % (t1 - t0) 

print ("Total simulation time ", cpu_time)

directory = "tmp_" + "N" + str(args.N) + "_dt" + str(args.dt) + "_D" + str(args.D) 
if not os.path.exists(directory):
    os.mkdir(directory)


if args.plot == "True": 
    plt.plot(u)
    plt.title(directory.replace("_", " ")  + "CPU time " + cpu_time)
    plt.savefig(directory + "/u_final.png")
    plt.show()



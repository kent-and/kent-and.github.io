
from scipy import * 
import matplotlib.pyplot as plt 
import argparse 
import os
import time 
from dolfin import * 

parser = argparse.ArgumentParser()
parser.add_argument("--N", default=10, type=int)
parser.add_argument("--dt", default=0.1, type=float)
parser.add_argument("--D", default=1.0, type=float)
parser.add_argument("--T", default=1.0, type=float)
parser.add_argument("--plot", default="False", type=str)
args = parser.parse_args()
t0 = time.process_time() 


class InitialCondition(UserExpression):
    def eval(self, v, x): 
        if abs(x[0]-0.5) <= 0.1: v[0] = 1  
        else: v[0] = 0 
#        print (x[0], v[0])

mesh = UnitIntervalMesh(args.N) 
V = FunctionSpace(mesh, "CG", 1) 
u = TrialFunction(V) 
v = TestFunction(V) 

U = Function(V)
U0 = project(InitialCondition(), V) 
U_prev = Function(V) 
U_prev.vector()[:] = U0.vector()[:]
D = Constant(args.D)
dt = Constant(args.dt)


if args.plot == "True": plt.plot(U_prev.vector()[:])



t = 0 
h = 1/args.N
while t<args.T:   
    t += args.dt

    a = u*v*dx + dt*D*inner(grad(u), grad(v))*dx 
    L = U_prev*v*dx 

    solve(a == L, U) 
    print ("max value ", max(U.vector()[:]), " time ", t)
    U_prev.vector()[:] = U.vector()[:]

    if args.plot == "True": 
        plt.plot(U.vector()[:])


t1 = time.process_time() 
cpu_time = "%2.0e" % (t1 - t0) 

print ("Total simulation time ", cpu_time)

directory = "tmp_" + "N" + str(args.N) + "_dt" + str(args.dt) + "_D" + str(args.D) 
if not os.path.exists(directory):
    os.mkdir(directory)


if args.plot == "True": 
    plt.plot(U.vector()[:])
    plt.title(directory.replace("_", " ")  + "CPU time " + cpu_time)
    plt.savefig(directory + "/u_final.png")
    plt.show()



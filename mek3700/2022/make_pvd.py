
from dolfin import * 
import argparse 
parser = argparse.ArgumentParser()
parser.add_argument("--meshfile", type=str, default="Mesh8.h5")
args = parser.parse_args()


mesh = Mesh()
hdf = HDF5File(mesh.mpi_comm(), args.meshfile, "r")
hdf.read(mesh, "/mesh", False)  

print (args.meshfile[:-2]+"pvd")
f = File(args.meshfile[:-2]+"pvd")
f << mesh 





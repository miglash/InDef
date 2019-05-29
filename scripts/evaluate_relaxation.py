#A script that compares two atomic geometries with each other to evaluate how 
#big the overall changes are
import math
import numpy as np

#Parse a POSCAR file
def parsePoscar(data_file):

    f = open(str(data_file),'r')
    poscar_data = f.read().split('\n')
    f.close()

    #Contains the scaling factor
    scale=float(poscar_data[1])

    #Contains the lattice
    lattice=[]
    temp=poscar_data[2].split()
    lattice.append([float(temp[0]),float(temp[1]),float(temp[2])])
    temp=poscar_data[3].split()
    lattice.append([float(temp[0]),float(temp[1]),float(temp[2])])
    temp=poscar_data[4].split()
    lattice.append([float(temp[0]),float(temp[1]),float(temp[2])])

    #Contains composition
    comp={}
    atoms=poscar_data[5].split()
    nat=poscar_data[6].split()
    ntotal=0
    for itype in range(0,len(temp)):
        comp[atoms[itype]]=int(nat[itype])
        ntotal=ntotal+int(nat[itype])

    #Contains coordinate type
    coordtype=poscar_data[7].split()
    if (coordtype[0] != "Direct" and coordtype[0] != "direct"):
        print("Warning: Coordinate type not recognized, but should not cause an error")

    #Contains the atomic coordinates
    coord=[]
    for iline in range(8,8+ntotal):
        temp=poscar_data[iline].split()
        coord.append([float(temp[0]),float(temp[1]),float(temp[2])])    

    structure = {}
    structure["natoms"]=ntotal
    structure["comp"]=comp
    structure["scale"]=scale
    structure["lattice"]=lattice
    structure["coord"]=coord
    return structure

def compareStruct(structure1,structure2):
    
    #Compare the compositions
    if (structure1["comp"] != structure2["comp"]):
       print("The compositions are not the same: NOT IMPLEMENTED YET")
       sys.exit()

    #Compare the lattices
    for ilat in range(0,2):
        for jlat in range(0,2):
            a1=structure1["scale"]*structure1["lattice"][ilat][jlat]
            a2=structure2["scale"]*structure2["lattice"][ilat][jlat]
            if (a1 != a2):
               print("Warning: The lattices of the two structures are not the same?")
               print("Are you sure you know what you are using this code for?")
               sys.exit()

    lat=np.array(structure1["lattice"])
    lat=lat*structure1["scale"]

    #Finally, compare the geometries
    ntotal = structure1["natoms"]
    minmoved = lat.max()
    maxmoved = 0.0

    for iat in range(0,ntotal):

        vec1=np.array(structure1["coord"][iat])
        vec2=np.array(structure2["coord"][iat])

        #This is a kind of shitty way to compare over the periodic boundary
        for ix in range(0,2):
            if abs(vec1[ix]-vec2[ix]) > 0.5:
               if vec1[ix] > 0.5:
                  vec1[ix] = vec1[ix] - 1
               else:
                  vec2[ix] = vec2[ix] - 1

        vec1=np.dot(lat,vec1)
        vec2=np.dot(lat,vec2)

        dist=0.0
        for ix in range(0,2):
            dist=dist+(vec1[ix]-vec2[ix])**2
        dist=math.sqrt(dist)

        #Keep track of the furthest moved and the least moved distances
        if (dist < minmoved):
           minmoved = dist
        if (dist > maxmoved):
           maxmoved = dist

        #Not really interested in things that didnt move
        if ( dist > 0.05):
           print("%3i   %5.3f"% (iat+1, dist))

    print("The min amount of movement: %6.4f; max amount: %6.4f in AA"% (minmoved,maxmoved))

file1="CONTCAR-q0"
file2="CONTCAR-q1"
file3="POSCAR_init-q1"
file4="POSCAR_init-q0"

structure1 = parsePoscar(file1)
structure2 = parsePoscar(file4)

compareStruct(structure1,structure2)

structure1 = parsePoscar(file3)
structure2 = parsePoscar(file4)

compareStruct(structure1,structure2)

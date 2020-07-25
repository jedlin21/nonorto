nNode = 51
mNode = 321
xLength = 2
yLength= 0.3
minusXLength = 0.05
symmetryPoints = 25
import numpy as np

mesh = list()
mesh.append("NDIME= 2")
mesh.append(f"NELEM= {(nNode - 1) * (mNode - 1)}")
i = 0
for x in range(nNode-1):
    for y in range(mNode-1):
        mesh.append(f"9\t{y+x*mNode}\t{y+x*mNode+1}\t{y+(x+1)*mNode+1}\t{y+(x+1)*mNode}\t{i}")
        i += 1

with open("converted/cgns.su2") as f:
    su2 = f.readlines()

newSu2 = list()
for a in su2[32003:64424]:
    _, x, y, i = a.split("\t")
    x, y, i = (float(x), float(y), int(i))
    newSu2.append([x,y])
newSu2 = np.array(sorted(newSu2, key=lambda x: (x[0], -x[1])))
x = newSu2[::321][:,0][::2]
y = newSu2[:321][:,1]
nNode = len(x)
#len(y[::321][:,0][y[::321][:,0]<0.03])
#len(y[::321][:,0][y[::321][:,0]>0.1])

# mesh.append(f"NPOIN= {nNode*mNode}")
# i = 0
# for x in range(nNode):
#     for y in range(mNode-1, -1, -1):
#         xCoord = x/(nNode-1) * (xLength+minusXLength) - minusXLength
#         yCoord = y/(mNode-1) * yLength
#         mesh.append(f"{xCoord}\t{yCoord}\t{i}")
#         i += 1

mesh.append(f"NPOIN= {nNode*mNode}")
i = 0
for column in range(nNode):
    for row in range(mNode):
        mesh.append(f"{x[column]}\t{y[row]}\t{i}")
        i+=1


mesh.append("NMARK= 5")
mesh.append("MARKER_TAG= farfield")
mesh.append(f"MARKER_ELEMS= {nNode-1}")
for x in range(0,nNode*mNode-mNode,mNode):
    mesh.append(f"3\t{x+mNode}\t{x}")

mesh.append("MARKER_TAG= inlet")
mesh.append(f"MARKER_ELEMS= {mNode-1}")
for x in range(mNode-1):
    mesh.append(f"3\t{x}\t{x+1}")

mesh.append("MARKER_TAG= outlet")
mesh.append(f"MARKER_ELEMS= {mNode-1}")
for x in range((nNode-1)*(mNode),nNode*mNode-1):
    mesh.append(f"3\t{x+1}\t{x}")

mesh.append("MARKER_TAG= symmetry")
mesh.append(f"MARKER_ELEMS= {symmetryPoints}")
for x in range(mNode-1,symmetryPoints*mNode,mNode):
    mesh.append(f"3\t{x}\t{x+mNode}")

mesh.append("MARKER_TAG= wall")
mesh.append(f"MARKER_ELEMS= {nNode - symmetryPoints - 1}")
for x in range((symmetryPoints+1)*mNode-1,nNode*mNode-1,mNode):
    mesh.append(f"3\t{x}\t{x+mNode}")    


with open('su2_original/mesh.su2', "w") as f:
    f.write("\n".join(mesh))

y_coef = 0.3
xOffset = 20
yOffset = 10



nNode = 65
mNode = 65
xLength = 0.3048
yLength= 0.03
NPOIN= 4225
NodeCoordinatesLine = 4099

with open("su2_original/mesh_flatplate_65x65.su2") as f:
    su2 = f.readlines()

xZero = float(su2[NodeCoordinatesLine +  64 * (64-xOffset)].split("\t")[0])
print(xZero)

xyz = True
for index in range(NodeCoordinatesLine, NPOIN+NodeCoordinatesLine-1):
    x, y, i = su2[index].split("\t")
    x, y, i = (float(x), float(y), int(i))

    _, y_next, _ = su2[index+1].split("\t")
    y_next =  float(y_next)

    if i // 65 < (65 - xOffset): # Do not change
        continue

    #xNode = (i ) // nNode # 60/64
    #yNode = i % mNode

    #xCoord = float(xNode)/float(nNode-1)
    #yCoord = float(yNode)/float(mNode-1)
    #xCoord_new =  xLength * xCoord 
    #                  (50    -    (65  -  20) / 20 (5/20) *    
    #xCoord_new = xZero + ( (i//65 - ( nNode - xOffset )) / xOffset) * (0.3048 - xZero)
    #yCoord_new =  yLength * yCoord  

    if i % 65 < (65 - yOffset) or i % 65 == 64:
        continue
 # ToDo: odejmij co drugi
    if xyz:
        xyz = False
        yCoord_new = y + y_coef * (y - y_next)
    else:
        xyz = True
        yCoord_new = y - y_coef * (y - y_next)

    #print(f"{i} {y} {yCoord_new} {y_next}")


    su2[index] = ("%15.14f \t %15.14f \t %s\n" % (x, yCoord_new, i))

with open("su2_modified/mesh_flatplate_65x65.su2", "w") as f:
    f.write("".join(su2))



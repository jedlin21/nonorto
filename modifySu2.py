import numpy as np

y_coef = 0.3
xOffset = 44
yOffset = 2

nNode = 65
mNode = 65
xLength = 0.3048
yLength= 0.03
NPOIN= 4225
NodeCoordinatesLine = 4099

with open("su2_original/mesh_flatplate_65x65.su2") as f:
    su2 = f.readlines()

xZero = float(su2[NodeCoordinatesLine +  65 * (65-xOffset) - 1].split("\t")[0])
yZero = float(su2[NodeCoordinatesLine +  65 * (65-xOffset) - 1].split("\t")[1])
iZero = float(su2[NodeCoordinatesLine +  65 * (65-xOffset) - 1].split("\t")[2])
print(xZero)
print(iZero)
print(yZero)

xyz = True
for index in range(NodeCoordinatesLine+65, NPOIN+NodeCoordinatesLine-1 - 65): # TODO: -1 -65??????? check it
    x_top_left, y_top_left, i_top_left = su2[index-1].split("\t")
    x_top_left, y_top_left, i_top_left = (float(x_top_left), float(y_top_left), int(i_top_left))
    
    x_middle_left, y_middle_left, i_middle_left = su2[index].split("\t")
    x_middle_left, y_middle_left, i_middle_left = (float(x_middle_left), float(y_middle_left), int(i_middle_left))

    x_bottom_left, y_bottom_left, i_bottom_left = su2[index+1].split("\t")
    x_bottom_left, y_bottom_left, i_bottom_left = (float(x_bottom_left), float(y_bottom_left), int(i_bottom_left))

    hop = 65

    x_top_right, y_top_right, i_top_right = su2[index-1 + hop].split("\t")
    x_top_right, y_top_right, i_top_right = (float(x_top_right), float(y_top_right), int(i_top_right))
    
    x_middle_right, y_middle_right, i_middle_right = su2[index + hop].split("\t")
    x_middle_right, y_middle_right, i_middle_right = (float(x_middle_right), float(y_middle_right), int(i_middle_right))

    x_bottom_right, y_bottom_right, i_bottom_right = su2[index+1 + hop].split("\t")
    x_bottom_right, y_bottom_right, i_bottom_right = (float(x_bottom_right), float(y_bottom_right), int(i_bottom_right))

    

    if i_middle_left // 65 < (65 - xOffset-1): # Do not change
        continue

    if i_middle_left % 65 < (65 - yOffset) or i_middle_left % 65 == 64:
        continue


    # Calc deltaY
    deltaY = 0
    # x_middle_left  B8
    # x_middle_right B9
    # y_middle_left  C8 
    # y_middle_right C9
    # y_top_left     D8
    # D9 
    # deltaY         E9  

    ys1 = ((1/2)*y_middle_left*y_middle_left+((1/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
    xs1 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*y_middle_left+((2/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
    ys2 =(((1/2)*(y_top_left-y_middle_right)+y_middle_left+deltaY)*(y_top_left-y_middle_right)+((2/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)
    xs2 =(((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*(y_top_left-y_middle_right)+((1/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)

    katDo90 = np.arctan((xs1-xs2)/(ys2-ys1)) * 180 / np.pi
    katPochKomorki = np.arctan((y_middle_right-y_middle_left)/(x_middle_right-x_middle_left)) * 180 / np.pi



    deltaY = y_coef * (y_middle_left - y_bottom_left)


    if xyz:
        xyz = False
        yCoord_new = y_middle_left + deltaY
    else:
        xyz = True
        yCoord_new = y_middle_left - deltaY

    #print(f"{i} {y} {yCoord_new} {y_bottom_left}")
    print(index)
    print(i_bottom_left)
    print(f"x_top_left: {x_top_left};\ty_top_left: {y_top_left}")
    print(f"x_middle_left: {x_middle_left};\ty_middle_left: {y_middle_left}")
    print(f"x_bottom_left: {x_bottom_left};\ty_bottom_left: {y_bottom_left}")
    print(f"x_top_right: {x_top_right};\ty_top_right: {y_top_right}")
    print(f"x_middle_right: {x_middle_right};\ty_middle_right: {y_middle_right}")
    print(f"x_bottom_right: {x_bottom_right};\ty_bottom_right: {y_bottom_right}")
    print("\n")


    su2[index] = ("%15.14f \t %15.14f \t %s\n" % (x_middle_left, yCoord_new, i_middle_left))

with open("su2_modified/mesh_flatplate_65x65.su2", "w") as f:
    f.write("".join(su2))


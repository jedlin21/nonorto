target = 77 # 80ok
target_cos = 0.4
epsilon = 4
#kappa = 0.000000000001
kappa = 0.000000001
#xOffset = 44 # X==0
xOffset = 10
yOffset = 1000
mode = "experiment" # "default", "constant", "experiment", "fsolve"
A = 1.721 # constant 0.664, 1.721, 5.0

#mode = "constant"
maxC=0.000016064370512998453
yConstant = maxC * 0.9

import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import minimize
from math import copysign


def func_v1(deltaY, data, target):
    # data = args[0]
    # data = args[1]
    y_top_left = data["y_top_left"]
    x_middle_left = data["x_middle_left"]
    y_middle_left = data["y_middle_left"]
    x_middle_right = data["x_middle_right"]
    y_middle_right = data["y_middle_right"]

    ys1 = ((1/2)*y_middle_left*y_middle_left+((1/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
    xs1 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*y_middle_left+((2/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
    ys2 = (((1/2)*(y_top_left-y_middle_right)+y_middle_left+deltaY)*(y_top_left-y_middle_right)+((2/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)
    xs2 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*(y_top_left-y_middle_right)+((1/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)

    katDo90 = np.arctan((xs1-xs2)/(ys2-ys1)) * 180 / np.pi
    katPochKomorki = np.arctan((y_middle_right-y_middle_left)/(x_middle_right-x_middle_left)) * 180 / np.pi

    nonOrto = katDo90 - katPochKomorki

    yCoord_new = y_middle_left + deltaY
    if yCoord_new > y_top_right  or y_bottom_right > yCoord_new:
        return 10^9
    else:
        return nonOrto - target


def func_v2(deltaY, data, target):
    # data = args[0]
    # data = args[1]
    y_top_left = data["y_top_left"]
    x_middle_left = data["x_middle_left"]
    y_middle_left = data["y_middle_left"]
    x_middle_right = data["x_middle_right"]
    y_middle_right = data["y_middle_right"]

    yCoord_new = y_middle_left + deltaY

    ys1 = ((1/2)*y_middle_left*y_middle_left+((1/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
    xs1 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*y_middle_left+((2/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
    ys2 = (((1/2)*(y_top_left-yCoord_new)+y_middle_left+deltaY)*(y_top_left-yCoord_new)+((2/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_top_left-yCoord_new+(1/2)*deltaY)
    xs2 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*(y_top_left-yCoord_new)+((1/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_top_left-yCoord_new+(1/2)*deltaY)

    a1 = deltaY/(x_middle_right-x_middle_left)
    b1 = yCoord_new-a1*x_middle_right
    try:
        a2 = (ys1-ys2)/(xs1-xs2)
    except:
        print(xs1)
        print(xs2)
        pass    
    b2 = ys1-a2*xs1 
    
    srodekX = (b2-b1)/(a1-a2)
    srodekY = a1*srodekX+b1
    normalizacja = np.sqrt((x_middle_right-srodekX)**2+(yCoord_new-srodekY)**2)*np.sqrt((ys1-srodekY)**2+(xs1-srodekX)**2)
    
    cosBeta = (-(x_middle_right-srodekX)*(ys1-srodekY)+(yCoord_new-srodekY)*(xs1-srodekX))/normalizacja
    nonOrto = np.arccos(cosBeta) * 180 / np.pi

    x = (x_middle_right-srodekX)*(xs1-srodekX) + (y_middle_right-srodekY)*(ys1-srodekY)
    nonOrto *= copysign(1, x) 

    if yCoord_new > y_top_right  or y_bottom_right > yCoord_new:
        return 10^9
    else:
        return nonOrto - target

nNode = 51
mNode = 321
hop = 321
xLength = 0.3048
yLength= 0.03
NPOIN= nNode*mNode
NodeCoordinatesLine = (nNode-1)*(mNode-1) + 3

with open("su2_original/mesh.su2") as f:
    su2 = f.readlines()


xZero = float(su2[NodeCoordinatesLine +  mNode * (nNode-xOffset) - 1].split("\t")[0])
yZero = float(su2[NodeCoordinatesLine +  mNode * (nNode-xOffset) - 1].split("\t")[1])
iZero = float(su2[NodeCoordinatesLine +  mNode * (nNode-xOffset) - 1].split("\t")[2])
print(xZero)
print(iZero)
print(yZero)

flag = True
for index in range(NodeCoordinatesLine+mNode, NPOIN+NodeCoordinatesLine-1 - mNode): 
    x_top_left, y_top_left, i_top_left = su2[index-1].split("\t")
    x_top_left, y_top_left, i_top_left = (float(x_top_left), float(y_top_left), int(i_top_left))
    
    x_middle_left, y_middle_left, i_middle_left = su2[index].split("\t")
    x_middle_left, y_middle_left, i_middle_left = (float(x_middle_left), float(y_middle_left), int(i_middle_left))

    x_bottom_left, y_bottom_left, i_bottom_left = su2[index+1].split("\t")
    x_bottom_left, y_bottom_left, i_bottom_left = (float(x_bottom_left), float(y_bottom_left), int(i_bottom_left))

    
    
    x_top_right, y_top_right, i_top_right = su2[index-1 + hop].split("\t")
    x_top_right, y_top_right, i_top_right = (float(x_top_right), float(y_top_right), int(i_top_right))
    
    x_middle_right, y_middle_right, i_middle_right = su2[index + hop].split("\t")
    x_middle_right, y_middle_right, i_middle_right = (float(x_middle_right), float(y_middle_right), int(i_middle_right))

    x_bottom_right, y_bottom_right, i_bottom_right = su2[index+1 + hop].split("\t")
    x_bottom_right, y_bottom_right, i_bottom_right = (float(x_bottom_right), float(y_bottom_right), int(i_bottom_right))

    if i_middle_left // mNode < (nNode - xOffset-1):
        continue

    if i_middle_left % mNode < (mNode - yOffset) or i_middle_left % mNode == mNode-1:
        continue

    if i_middle_left % mNode % 2 == 0:
        continue

    

    y_node = y_top_left
    x_node = x_bottom_left
    # print(x_node)
    # print(f"{y_node}   ?=   {A * 4.572 * np.e ** (-4) * np.sqrt(x_node)}")
    if y_node > A * 4.572 * 10 ** (-4) * np.sqrt(x_node):
        continue
    data = dict()
    data["y_top_left"] = y_top_left 
    data["x_middle_left"] = x_middle_left 
    data["y_middle_left"] = y_middle_left 
    data["x_middle_right"] = x_middle_right 
    data["y_middle_right"] = y_middle_right
    # Calc deltaY
    # x_middle_left  B8
    # x_middle_right B9
    # y_middle_left  C8 
    # y_middle_right C9
    # y_top_left     D8
    # D9 
    # deltaY         E9  

    if mode == "constant":

        if flag:
            deltaY = yConstant
        else:
            deltaY = -yConstant
    
        ys1 = ((1/2)*y_middle_left*y_middle_left+((1/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
        xs1 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*y_middle_left+((2/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
        ys2 = (((1/2)*(y_top_left-y_middle_right)+y_middle_left+deltaY)*(y_top_left-y_middle_right)+((2/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)
        xs2 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*(y_top_left-y_middle_right)+((1/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)

        katDo90 = np.arctan((xs1-xs2)/(ys2-ys1)) * 180 / np.pi
        katPochKomorki = np.arctan((y_middle_right-y_middle_left)/(x_middle_right-x_middle_left)) * 180 / np.pi

        nonOrto = katDo90 - katPochKomorki
    elif mode == "experiment":
        if flag:
            deltaY = y_top_left - y_middle_left - kappa
        else:
            deltaY = y_bottom_left - y_middle_left + kappa
       # print(f"check: {y_middle_left + deltaY}")
        
        nonOrto = 0
        startOrto = 0
        cosBeta = 0
        # while not np.isclose(target_cos, np.abs(cosBeta), atol=epsilon):
        start = True
        while not np.isclose(target, np.abs(nonOrto), atol=epsilon):
            if flag:
                deltaY -= kappa
            else:
                deltaY += kappa
            yCoord_new = y_middle_left + deltaY
            
            # x_middle_left  B8
            # x_middle_right B9
            # y_middle_left  C8 
            # y_middle_right C9 -- yCoord_new
            # deltaY         E9
            # 
            # ys1            F8
            # xs1            G8   
            # ys2            H8   
            # xs2            I8   
            # a1             N8
            # b1             O8
            # a2             P8
            # b2             Q8
            # ys2            H8
            # srodekX        R8
            # srodekY        S8
            # normalizacja   T8
            # cosBeta        U8

            ys1 = ((1/2)*y_middle_left*y_middle_left+((1/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
            xs1 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*y_middle_left+((2/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
            ys2 = (((1/2)*(y_top_left-yCoord_new)+y_middle_left+deltaY)*(y_top_left-yCoord_new)+((2/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_top_left-yCoord_new+(1/2)*deltaY)
            xs2 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*(y_top_left-yCoord_new)+((1/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_top_left-yCoord_new+(1/2)*deltaY)

            # katDo90 = np.arctan((xs1-xs2)/(ys2-ys1)) * 180 / np.pi
            # katPochKomorki = np.arctan((yCoord_new-y_middle_left)/(x_middle_right-x_middle_left)) * 180 / np.pi
            # nonOrto = katDo90 - katPochKomorki
            
            
            a1 = deltaY/(x_middle_right-x_middle_left)
            b1 = yCoord_new-a1*x_middle_right
            try:
                a2 = (ys1-ys2)/(xs1-xs2)
            except:
                print(xs1)
                print(xs2)
                print(nonOrto)
                continue
                
            b2 = ys1-a2*xs1 

            
            srodekX = (b2-b1)/(a1-a2)
            srodekY = a1*srodekX+b1
            normalizacja = np.sqrt((x_middle_right-srodekX)**2+(yCoord_new-srodekY)**2)*np.sqrt((ys1-srodekY)**2+(xs1-srodekX)**2)
            
            cosBeta = (-(x_middle_right-srodekX)*(ys1-srodekY)+(yCoord_new-srodekY)*(xs1-srodekX))/normalizacja
            nonOrto = np.arccos(cosBeta) * 180 / np.pi
            if start:
                start = False
                startOrto = nonOrto
        # print(f"nonOrto {nonOrto} newCoord: {y_middle_left + deltaY}  y_top_right: {y_top_right}" )
           # print(f"nonOrto {nonOrto}" )
            
            if(y_middle_left + deltaY > y_top_right or y_middle_left + deltaY < 0):
                if flag:
                    deltaY = y_bottom_left - y_middle_left + kappa
                else:
                    deltaY = y_top_left - y_middle_left - kappa
                print("Motyla noga")
                ys1 = ((1/2)*y_middle_left*y_middle_left+((1/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
                xs1 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*y_middle_left+((2/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
                ys2 = (((1/2)*(y_top_left-y_middle_right)+y_middle_left+deltaY)*(y_top_left-y_middle_right)+((2/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)
                xs2 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*(y_top_left-y_middle_right)+((1/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)

                katDo90 = np.arctan((xs1-xs2)/(ys2-ys1)) * 180 / np.pi
                katPochKomorki = np.arctan((y_middle_right-y_middle_left)/(x_middle_right-x_middle_left)) * 180 / np.pi

                nonOrto = katDo90 - katPochKomorki
                print(f"nonOrto {nonOrto}" )
                print(f"startOrto {startOrto}" )
                break
    elif mode == "fsolve":
        if flag:
            deltaY = y_top_left - y_middle_left - 0.000001    
            target = -target 
        else:
            deltaY = y_bottom_left - y_middle_left + 0.000001
            target = -target 
        
        deltaY, full_output, flag, msg = fsolve(func_v2, 0, (data, target), full_output=True)
        if(flag != 1):
            print("Motyla noga")
            print(msg)
            print(full_output)
            break
        #bnds = ((0, None),)
        #result = minimize(func_v1, (0), args=(data, target), method='SLSQP', bounds=bnds)
        #deltaY = result.x

        yCoord_new = y_middle_left + deltaY

        ys1 = ((1/2)*y_middle_left*y_middle_left+((1/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
        xs1 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*y_middle_left+((2/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
        ys2 = (((1/2)*(y_top_left-y_middle_right)+y_middle_left+deltaY)*(y_top_left-y_middle_right)+((2/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)
        xs2 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*(y_top_left-y_middle_right)+((1/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)

        srodekX = x_middle_left+0.5*(x_middle_right-x_middle_left)
        srodekY = y_middle_left+0.5*(yCoord_new-y_middle_left)
        normalizacja = np.sqrt((x_middle_right-srodekX)**2+(y_middle_right-srodekY)**2)*np.sqrt((ys1-srodekY)**2+(xs1-srodekX)**2)
        cosBeta = (-(x_middle_right-srodekX)*(ys1-srodekY)+(y_middle_right-srodekY)*(xs1-srodekX))/normalizacja
        nonOrto = np.arccos(cosBeta) * 180 / np.pi
        
        x = (x_middle_right-srodekX)*(xs1-srodekX) + (y_middle_right-srodekY)*(ys1-srodekY)
        nonOrto *= copysign(1, x) 
    else:
        deltaY = 0
        nonOrto = 0
        while not np.isclose(target, np.abs(nonOrto), atol=epsilon) or not np.abs(nonOrto) > target:
            ys1 = ((1/2)*y_middle_left*y_middle_left+((1/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
            xs1 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*y_middle_left+((2/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
            ys2 = (((1/2)*(y_top_left-y_middle_right)+y_middle_left+deltaY)*(y_top_left-y_middle_right)+((2/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)
            xs2 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*(y_top_left-y_middle_right)+((1/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)

            katDo90 = np.arctan((xs1-xs2)/(ys2-ys1)) * 180 / np.pi
            katPochKomorki = np.arctan((y_middle_right-y_middle_left)/(x_middle_right-x_middle_left)) * 180 / np.pi

            nonOrto = katDo90 - katPochKomorki

            if flag:
                deltaY += kappa
            else:
                deltaY -= kappa
            
        # print(f"nonOrto {nonOrto} newCoord: {y_middle_left + deltaY}  y_top_right: {y_top_right}" )
            #print(f"nonOrto {nonOrto}" )
            if(y_middle_left + deltaY > y_top_right or y_middle_left + deltaY < 0):
                print("Motyla noga")
    

    if mode == "constant":
        yCoord_new = y_middle_right + deltaY
    else:
        yCoord_new = y_middle_left + deltaY
    
    if flag:
        flag = False
    else:
        flag = True

    #print(f"{i} {y} {yCoord_new} {y_bottom_left}")
    #print(index)
    # print(i_bottom_left)
    print(f"{x_top_left};{y_middle_left};{y_top_left};non:{nonOrto}; start:{startOrto}")
    # print(f"x_top_left: {x_top_left};\ty_top_left: {y_top_left}")
    # print(f"x_middle_left: {x_middle_left};\ty_middle_left: {y_middle_left}")
    # print(f"x_bottom_left: {x_bottom_left};\ty_bottom_left: {y_bottom_left}")
    # print(f"x_top_right: {x_top_right};\ty_top_right: {y_top_right}")
    # print(f"x_middle_right: {x_middle_right};\ty_middle_right: {y_middle_right}")
    # print(f"x_bottom_right: {x_bottom_right};\ty_bottom_right: {y_bottom_right}")
    # print(f"deltaY: {deltaY} yCoord_new: {yCoord_new} nonOrto: {nonOrto} cosBeta: {cosBeta}")
    # print(f"{x_middle_left};{y_middle_left};{yCoord_new};{y_top_left};{deltaY};{ys1};{xs1};{ys2};{xs2};;;{srodekX};{srodekY};{normalizacja};{cosBeta};{nonOrto}")
    # print("\n")

    if yCoord_new > y_top_right  or y_bottom_right > yCoord_new:
    #if not y_bottom_right > yCoord_new > y_top_right:
        print("newCoord outside bounds")
        break
    su2[index + hop] = ("%.16e \t %.16e \t %s\n" % (x_middle_right, yCoord_new, i_middle_right))

with open("su2_original/mesh80.su2", "w") as f:
    f.write("".join(su2))


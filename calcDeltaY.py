import numpy as np

X = [0, 18, 28, 42, 60, 82, 108, 138, 172, 210, 252, 298, 348, 402, 460]
Y1_middle = [1, 1.1, 0.91, 1.04, 0.94,1.02,0.92,1.02,0.92,1.02,0.92,1.02,0.92,1.02,0.92]
Y2_top = [2.1,2.1,2.1,2.1,2.1,2.1,2.1,2.1,2.1,2.1,2.1,2.1,2.1,2.1,2.1]
deltaYT = [0.1,-0.19,0.13,-0.1,0.08,-0.1,0.1,-0.1,0.1,-0.1,0.1,-0.1,0.1,-0.1]

# x_middle_left  B8
# x_middle_right B9
# y_middle_left  C8 
# y_middle_right C9
# y_top_left     D8
# D9 
# deltaY         E9  

target = 14
epsilon = 0.01
kappa = 0.00001
flag = True
for index, (x_middle_left, x_middle_right, y_middle_right, y_top_left ) in enumerate(zip(X[:-1], X[1:], Y1_middle[1:], Y2_top[:-1])):
    y_middle_left = Y1_middle[index]
    deltaY = 0
    nonOrto = 0
    while target - np.abs(nonOrto) > epsilon or np.abs(nonOrto) > target:
        ys1 = ((1/2)*y_middle_left*y_middle_left+((1/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
        xs1 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*y_middle_left+((2/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_middle_left+(1/2)*deltaY)
        ys2 = (((1/2)*(y_top_left-y_middle_right)+y_middle_left+deltaY)*(y_top_left-y_middle_right)+((2/3)*deltaY+y_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)
        xs2 = (((1/2)*(x_middle_right-x_middle_left)+x_middle_left)*(y_top_left-y_middle_right)+((1/3)*(x_middle_right-x_middle_left)+x_middle_left)*(1/2)*deltaY)/(y_top_left-y_middle_right+(1/2)*deltaY)

        # katDo90 = np.arctan((xs1-xs2)/(ys2-ys1)) * 180 / np.pi
        # katPochKomorki = np.arctan((y_middle_right-y_middle_left)/(x_middle_right-x_middle_left)) * 180 / np.pi
        # nonOrto = katDo90 - katPochKomorki

        srodekX = x_middle_left+0.5*(x_middle_right-x_middle_left)
        srodekY = y_middle_left+0.5*(y_middle_right-y_middle_left)
        normalizacja = np.sqrt((x_middle_right-srodekX)**2+(y_middle_right-srodekY)**2)*np.sqrt((ys1-srodekY)**2+(xs1-srodekX)**2)
        cosBeta = (-(x_middle_right-srodekX)*(ys1-srodekY)+(y_middle_right-srodekY)*(xs1-srodekX))/normalizacja
        nonOrto = np.arccos(cosBeta) * 180 / np.pi


        if flag:
            deltaY += kappa
        else:
            deltaY -= kappa
    if flag:
        flag = False
    else:
        flag = True

    Y1_middle[index+1] = Y1_middle[index] + deltaY
    #print(Y1_middle)
    #print(y_middle_left, y_middle_right, deltaY)
    print(nonOrto, Y1_middle[index+1])

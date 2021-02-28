import math
import numpy as np
from numpy.linalg import inv
imageWidth = 704
imageHeight = 576
ncx = 752;
nfx = 704;
dx = 0.005770
dy = 0.006340
dpx = 0.006163
dpy = 0.006340

def head_feet_points(x1,y1,x2,y2,mask):
    y_new = y1
    while (y_new < y2):
        m = 0
        while (mask[y_new - 1][x1 + m - 1]) == False:
            m = m + 1
            if x1 + m == x2 - 1:
                break
        if (mask[y_new - 1][x1 + m - 1]) == True:
            break
        y_new = y_new + 1
    y_new_2 = y2

    while (y_new_2 > y1):
        m = 0
        while (mask[y_new_2 - 1][x1 + m - 1]) == False:
            m = m + 1
            if x1 + m == x2 - 1:
                break
        if (mask[y_new_2 - 1][x1 + m - 1]) == True:
            break
        y_new_2 = y_new_2 - 1

    head_point = [int((x1 + x2) / 2), y_new]
    feet_point = [int((x1 + x2) / 2), y_new_2]
    return head_point, feet_point

def height_calculation(head_point, feet_point,camera):
    head_point = head_point
    foot_point = feet_point
    variables(camera)
    undistortedHeadPoints = undistortion(head_point);
    undistortedFootPoints = undistortion(foot_point);
    undistortedFootPoints=np.hstack((undistortedFootPoints,1))
    undistortedFootPoints=np.asmatrix(undistortedFootPoints)
    undistortedFootPoints=undistortedFootPoints.transpose()
    H_1 = C[:,[0,1]]
    H_2 = C[:,[3]]
    H_Z0 = np.hstack((H_1, H_2))
    xyCoordinates = np.dot(inv(H_Z0),undistortedFootPoints)
    xyCoordinates = xyCoordinates/xyCoordinates[2,:]
    Xw = xyCoordinates[0,:]
    Yw = xyCoordinates[1,:]
    Xu = undistortedHeadPoints[0]
    Yu = undistortedHeadPoints[1]
    h1 = (np.dot(Xw,(C[1,0]-(Yu*C[2,0]))) +np.dot(Yw,(C[1,1]-(Yu*C[2,1])))+C[1,3]-(Yu*C[2,3]))
    h2=((Yu*C[2,2])-C[1,2])
    height=np.true_divide(h1,h2)
    height = height*100;
    height= np.squeeze(np.asarray(height))
    if camera==3:
        height=height-8
    if camera==4:
        height=height-14
    return height


def variables(camera):
    camera_no=camera
    global focal,kappa1,cx,cy,tx,ty,sx,tz,rx,ry,rz,Yf,C
    if camera_no==1:
        focal = 5.567576
        kappa1 = 0.003937
        cx = 351.767835
        cy = 290.330367
        sx = 0.892250
        tx = -1.011907
        ty = 6.822796
        tz = -0.219634
        rx = 2.219688
        ry = -0.216147
        rz = -0.046567
    elif camera_no==2:
        focal = 5.356039
        kappa1 = 0.001677
        cx = 361.882191
        cy = 294.794329
        sx = 0.867831
        tx = 8.425794
        ty = 13.847812
        tz = -10.422549
        rx = 2.247683
        ry = -0.526615
        rz = -0.275268
    elif camera_no==3:
        focal = 5.490531
        kappa1 = 0.006706
        cx = 332.726815
        cy = 309.031077
        sx = 0.896059
        tx = 8.502440
        ty = -19.391517
        tz = 36.330113
        rx = -2.185152
        ry = -0.176223
        rz = -3.109509
    elif camera_no==4:
        focal = 5.878339
        kappa1 = 0.001730
        cx = 347.788807
        cy = 291.294051
        sx = 0.888467
        tx = -34.102278
        ty = 16.026272
        tz = 0.767067
        rx = 2.806677
        ry = 0.714775
        rz = 0.881079
    elif camera_no==5:
        focal = 6.184144
        kappa1 = 0.004589
        cx = 355.250043
        cy = 297.764224
        sx = 0.795079
        tx = -13.367259
        ty = -9.173007
        tz = 20.063027
        rx = -2.476520
        ry = 0.635270
        rz = 2.507219
    else:
        focal = 5.780237
        kappa1 = 0.004382
        cx = 315.873465
        cy = 290.886565
        sx = 0.891318
        tx = 0.345240
        ty = -6.270184
        tz = 14.054230
        rx = -2.501424
        ry = 0.338429
        rz = 2.696578
    fx = focal / dpx
    fy = focal / dpy
    k=np.matrix([[focal, 0,0],[0,focal,0],[0,0,1]])
    R11 = math.cos(ry) * math.cos(rz)
    R12 = math.cos(rz) * math.sin(rx) * math.sin(ry) - math.cos(rx) * math.sin(rz)
    R13 = math.sin(rx) * math.sin(rz) + math.cos(rx) * math.cos(rz) * math.sin(ry)
    R21 = math.cos(ry) * math.sin(rz)
    R22 = math.sin(rx) * math.sin(ry) * math.sin(rz) + math.cos(rx) * math.cos(rz)
    R23 = math.cos(rx) * math.sin(ry) * math.sin(rz) - math.cos(rz) * math.sin(rx)
    R31 = -math.sin(ry)
    R32 = math.cos(ry) * math.sin(rx)
    R33 = math.cos(rx) * math.cos(ry)
    R=np.matrix([[R11,R12,R13,tx], [R21,R22,R23,ty], [R31,R32,R33,tz]])
    C = np.dot(k,R);


def undistortion(point):
    Xf=point[0]
    Yf=point[1]
    dx1 = dx * (ncx / nfx);
    Xd = (dx1 * (Xf -cx)) /sx
    Yd = (Yf-cy)*dy
    r = math.sqrt((Xd** 2)+(Yd**2))
    kr = 1 + ((kappa1)*(r** 2))
    Xu = Xd*kr;
    Yu = Yd*kr;
    return(Xu,Yu)


def main(x1,y1,x2,y2,mask,camera):
    head_point,feet_point = head_feet_points(x1,y1,x2,y2,mask)
    height =  height_calculation(head_point, feet_point, camera)
    return height
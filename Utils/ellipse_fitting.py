# -*- coding: utf-8 -*-
"""
Created on Fri May 27 14:20:27 2016

@author: Win7
"""

import numpy as np
from numpy.linalg import eig, inv

def fitEllipse(x,y):
    x = x[:,np.newaxis]
    y = y[:,np.newaxis]
    D =  np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
    S = np.dot(D.T,D)
    C = np.zeros([6,6])
    C[0,2] = C[2,0] = 2; C[1,1] = -1
    E, V =  eig(np.dot(inv(S), C))
    n = np.argmax(np.abs(E))
    a = V[:,n]
    return a

def ellipse_center(a):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    num = b*b-a*c
    x0=(c*d-b*f)/num
    y0=(a*f-b*d)/num
    return np.array([x0,y0])


def ellipse_angle_of_rotation( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    return 0.5*np.arctan(2*b/(a-c))


def ellipse_axis_length( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
    down1=(b*b-a*c)*( (c-a)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    down2=(b*b-a*c)*( (a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    res1=np.sqrt(up/down1)
    res2=np.sqrt(up/down2)
    return np.array([res1, res2])

def ellipse_angle_of_rotation2( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    if b == 0:
        if a > c:
            return 0
        else:
            return np.pi/2
    else: 
        if a > c:
            return np.arctan(2*b/(a-c))/2
        else:
            return np.pi/2 + np.arctan(2*b/(a-c))/2

if __name__ == '__main__':
    arc = 2
    R = np.arange(0,arc*np.pi, 0.01)
#    x = 1.*np.cos(R) + 2 + 0.1*np.random.rand(len(R))
#    y = 1.9*np.sin(R) + 1. + 0.1*np.random.rand(len(R))
#    theta0=0.3
#    I=x+1j*y
#    I_rot=np.abs(I)*(np.cos(np.angle(I)-theta0)+1j*np.sin(np.angle(I)-theta0))
#    x=I_rot.real
#    y=I_rot.imag
    x=I[:,200]
    y=Q[:,200]
    a = fitEllipse(x,y)
    center = ellipse_center(a)
    phi = ellipse_angle_of_rotation(a)
    
#    phi = ellipse_angle_of_rotation2(a)
    axes = ellipse_axis_length(a)
    if phi < 0:
        phi +=np.pi/2
        axes[0],axes[1]=axes[1],axes[0]
    
    print("center = ",  center)
    print("angle of rotation = ",  phi)
    print("axes = ", axes)
    
    a, b = axes
#    phi=phi-np.pi/2
    xx = center[0] + a*np.cos(R)*np.cos(phi) - b*np.sin(R)*np.sin(phi)
    yy = center[1] + a*np.cos(R)*np.sin(phi) + b*np.sin(R)*np.cos(phi)
#  
    #%%
    I_cal=x-center[0]+1j*(y-center[1])
    I_cal=np.abs(I_cal)*(np.cos(np.angle(I_cal)-phi)+1j*np.sin(np.angle(I_cal)-phi))
    I_cal=I_cal.real+1j*I_cal.imag/axes[1]*axes[0]
    from pylab import *
    fig,ax=subplots()
    l1,=ax.plot(x,y)
    l2,=ax.plot(xx,yy, color = 'red')
    l3,=ax.plot(I_cal.real,I_cal.imag)
    plt.axis('equal')
    show()


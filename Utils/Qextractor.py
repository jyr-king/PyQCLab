# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 15:48:04 2016
class Qextractor: get a Sparameter data and try to extract the internal Q and coupling Q factors.
@author: Xmon-SC05
"""
#import os
import numpy as np
import skrf as rf
from scipy.optimize import leastsq,curve_fit

def fitQ_UCSB(p,x,y):
    Qi,Qc,phi,f0=p
    invS21=1+Qi/Qc*np.exp(1j*phi)/(1+2j*Qi*(x-f0)/f0)
    a=1/y-invS21
    return a.real**2 + a.imag**2
    
def fitQ_Yale(p,x,y):
    Qe,Qt,df,f0=p
    S21=1-(1/Qe-2j*df/f0)/(1/Qt+2j*(x-f0)/f0)
    a=y-S21
    return a.real**2 + a.imag**2 

def fit_linearPhase(x,a,b):
    return a*x+b

def dbphase2complex(mag_db,phase,deg=True):
    if deg:
        phase=np.deg2rad(phase)
        return rf.db_2_mag(mag_db)*np.exp(1j*phase)
        
class Qextractor():
    def __init__(self,freq=0,sparam=0):
        self.freq=freq
        self.sparam=sparam
        self.q_succeed=False
        self.P=0
#        self.update(p0)    

    def _normalize(self):
        magS_n = rf.db_2_mag(self.magS_db-self.magS_db[0] - \
        (self.magS_db[0]-self.magS_db[-1])/(self.freq[0]-self.freq[-1])*(self.freq-self.freq[0]))
        angS_n  = self.angS-self.angS[0] - \
        (self.angS[0]-self.angS[-1])/(self.freq[0]-self.freq[-1])*(self.freq-self.freq[0])
        self.S_n = magS_n*(np.cos(angS_n)+1j*np.sin(angS_n))
        self.invS_n=1/self.S_n
    
    def  _normalize2(self,N=10):
        magS_n=rf.db_2_mag(self.magS_db-(self.magS_db[0]+self.magS_db[-1])/2)
        popt,pcov=curve_fit(fit_linearPhase,self.freq[:N],self.angS[:N])
        angS_n=self.angS-(popt[0]*self.freq+popt[1])
        self.S_n=magS_n*np.exp(1j*angS_n)
        self.invS_n=1/self.S_n
        
    def _extractQ(self,p0,method='Yale'):
        if method=='Yale':
            P,ier=leastsq(fitQ_Yale,p0,args=(self.freq,self.S_n))
            if ier < 4:
#            else:
#            for i in range(iter-1):
#                P,ier=leastsq(fitQ_Yale,P,args=(self.freq,self.S_n))
                self.S_fit=1-(1/P[0]-2j*P[2]/P[3])/(1/P[1]+2j*(self.freq-P[3])/P[3])
                self.invS_fit=1/self.S_fit
    #            figure(), plot(S21_n.real,S21_n.imag,'b-',S21_fit.real,S21_fit.imag,'r*')
                self.Qi=P[0]*P[1]/(P[0]-P[1])
                self.Qc=P[0]
                self.f0=P[3]
                self.P=P
                self.q_succeed=True
            else:
                print('Cannot find the solution.')
#                self.q_succeed=False
        elif method=='UCSB':
            P,ier=leastsq(fitQ_UCSB,p0,args=(self.freq,self.S_n))
            if ier < 4:
#            invS21 = 1/S21_n
#            else:
                self.invS_fit = 1+P[0]/P[1]*np.exp(1j*P[2])/(1+2j*P[0]*(self.freq-P[3])/P[3])
                self.S_fit=1/self.invS_fit
    #            figure()
    #            plot(invS21.real,invS21.imag,'bo',invS21_fit.real,invS21_fit.imag,'r-')
                self.Qi,self.Qc,self.f0=P[0],P[1],P[3]
                self.P=P
                self.q_succeed=True
            else:
                print('Cannot find the solution.')
#                self.q_succeed=False
        elif method=='WANG':
#            P,ier=leastsq(self.fitsCirle,p0,args=(self.freq,self.S_n))
                self.fitsCirle(p0)
    def update(self,p0,method='Yale'):
        self.q_succeed=False
        self.magS_db=rf.mag_2_db(np.abs(self.sparam))
        self.angS=np.unwrap(np.angle(self.sparam),discont=0.9*np.pi)
        self._normalize()
        self._extractQ(p0,method)
        
    def update2(self,p0,method='UCSB'):
        self.q_succeed=False
        self.magS_db=rf.mag_2_db(np.abs(self.sparam))
        self.angS=np.unwrap(np.angle(self.sparam),discont=0.9*np.pi)
        self._normalize2()
        self._extractQ(p0,method)   
   
        
    def fitsCirle(self,p0,method='WANG'):
        S_21=self.invS_n
        N=len(S_21)
        Fre=self.freq
        x=S_21.real
        y=S_21.imag
        C=np.float64(N)* np.sum(x**2) - np.sum(x)*np.sum(x)
        D=np.float64(N) * np.sum(x*y) - np.sum(x)*np.sum(y)
        E=np.float64(N)* np.sum(x**3)+np.float64(N) *np.sum(x*y**2) - (np.sum(x**2) +np.sum(y**2)) *np.sum(x)
        G=np.float64(N) * np.sum(y**2)-np.sum(y) *np.sum(y)
        H=np.float64(N) * np.sum(x**2*y) + np.float64(N) *np.sum(y**3) - (np.sum(x**2) +np.sum(y**2))*np.sum(y)
        a2=(H * D - E * G) / (C * G - D * D)
        b2=(H * C - E * D) / (D * D - G * C)
        c2=-(a2 *np.sum(x) + b2*np.sum(y)+np.sum(x**2) +np.sum(y**2))/np.float64(N) 
        xc=-a2/2
        yc = b2/(-2)
        radius =np.sqrt(a2 * a2 + b2 * b2 - 4 * c2) / 2
        
        alpha=np.arange(0,2*np.pi,2*np.pi/500)
        fitxx=radius*np.cos(alpha)+xc
        fityy=radius*np.sin(alpha)+yc
        self.invS_fit=fitxx+1j*fityy
        #三个重要点的坐标
        ang=np.arctan(yc/(xc-1))
        x0=radius*np.cos(ang)+xc
        y0=radius*np.sin(ang)+yc
        x1=-radius*np.sin(ang)+xc
        x2=radius*np.sin(ang)+xc
        y1=radius*np.cos(ang)+yc
        y2=-radius*np.cos(ang)+yc
        delta0=np.sqrt((S_21.real-x0)**2+(S_21.imag-y0)**2)
        delta1=np.sqrt((S_21.real-x1)**2+(S_21.imag-y1)**2)
        delta2=np.sqrt((S_21.real-x2)**2+(S_21.imag-y2)**2)
        ind0=np.argpartition(delta0, 2)[:2]
        ind1=np.argpartition(delta1, 2)[:2]
        ind2=np.argpartition(delta2, 2)[:2]
        k0=delta0[ind0[0]]/(delta0[ind0[0]]+delta0[ind0[1]])
        k1=delta1[ind1[0]]/(delta1[ind1[0]]+delta1[ind1[1]])
        k2=delta2[ind2[0]]/(delta2[ind2[0]]+delta2[ind2[1]])
        self.ff0=Fre[ind0[0]]*k0+Fre[ind0[1]]*(1-k0)
        ff1=Fre[ind1[0]]*k1+Fre[ind1[1]]*(1-k1)
        ff2=Fre[ind2[0]]*k2+Fre[ind2[1]]*(1-k2)
        
        self.Qi=self.ff0/abs(ff1-ff2)
        self.Qc=self.Qi/radius/(1-np.tan(ang))/2
#        self.Qi,self.Qc,self.f0=p0[0],p0[1],p0[3]
        self.P=p0
        self.q_succeed=True
        print('Wang fit')
        pass
      
   
    
    
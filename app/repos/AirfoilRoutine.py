from math import cos, sin, tan
from math import atan
from math import pi
from math import pow
from math import sqrt
import numpy as np
import plotly.express as px
import pandas as pd

from repos import line_style

def Plot(X,Y,filename):  
    df = pd.DataFrame({'x':X,'y':Y})
    return line_style.style(df,filename,"x","y")

def linspace(start,stop,np):
    return [start+(stop-start)*i/(np-1) for i in range(np)]

class AirfoilOpt:
    def __init__(self,cl,Re,xf):
        #xf,op = boolean returned by a radio button, when clicking opposite 
        #radio button should be unable
        self.cl = cl
        self.Re = Re
        self.xf = xf
        
    def ComputeOpt(self):
        if self.xf == 1:
            #XFOIL
            t = p00,p10,p01,p20,p11,p02,p30,p21,p12,p03,p40,p31,p22,p13,p04,p50,p41,p32,p23,p14,p05 = 0.09518,0.01241,-2.833e-7,0.02037,-2.515e-7,1.867e-12,-0.008588,-8.79e-9,7.272e-13,-4.661e-18,-0.002015,3.978e-8,-1.519e-13,-4.172e-19,3.83e-24,0,0,0,0,0,0;
            m = p00,p10,p01,p20,p11,p02,p30,p21,p12,p03,p40,p31,p22,p13,p04,p50,p41,p32,p23,p14,p05 = 0.1254,-0.6447,-1.177e-06,1.361,3.543e-06,3.296e-12,-1.526,-2.139e-06,-1.127e-11,4.103e-18,0.8753,3.56e-07,4.252e-12,1.625e-17,-2.688e-23,-0.2038,2.88e-07,-2.367e-12,3.096e-18,-1.622e-23,2.928e-29
            p = p00,p10,p01,p20,p11,p02,p30,p21,p12,p03,p40,p31,p22,p13,p04,p50,p41,p32,p23,p14,p05 = 0.548572941651842,-2.11497686350137,6.41281207623112e-06,6.30329817937694,-1.11031553136444e-05,-4.46380029607996e-11,-6.68932026608318,2.67087147832565e-06,5.55792416719627e-11,1.29606199644897e-16,2.73722562622503,6.49029298130340e-06,-3.79242867621302e-11,-5.62780485239714e-17,-1.95021386686158e-22,-0.321223019110041,-3.41872897707494e-06,1.16010721373322e-11,4.96092230048236e-18,3.73527580989757e-23,1.10980366990981e-28
            a = p00,p10,p01,p20,p11,p02,p30,p21,p12,p03,p40,p31,p22,p13,p04,p50,p41,p32,p23,p14,p05 = -5.037,47.47,3.753e-05,-99.91,-0.0001886,-4.993e-11,127.6,9.309e-05,7.025e-10,-7.263e-16,-75.48,-4.305e-05, -7.337e-11,-1.442e-15, 2.632e-21 ,17.36 ,-1.013e-05 , 1.477e-10 ,-3.962e-16 , 1.661e-21 , -2.651e-27
            e = p00,p10,p01,p20,p11,p02,p30,p21,p12,p03,p40,p31,p22,p13,p04,p50,p41,p32,p23,p14,p05 = 180.8 ,-1058,-0.001234,2553 , 0.004138, 6.259e-09 ,-2868 , -0.00381,-1.159e-08,-1.834e-14 , 1465 , 0.002486 ,1.457e-09 ,2.808e-14,2.353e-20, -278.4 ,-0.0005777, -7.806e-10 ,1.526e-15 ,-2.904e-20 , -8.212e-27
      
        else:
            #Openfoma = 
            t = p00,p10,p01,p20,p11,p02,p30,p21,p12,p03,p40,p31,p22,p13,p04,p50,p41,p32,p23,p14,p05 = 0.07889 , 0.01672 , -1.758e-08 , -0.05668 ,2.524e-08 ,1.218e-13 , 0.08513, -7.137e-08 , -3.485e-14 , -5.01e-19 ,-0.05713 , 7.199e-8 , -6.425e-14, 6.336e-20 , 8.571e-25 ,0.01376,-1.897e-08 , -8.236e-15 , 1.009e-19 , -2.002e-25,-4.922e-31
            m = p00,p10,p01,p20,p11,p02,p30,p21,p12,p03,p40,p31,p22,p13,p04,p50,p41,p32,p23,p14,p05 = -0.02023,0.1182, 1.537e-07,-0.124, 1.185e-07 , -1.102e-12 , 0.09208 , -2.497e-07 ,4.935e-14, 3.427e-18 , -0.01241 ,1.257e-07,1.799e-13 , -3.424e-19 ,-5.108e-24 , -0.005936 ,-1.94e-08,-4.414e-14 ,-7.782e-20 ,3.618e-25 ,2.915e-30
            p = p00,p10,p01,p20,p11,p02,p30,p21,p12,p03,p40,p31,p22,p13,p04,p50,p41,p32,p23,p14,p05 = 0.4108, 0.04476,-3.693e-07,-0.1586 ,-9.411e-08 ,3.465e-12 ,0.3365 , -6.553e-07 , 2.028e-12 , -1.548e-17,-0.3046, 9.906e-07,-1.618e-12 , -2.143e-18 ,2.98e-23 , 0.09557 ,-4.299e-07,8.917e-13 ,-6.911e-19 ,2.619e-24 ,-2.165e-29
            a = p00,p10,p01,p20,p11,p02,p30,p21,p12,p03,p40,p31,p22,p13,p04,p50,p41,p32,p23,p14,p05 = 2.03 , -0.831 , -1.772e-05 , 8.198 , -2.097e-05 ,1.303e-10 ,-3.592, 2.714e-05, 3.198e-11 , -4.256e-16 , -2.264 ,-1.647e-05 , -1.38e-12 ,-8.249e-17 ,6.969e-22,1.553 ,1.342e-06 ,1.239e-11,-3.24e-17,1.091e-22 ,-4.62e-28
            e = p00,p10,p01,p20,p11,p02,p30,p21,p12,p03,p40,p31,p22,p13,p04,p50,p41,p32,p23,p14,p05 = -0.6456,30.84,5.542e-05,65.34,0.0002088,-4.808e-10 ,-136.5 ,-9.964e-05 , -5.69e-10 ,1.854e-15,88.47 ,-7.461e-06 ,1.678e-10 , 9.211e-16 , -3.316e-21 , -20.95 ,2.582e-05 , -1.064e-10 ,1.4e-16,-8.841e-22 ,2.334e-27
        
            
        matrix = [t,m,p,a,e]
        opts  = []
        
        for i in range(5):        
            val = matrix[i][0] + matrix[i][1]*self.cl + matrix[i][2]*self.Re + matrix[i][3]*self.cl**2 + matrix[i][4]*self.cl*self.Re + matrix[i][5]*self.Re**2 + matrix[i][6]*self.cl**3 + matrix[i][7]*self.cl**2*self.Re + matrix[i][8]*self.cl*self.Re**2 + matrix[i][9]*self.Re**3 + matrix[i][10]*self.cl**4 + matrix[i][11]*self.cl**3*self.Re + matrix[i][12]*self.cl**2*self.Re**2  + matrix[i][13]*self.cl*self.Re**3 + matrix[i][14]*self.Re**4 + matrix[i][15]*self.cl**5   + matrix[i][16]*self.cl**4*self.Re + matrix[i][17]*self.cl**3*self.Re**2 + matrix[i][18]*self.cl**2*self.Re**3 + matrix[i][19]*self.cl*self.Re**4 + matrix[i][20]*self.Re**5
            opts.append(val)
        self.t, self.m, self.p, self.a, self.e = opts[0],opts[1],opts[2],opts[3],opts[4]
        if self.m < 0:
            self.m == 0
        filename = "NACA Numbers: m = " + str(round(self.m*100,3)) + " p = " + str(round(self.p*10,3))+  " t = " + str(round(self.t*100,3)) #+ " At Cl = " +  str(self.cl) + " and Re = " + str(self.Re)
        return self.t, self.m, self.p, self.a, self.e, filename
        
    

    def Coordinates(self,n,finite_TE = False, half_cosine_spacing = False):
        n = int(round(n/2,0))
        m = float(self.m)
        p = float(self.p)
        t = float(self.t)
    
        a0 = +0.2969
        a1 = -0.1260
        a2 = -0.3516
        a3 = +0.2843
    
        if finite_TE:
            a4 = -0.1015 # For finite thick TE
        else:
            a4 = -0.1036 # For zero thick TE
    
        if half_cosine_spacing:
            beta = linspace(0.0,pi,n+1)
            x = [(0.5*(1.0-cos(xx))) for xx in beta]  # Half cosine based spacing
        else:
            x = linspace(0.0,1.0,n+1)
    
        yt = [5*t*(a0*sqrt(xx)+a1*xx+a2*pow(xx,2)+a3*pow(xx,3)+a4*pow(xx,4)) for xx in x]
    
        xc1 = [xx for xx in x if xx <= p]
        xc2 = [xx for xx in x if xx > p]
    
        if p == 0:
            xu = x
            yu = yt
    
            xl = x
            yl = [-xx for xx in yt]
    
            xc = xc1 + xc2
            zc = [0]*len(xc)
        else:
            yc1 = [m/pow(p,2)*xx*(2*p-xx) for xx in xc1]
            yc2 = [m/pow(1-p,2)*(1-2*p+xx)*(1-xx) for xx in xc2]
            zc = yc1 + yc2
    
            dyc1_dx = [m/pow(p,2)*(2*p-2*xx) for xx in xc1]
            dyc2_dx = [m/pow(1-p,2)*(2*p-2*xx) for xx in xc2]
            dyc_dx = dyc1_dx + dyc2_dx
    
            theta = [atan(xx) for xx in dyc_dx]
    
            xu = [xx - yy * sin(zz) for xx,yy,zz in zip(x,yt,theta)]
            yu = [xx + yy * cos(zz) for xx,yy,zz in zip(zc,yt,theta)]
    
            xl = [xx + yy * sin(zz) for xx,yy,zz in zip(x,yt,theta)]
            yl = [xx - yy * cos(zz) for xx,yy,zz in zip(zc,yt,theta)]
    
        X = xu[::-1] + xl[1:];
        Z = yu[::-1] + yl[1:];
    
        self.X = X
        self.Y = Z
        return self.X, self.Y
        
            

        
              
      
      
        
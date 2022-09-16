import numpy as np
import plotly.express as px
import pandas as pd
import math

from repos import line_style

def Plot(X,Y):  
    df = pd.DataFrame({'Velocity (m/s)':X,'Thrust (N)':Y})
    return line_style.style_thrust(df,"Thrust","Velocity (m/s)","Thrust (N)")

def PlotEmptyTO(X,Y):  
    df = pd.DataFrame({'[m]':X,' ':Y})
    return line_style.style_thrust(df,'Take-off Runway','[m]',' ')

def PlotTakeOff(X,names):  
    return line_style.style_takeOff(X,names,'Take-off Runway','[m]','[-]')

class AircraftThrust(object):
    def __init__(self,S,p,cd0,V,Kv,d,P,own):
        #xf,op = boolean returned by a radio button, when clicking opposite 
        #radio button should be unable
        self.S,self.p,self.V, self.Kv,self.d,self.P, self.cd0 = S, p, V, Kv, d, P, cd0*0.5*p*S
        self.RPM1     = self.Kv*self.V*0.9*0.2
        self.RPM2     = self.Kv*self.V*0.9*0.4
        self.RPM3     = self.Kv*self.V*0.9*0.6
        self.RPM4     = self.Kv*self.V*0.9*0.8
        self.RPM5     = self.Kv*self.V*0.9*1
        if own:
            self.own = own/100
            self.RPMown   = self.Kv*self.V*0.9*self.own
        else:
            self.RPMown = ''
        
    def ComputeThrust(self):
        V0       = np.arange(0, 200, 0.01) #%m/s airspeed
        D        = []
        T1       = []
        T2       = []
        T3       = []
        T4       = []
        T5       = []
        Town     = []
        D.append(0)
        T1.append((self.p*math.pi*((0.0254*self.d)**2)/4)*(((self.RPM1*0.0254*self.P/60)**2)-((self.RPM1*0.0254*self.P/60)*V0[0]))*(self.d/(3.29546*self.P))**1.5)
        T2.append((self.p*math.pi*((0.0254*self.d)**2)/4)*(((self.RPM2*0.0254*self.P/60)**2)-((self.RPM2*0.0254*self.P/60)*V0[0]))*(self.d/(3.29546*self.P))**1.5)
        T3.append((self.p*math.pi*((0.0254*self.d)**2)/4)*(((self.RPM3*0.0254*self.P/60)**2)-((self.RPM3*0.0254*self.P/60)*V0[0]))*(self.d/(3.29546*self.P))**1.5)
        T4.append((self.p*math.pi*((0.0254*self.d)**2)/4)*(((self.RPM4*0.0254*self.P/60)**2)-((self.RPM4*0.0254*self.P/60)*V0[0]))*(self.d/(3.29546*self.P))**1.5)
        T5.append((self.p*math.pi*((0.0254*self.d)**2)/4)*(((self.RPM5*0.0254*self.P/60)**2)-((self.RPM5*0.0254*self.P/60)*V0[0]))*(self.d/(3.29546*self.P))**1.5)
        if self.RPMown:
          Town.append((self.p*math.pi*((0.0254*self.d)**2)/4)*(((self.RPMown*0.0254*self.P/60)**2)-((self.RPMown*0.0254*self.P/60)*V0[0]))*(self.d/(3.29546*self.P))**1.5)
        i = 0
        while T1[i]>0:
            i    +=1 
            T1.append((self.p*math.pi*((0.0254*self.d)**2)/4)*(((self.RPM1*0.0254*self.P/60)**2)-((self.RPM1*0.0254*self.P/60)*V0[i]))*(self.d/(3.29546*self.P))**1.5)
            
        i = 0
        while T2[i]>0:
            i    +=1 
            T2.append((self.p*math.pi*((0.0254*self.d)**2)/4)*(((self.RPM2*0.0254*self.P/60)**2)-((self.RPM2*0.0254*self.P/60)*V0[i]))*(self.d/(3.29546*self.P))**1.5)
            
        i = 0
        while T3[i]>0:
            i    +=1 
            T3.append((self.p*math.pi*((0.0254*self.d)**2)/4)*(((self.RPM3*0.0254*self.P/60)**2)-((self.RPM3*0.0254*self.P/60)*V0[i]))*(self.d/(3.29546*self.P))**1.5)
            
        i = 0
        while T4[i]>0:
            i    +=1 
            T4.append((self.p*math.pi*((0.0254*self.d)**2)/4)*(((self.RPM4*0.0254*self.P/60)**2)-((self.RPM4*0.0254*self.P/60)*V0[i]))*(self.d/(3.29546*self.P))**1.5)
        
        i = 0 
        if self.RPMown:
          while Town[i]>0:
            i +=1
            Town.append((self.p*math.pi*((0.0254*self.d)**2)/4)*(((self.RPMown*0.0254*self.P/60)**2)-((self.RPMown*0.0254*self.P/60)*V0[i]))*(self.d/(3.29546*self.P))**1.5)
    
        i = 0
        while T5[i]>0:
            i    +=1 
            T5.append((self.p*math.pi*((0.0254*self.d)**2)/4)*(((self.RPM5*0.0254*self.P/60)**2)-((self.RPM5*0.0254*self.P/60)*V0[i]))*(self.d/(3.29546*self.P))**1.5)
        V0  = V0[0:i+1]
        
        i = 0       
        while D[i] <T5[i]:
            i    +=1 
            D.append(self.cd0*(V0[i]**2))
            
            
        T1    = np.array(T1)
        T2    = np.array(T2)
        T3    = np.array(T3)
        T4    = np.array(T4)
        T5    = np.array(T5)
        if self.RPMown:
          Town  = np.array(Town)
        else:
            Town = 0
        D   = np.array(D)        
        #ABC  = np.stack((T1,T2,T3,T4,T5,V0))
        StaticThrust=T5[0]; #Newton at 100% throttle
        #print("Static Thrust at 100% throttle [N]:",StaticThrust)
        MaxFlightVelocity=V0[i]; #Km/h
        #print("Maximum flight velocity [Km/h]:",MaxFlightVelocity)
        #X = ABC[5,:];  #this is the V in the other module, the "dynamic" velocity
        #Y = ABC[4,:];  #This is T in the other module, is the dynamuc thrust at 100% throttle
        return T1.tolist(),T2.tolist(),T3.tolist(),T4.tolist(),T5.tolist(),Town.tolist(),V0.tolist(),MaxFlightVelocity

#Small dialog text with the following message:
#Assuming the aircraft is able to rotate at 1.1Vstall


class TakeOffRun(object):
    def __init__(self,mass,Rrc,density,S,Cltakeoff,Clmax,dcoef,TownVal,Ts,T1,T2,T3,T4,T5,TownVec,V0,T):
        #Ts = boolean returned by a radio button, when clicking opposite 
        #radio button should be unable
        self.mass,self.Rrc,self.density, self.S,self.Cltakeoff,self.Clmax,self.dcoef,self.TownVal,self.Ts,self.T1,self.T2,self.T3,self.T4,self.T5,self.TownVec,self.V0,self.T  = mass,Rrc,density,S,Cltakeoff,Clmax,dcoef,TownVal,Ts,T1,T2,T3,T4,T5,TownVec,V0,T
        self.weight     = self.mass*9.81
        self.timestep   = 0.001
        
    def ComputeTakeOffRunStatic(self):
      

          i          =  1
          t          = [0]
          x          = [0]
          D          = [0]
          V          = [0]
          L          = [0.5*self.density*self.S*self.Cltakeoff*(V[0]**2)]
          N          = [self.weight-L[0]]
          Fr         = [self.Rrc*N[0]]
          ax         = [(self.T-D[0]-Fr[0])/self.mass]
          Vreq       = [(2*self.weight/(self.S*self.density*self.Clmax))**0.5]
          
          
          while V[i-1]<Vreq[0]*1.1:
            t.append(t[i-1]+self.timestep)    
            x.append(x[i-1]+V[i-1]*self.timestep+((self.timestep**2)/2)*ax[i-1])
            V.append(V[i-1]+ax[i-1]*self.timestep)
            D.append(0.5*self.density*self.S*self.dcoef*(V[i]**2))
            L.append(0.5*self.density*self.S*self.Cltakeoff*(V[i]**2))
            N.append(self.weight-L[i])
            Fr.append(self.Rrc*N[i])    
            ax.append((self.T-D[i]-Fr[i])/self.mass)
            i =i+1
            if i > 120000:
                x.append(6666)
                break
                
            
          if x[-1] == 6666:
            xx="Unable to takeoff"
            tt="Maximum time of 2 min exceed"
          else:
            xx=x[-1]
            tt=t[-1]
        
          #print("Takeoff time [s]:",tt)
          #print("Takeoff runway [m]:",xx)
          names = ['100']
          return names,xx,tt
       
                    
    def ComputeTakeOffRunDynamic(self): 
          
          names = ['20','40','60','80','100']
          mat = [self.T1,self.T2,self.T3,self.T4,self.T5]
          
          if self.TownVal:
            names = [20,40,60,80,100]
            vec = []
            index = ''
            for i,j in enumerate(names):
              if i!=len(names)-1:
                if j<=self.TownVal and names[i+1]>=self.TownVal:
                  index = i
              vec.append(str(j))
            names = vec
            if not index:
              index = -1 
            names.insert(index+1,str(self.TownVal))
            mat = [self.T1,self.T2,self.T3,self.T4,self.T5]
            mat.insert(index+1,self.TownVec)
          
          
            
          xx = []
          tt = []
          
          for j in range(0,len(mat),1):
            i          = 1
            t          = [0]
            x          = [0]
            D          = [0]
            V          = [0]
            L          = [0.5*self.density*self.S*self.Cltakeoff*(V[0]**2)]
            N          = [self.weight-L[0]]
            Fr         = [self.Rrc*N[0]]
            ax         = [(mat[j][0]-D[0]-Fr[0])/self.mass]          
           
            Vreq       = (2*self.weight/(self.S*self.density*self.Clmax))**0.5
            while V[i-1] < Vreq*1.1:
              t.append(t[i-1]+self.timestep)    
              x.append(x[i-1]+V[i-1]*self.timestep+((self.timestep**2)/2)*ax[i-1])
              V.append(V[i-1]+ax[i-1]*self.timestep)
              D.append(0.5*self.density*self.S*self.dcoef*(V[i]**2))
              L.append(0.5*self.density*self.S*self.Cltakeoff*(V[i]**2))
              N.append(self.weight-L[i])
              Fr.append(self.Rrc*N[i])              
              min_Index = np.argmin(np.abs(np.array(self.V0)-np.array(V[i])))
              ax.append((mat[j][min_Index]-D[i]-Fr[i])/self.mass)
              i +=1
              if i > 120000:
                x.append(6666)
                break
                
            
            if x[-1] == 6666:
                xx.append("")
                tt.append("Maximum time of 2 min exceed")
            else:
                xx.append(x[-1])
                tt.append(t[-1])
        
          #print("Takeoff time [s]:",tt)
          #print("Takeoff runway [m]:",xx)
          #print(names)
          return names,xx,tt
           
          
     
                                  
               
        
        

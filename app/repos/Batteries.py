import math
import plotly.express as px
import pandas as pd
import numpy as np 

from repos import line_style
 
class  Battery(object):
    def __init__(self,rad1,rad2,rad3,var1,var2,k):
      self.rad1,self.rad2,self.rad3,self.var1,self.var2,self.k = rad1, rad2, rad3, var1, var2, k
      
    def ComputeVal(self):
      
      if self.rad2==1:
          self.k = 1.05    
      elif self.rad2==2 or self.rad2==3:
          self.k = 1.3
      elif self.rad2==4 or self.rad2==5:
        self.k = 1.03  
        
      if self.rad1==1:
          t = self.rad3*((self.var1/(self.var2*self.rad3))**self.k)        #h
          #print("t [h]:",t)
          self.t = t
          self.C = self.var1
          self.i = self.var2
          return t
      elif self.rad1==2:
          C = (self.var1**(1/self.k))*self.var2*self.rad3/(self.rad3**(1/self.k))    #Ah
          #print("C [Ah]:",C)
          self.t = self.var1
          self.C = C
          self.i = self.var2
          return C
      elif self.rad1==3:
          i = self.var2/(self.rad3*((self.var1/self.rad3)**(1/self.k)))  #amp
          #print("i [A]:",i)
          self.t = self.var1
          self.C = self.var2
          self.i = i
          return i
      
    def GenPlotCord(self):
        
        numbers = np.linspace(0.1, 5, 100)    
        iP = numbers*self.i
        iP = np.array(iP)
        valCp = []
        for i in list(self.C/(iP*self.rad3)):
           valCp.append(i**self.k)
        CP = iP*(self.rad3*np.array(valCp))
        tP = self.rad3*np.array(valCp)
        return iP.tolist(),CP.tolist(),tP.tolist()
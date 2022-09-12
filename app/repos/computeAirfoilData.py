import numpy as np
import math
import os
import XfoilCalculator
from airfoildata import airfoildata

class airfoilData(object):
    def __init__(self, airfoilFile,Re):
        self.Re = Re
        self.airfoilFile = airfoilFile
        self.X, self.Y = XfoilCalculator.extractCoordinates(self.airfoilFile)
        XfoilCalculator.plot(self.X, self.Y, "Airfoil", "[x/c]", "[-]")
        
        
    def computeAeroData(self):
        alpha = list(range(-8,18,1))
        nodes = "100"
        iteration = "100"
        visc = "On"
        XfoilCalculator.CreateAirfoilFile(self.X,self.Y)
        self.Cl, self.Cd, self.Cm, self.alpha = XfoilCalculator.XfoilF(self.Re, alpha, nodes, iteration, visc)
        XfoilCalculator.plot(self.alpha, self.Cl, "Cl vs alpha", r"$\alpha$", "Cl")
        XfoilCalculator.plot(self.alpha, self.Cd, "Cd vs alpha",  r"$\alpha$", "Cd")
        XfoilCalculator.plot(self.alpha, self.Cm, "Cm vs alpha ",  r"$\alpha$", "Cm")
        XfoilCalculator.plot(self.Cd, self.Cl, "Cl vs Cd ",  "Cd", "Cl")
                             
        
    def ComputeMainParams(self):
        Cla, Clmax, Cdmin, alphastall, alpha0, Cd0, Cm0c4, x_ac, cmac_mean = airfoildata(self.alpha,self.Cl,self.Cd,self.Cm)
        return Cla, Clmax, Cdmin, alphastall, alpha0, Cd0, Cm0c4, x_ac, cmac_mean
        
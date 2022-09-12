import os 
import pandas as pd
import numpy as np 
import line_style

def XfoilF(Re,alpha,nodes,iteration,visc):
    file = f"data/Re={str(Re)}_{str(nodes)}.txt"
    count = 1
    
    step = round((alpha[-1]-alpha[0])/(len(alpha)-1))
    if not step:
        step = 0
    
    with open('input.txt','w') as f:
        f.write("PLOP\nG\n\nload AirfoilCoordinates.dat \nppar \n")
        f.write(f"n {str(nodes)}\n \n \n")
        f.write("MDES\nFILT\nEXEC\n\nPANE\n\noper \niter \n")
        f.write(f"{str(iteration)} \n")
        if visc == "On":
            f.write("visc \n")
            f.write(f"{str(Re)} \n")
        else:
            f.write("Re \n")
            f.write(f"{str(Re)} \n")
        f.write("pacc \n")
        f.write(f"{file}\n\n")
        f.write(f"aseq {str(alpha[0])} {str(alpha[-1])} {str(step)} \npacc\n")
        f.close()
    os.system("/home/hoyos/Downloads/xfoil6.97/Xfoil/bin/xfoil < input.txt")
        
    with open(f'{file}','r') as f:
        lines = f.readlines()
        
    os.remove(file)
    
    del lines[0:12]
    Alfa = [None] * len(alpha)
    Cl = [None] * len(alpha)
    Cd = [None] * len(alpha)
    Cm = [None] * len(alpha)
    count = 0
    for i in range(len(alpha)):
        try:
            Cl_f = lines[i]
            Cd_f = lines[i]
            Cm_f = lines[i]
            alpha0 = int(float(Cl_f[2:9]))
            index =  alpha.index(alpha0)
            Alfa[index] = alpha0
            if alpha0 != alpha[count]:
                Alfa[count] = None
                Cl[count] = None
                Cd[count] = None
                Cm[count] = None
                count=+1
            if alpha0 < 10:
                Cl[index] = float(Cl_f[10:18])
            else:
                Cl[index] = float(Cl_f[11:19])
            Cd[index] = float(Cd_f[19:28])
            Cm[index] = float(Cm_f[38:47])
            count=+1
            
            if Cd[index] <= 0:
                Cl[index] = None;
                Cd[index] = None;
                Cm[index] = None;
            
        except:
            alpha_index = [i for i,j in enumerate(Alfa) if j is None]
            alphaF = [alpha[i] for i in alpha_index]
            for j in range(len(alphaF)):
                alphan = alphaF[j]
                index = alpha.index(alphan)
                Alfa[index] = alphan
                Cl[index], Cd[index], Cm[index] = XfoilS(Re,alphan,str(int(nodes)+10), iteration, visc)
            index = [i for i,j in enumerate(Cl) if j is None]
            if index:
                for i in index :
                    del Alfa[i]
                    del Cl[i]
                    del Cd[i] 
                    del Cm[i]
            break 
    return Cl,Cd,Cm,Alfa 
    

def XfoilS(Re,alpha,nodes,iteration,visc):
    if float(nodes) > 160:
        Cl = None
        Cd = None
        Cm = None
        return Cl,Cd,Cm
    file = f"data/Re={str(Re)}_angle={str(alpha)}_n{nodes}.txt"
    with open('input2.txt','w') as f:
        f.write("PLOP\nG\n\nload AirfoilCoordinates.dat \nppar \n")
        f.write(f"n {str(nodes)}\n \n \n")
        f.write("MDES\nFILT\nEXEC\n\nPANE\n\noper \niter \n")
        f.write(f"{str(iteration)} \n")
        if visc == "On":
            f.write("visc \n")
            f.write(f"{str(Re)} \n")
        else:
            f.write("Re \n")
            f.write(f"{str(Re)} \n")
        f.write("SEQP \npacc \n")
        f.write(f"{file}\n\n")
        f.write(f"ALFA {str(alpha)}\n")
        f.close()
    os.system("/home/hoyos/Downloads/xfoil6.97/Xfoil/bin/xfoil < input2.txt")
    with open(f'{file}','r') as f:
        lines = f.readlines()
    
    os.remove(file)
    
    del lines[0:12]
    try:
        Cl_f = lines[0]
        Cd_f = lines[0]
        Cm_f = lines[0]
        if alpha < 10:
            Cl = float(Cl_f[10:18])
        else:
            Cl = float(Cl_f[11:19])
        Cd = float(Cd_f[19:28])
        Cm = float(Cm_f[38:47])
    except:
        Cl, Cd, Cm = XfoilS(Re,alpha,str(int(nodes)+20),iteration,visc)
    return Cl, Cd, Cm


    
def CreateAirfoilFile(X,Y):
    with open('AirfoilCoordinates.dat','w') as f:
        for i in range(len(X)):
            if i ==0:
                f.write('New Airfoil\n')
            f.write("{:.6f}   {:.6f}\n".format(X[i],Y[i]))
    return X,Y

def extractCoordinates(fileName):
    Coords            =np.loadtxt(fileName,skiprows=1)	#Import airfoil coordinates
    X                 =Coords[:,0] 	#X Coordinates
    Y                 =Coords[:,1]  #Y Coordinates
    return X,Y
    
def plot(X,Y,title,xlabel,ylabel):
    df = pd.DataFrame({xlabel:X,ylabel:Y})
    return line_style.style_airfoil(df,title,xlabel,ylabel)
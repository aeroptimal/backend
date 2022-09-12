from scipy import stats
import numpy as np
from scipy.signal import argrelmax
from scipy.signal import argrelmin
from scipy.interpolate import interp1d
import statistics
def airfoildata(alphad,cl,cd,cm):
   
    id1 = (np.abs(np.array(alphad) + 4)).argmin()
    id2 = (np.abs(np.array(alphad) - 7)).argmin()
    #id2 = argrelmax(np.array(cl))[0][0]-1  until max cl -1 position

    Clmax = cl[argrelmax(np.array(cl))[0][0]]
    Cla, intercept, r_value, p_value, std_err = stats.linregress(np.array(alphad[id1:id2])*3.141592/180,cl[id1:id2])  #radians
    Cdmin = cd[argrelmin(np.array(cd))[0][0]]
    alphastall = alphad[argrelmax(np.array(cl))[0][0]] #degrees

    alpha0 = -intercept/(Cla*3.141592/180) #degrees
    y_interp = interp1d(np.array(alphad), np.array(cd),fill_value="extrapolate")
    Cd0 = y_interp(alpha0).item()
    y_interp = interp1d(np.array(alphad), np.array(cm),fill_value="extrapolate")
    Cm0c4 = y_interp(alpha0).item()   #At c/4
    cmacr = []
    variances = []
    b = np.linspace(0.15, 0.4, 40)
    for x in b:
        cmacr.append(np.array(cm[id1:id2]) + np.array(cl[id1:id2])*(x-0.25))
        variances.append(statistics.variance(cmacr[-1]))
    x_ac = b[np.argmin(variances)]
    cmac = np.array(cm[id1:id2]) + np.array(cl[id1:id2])*(x_ac-0.25)  #Array  of cmac (its suppose to be constant)
    cmac_mean = statistics.mean(cmac)
    return(Cla, Clmax, Cdmin, alphastall, alpha0, Cd0, Cm0c4, x_ac, cmac_mean)

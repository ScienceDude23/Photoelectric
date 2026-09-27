import numpy as np
from matplotlib import pyplot as plt


def loadData(filename):
    data = np.loadtxt(filename,delimiter=",",skiprows=2,dtype=float)
    n = len(data[:,0])

    # Individual data columns
    ret = data[:,0] # Retarding potential
    red = (data[:,1]+data[:,2])/2 # Average of red trials
    green = (data[:,3]+data[:,4])/2 # Average of green trials
    blue = data[:,5] # Blue trial

    # Initialize uncertainty arrays
    dd,dr,dg,db = [],[],[],[]

    for i in range(n):
        dd.append(0.05) # Uncertainty in retarding potential
        dr.append(np.sqrt(((data[i,1]-red[i])**2 + (data[i,2]-red[i])**2)/2)) # Uncert in red
        dg.append(np.sqrt(((data[i,3]-green[i])**2 + (data[i,4]-green[i])**2)/2)) # Uncert in green
        db.append((dr[i]+dg[i]) / 2) # Uncert in blue, averaged the red and green values since only 1 trial

    return ret,red,green,blue,dd,dr,dg,db

ret_u,red_u,green_u,blue_u,dd_u,dr_u,dg_u,db_u = loadData("dataset_orig.csv")
ret_m,red_m,green_m,blue_m,dd_m,dr_m,dg_m,db_m = loadData("dataset_mod.csv")


fig, (mod, unm) = plt.subplots(1,2,figsize=(12,5),dpi=300)

mod.errorbar(ret_u,red_u,xerr=dd_u,yerr=dr_u,
             color='red', label='Red')
mod.errorbar(ret_u,green_u,xerr=dd_u,yerr=dg_u,
             color='green', label='Green')
mod.errorbar(ret_u,blue_u,xerr=dd_u,yerr=db_u,
             color='blue', label='Blue')
mod.set_xlabel("Retarding Potential (V)")
mod.set_ylabel("Current (nA)")
mod.set_title("Unmodified data")
mod.legend()

unm.errorbar(ret_u,red_u,xerr=dd_u,yerr=dr_u,
             color='red', label='Red')
unm.errorbar(ret_u,green_u,xerr=dd_u,yerr=dg_u,
             color='green', label='Green')
unm.errorbar(ret_u,blue_m,xerr=dd_u,yerr=db_m,
             color='blue', label='Blue')
unm.set_xlabel("Retarding Potential(V)")
unm.set_title("Modified data")
unm.legend()

plt.savefig('modcomp.png')
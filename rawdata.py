import numpy as np
from matplotlib import pyplot as plt

data = np.loadtxt("dataset_mod.csv",delimiter=",",skiprows=2,dtype=float)
n = len(data[:,0])



# Individual data columns
ret = data[:,0] # Retarding potential
red1 = data[:,1]
red2 = data[:,2]
green1 = data[:,3]
green2 = data[:,4]

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

plt.figure(dpi=300)
plt.errorbar(ret,red1,label="Red Trial 1",
         color='red', linestyle='-',xerr=dd)
plt.errorbar(ret,red2,label="Red Trial 2",
         color='red', linestyle='--',xerr=dd)
plt.errorbar(ret,green1,label="Green Trial 1",
         color='green', linestyle='-',xerr=dd)
plt.errorbar(ret,green2,label="Green Trial 2",
         color='green', linestyle='--',xerr=dd)
plt.errorbar(ret,blue,label="Blue Trial",
         color='blue', linestyle='-',xerr=dd)
plt.xlabel("Retarding Potential (V)")
plt.ylabel("Current (nA)")
plt.title("Raw Trials")
plt.legend()
plt.savefig("rawdata.png")
plt.close()

plt.figure(dpi=300)
plt.errorbar(ret,red2,xerr=dd,yerr=dr,label="Red",
         color='red')
plt.errorbar(ret,green2,xerr=dd,yerr=dg,label="Green",
         color='green')
plt.errorbar(ret,blue,xerr=dd,yerr=db,label="Blue",
         color='blue')
plt.xlabel("Retarding Potential (V)")
plt.ylabel("Current (nA)")
plt.title("Averaged Trials")
plt.legend()
plt.savefig("avgdata.png")
plt.close()

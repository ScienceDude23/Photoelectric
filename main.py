import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from odrpack import odr_fit

# Load data
data = np.loadtxt("dataset.csv", delimiter=",", skiprows=2,dtype=float)
n = len(data[:,0])

# Takes the first 5 data points for first lin reg
def min(qty=[],unc=[]):
    qmin,umin = [],[]
    for i in range(5):
        qmin.append(qty[i])
        umin.append(unc[i])
    return np.array(qmin),np.array(umin)

# Takes the last 5 data points for second lin reg
def max(qty=[],unc=[]):
    qmax,umax = [],[]
    for i in range(5):
        qmax.append(qty[n-(i+1)])
        umax.append(unc[n-(i+1)])
    return np.array(qmax),np.array(umax)

# Linear function to pass to odr_fit
def lin(x,beta):
    print(type(beta),beta)
    a,b = beta
    return a * x + b

# Linear function to pass to curve_fit (different syntax required)
def lin_cf(x,a,b):
    return a * x + b

# Find the stopping potential V0 from the 2 lin regs of I vs V
def V0(a,b,c,d,ua,ub,uc,ud):
    v = (d-b)/(a-c)
    dnum = np.sqrt(ud**2 + ub**2)
    dden = np.sqrt(ua**2 + uc**2)
    dv = np.abs(v)*np.sqrt((dnum/(d-b))**2 + (dden/(a-c))**2)
    return v,dv

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

# Run min and max to get data to pass to lin regs
rmi,drmi = min(red,dr)
gmi,dgmi = min(green,dr)
bmi,dbmi = min(blue,dr)
dmi,ddmi = min(ret,dd)

rma,drma = max(red,dr)
bma,dbma = max(blue,dr)
gma,dgma = max(green,dr)
dma,ddma = max(ret,dd)

# Run the lin regs of I vs V with Orthogonal Distance Regression (ODS)
r_min = odr_fit(lin, dmi,rmi,
                beta0=[60,-190], 
                weight_x=1/(ddmi)**2, 
                weight_y=1/(drmi)**2)
g_min = odr_fit(lin, dmi,gmi,
                beta0=[60,-190], 
                weight_x=1/(ddmi)**2, 
                weight_y=1/(dgmi)**2)
b_min = odr_fit(lin, dmi,bmi,
                beta0=[60,-190],
                weight_x=1/(ddmi)**2,
                weight_y=1/(dbmi)**2)

r_max = odr_fit(lin, dma,rma,
                beta0=[60,-190], 
                weight_x=1/(ddma)**2, 
                weight_y=1/(drma)**2)
g_max = odr_fit(lin, dma,gma,
                beta0=[60,-190], 
                weight_x=1/(ddma)**2, 
                weight_y=1/(dgma)**2)
b_max = odr_fit(lin, dma,bma,
                beta0=[60,-190],
                weight_x=1/(ddma)**2,
                weight_y=1/(dbma)**2)

# Pull the parameters out of the lin reg and compute V0
ra,rb = r_min.beta
rc,rd = r_max.beta
rda,rdb = r_min.sd_beta
rdc,rdd = r_max.sd_beta
v0_r,dv0_r = V0(ra,rb,rc,rd,rda,rdb,rdc,rdd)

ga,gb = g_min.beta
gc,gd = g_max.beta
gda,gdb = g_min.sd_beta
gdc,gdd = g_max.sd_beta
v0_g,dv0_g = V0(ga,gb,gc,gd,gda,gdb,gdc,gdd)

ba,bb = b_min.beta
bc,bd = b_max.beta
bda,bdb = b_min.sd_beta
bdc,bdd = b_max.sd_beta
v0_b,dv0_b = V0(ba,bb,bc,bd,bda,bdb,bdc,bdd)

# Setup for the lin reg of V0 vs nu
v0 = [v0_r,v0_g,v0_b] # volts
dv0 = [dv0_r,dv0_g,dv0_b]
wl = np.array([630,521,466]) # nanometers
nu = 299792458 / wl # gigahertz

# Lin reg of V0 vs nu
popt, pcov = curve_fit(lin_cf,nu,v0,sigma=dv0,absolute_sigma=True) # nV/s
va,vb = popt
dva,dvb = np.sqrt(np.diag(pcov))

# Compute planck constant
h = va * 1.602 # h*10^(-28) to convert to SI
dh = dva * 1.602 
print(h,dh)

#command line - cd C:\double laser\10C

import numpy as np
import pylab as pl
from scipy.optimize import curve_fit
import glob
from sklearn.metrics import r2_score
from tkinter import Tcl
import natsort 

path = 'C:\\double laser\\new\\' 
flist = glob.glob(path+'*.csv')

"""
Flist=np.array([])
for i in flist:
    Flist=np.append(Flist,i.split("new\\")[1].split("C")[0])
Flist = sorted(Flist, key=int)
                   """
n = 0
Ampl_As = np.array([])
Ampl_S = np.array([])
Loss_As = np.array([])
Loss_S = np.array([])
N = np.array([])
ballast = np.array([])
T_arr = np.array([]) 

def generate_specific_rows( filePath, row_indices=[] ):
        with open( filePath ) as x:
            for i, line in enumerate( x ):
                if i in row_indices:
                    yield line

for f in flist[0:1]:
    
    T_arr = np.append( T_arr, float( f.split("new\\")[1].split("C")[0] ) )
    a,b,c = np.loadtxt( f,unpack=True,delimiter=';',usecols=[0,1,3],skiprows=10 )
  
    #read specific rows
    data = np.loadtxt(generate_specific_rows(f, row_indices=[6,8]), dtype='str', delimiter=";")
    T_ballast = float(data[1][26:])
    ballast = np.append(ballast,T_ballast)
    t_meas = data[0]
    
    #Zero level
    b = b-np.average(b[:62]); c = c-np.average(c[:62])
    #From 800m to 8000m
    b = b[392:3921]; c = c[392:3921]; a = a[392:3921]
    # pl.plot(a,b/c, label ='R') #As/S

    #Approximation 
    x = a
    y_as = b
    y_s = c
    
    [e, d], res1 = curve_fit( lambda x1,e,d: e*np.exp(d*x1),  x,  y_as,bounds=(-1, np.inf), maxfev = 10000 )
    [f1, g], res2 = curve_fit( lambda x2,f1,g: f1*np.exp(g*x2),  x,  y_s, bounds=(-1, np.inf), maxfev = 10000 )
    
    y_pred_as = e * np.exp(d * x)
    y_pred_s = f1* np.exp(g * x)
    
    #Parameters As
    Er_a_As = np.sqrt(np.diag(res1))[0]
    Er_k_As = np.sqrt(np.diag(res1))[1]*1000
    Std_As = np.std(y_as-y_pred_as)
    R2_As = r2_score(y_as, y_pred_as)
    
    #Parameters S
    Er_a_S = np.sqrt(np.diag(res2))[0]
    Er_k_S = np.sqrt(np.diag(res2))[1]*1000
    Std_S = np.std(y_s-y_pred_s)
    R2_S = r2_score(y_s, y_pred_s)
    
    pl.figure( f )
    pl.title( 'Reflectogram (T Ballast = %.3f'%T_ballast+" C)", fontsize = 20 )
    pl.plot( x, y_as, 'o', markersize = 6, label = 'Exp_As' )
    pl.plot( x, y_pred_as, '-.', label = 'Fit_As:\na = %.1f±%.1E (arb.un.); \nk = %.3f±%.1E (dB/km);\nstd = %.3f (arb.un.);\nR2 = %.4f'
            %(e, Er_a_As, -d*1000, Er_k_As, Std_As, R2_As), linewidth = 4)
    pl.plot(x, y_s, 'o', markersize = 6, label = 'Exp_St')
    pl.plot(x, y_pred_s, '-.', label = 'Fit_St:\na = %.1f±%.1E (arb.un.); \nk = %.3f±%.1E (dB/km); \nstd = %.3f (arb.un.);\nR2 = %.4f'
            %(f1, Er_a_S, -g*1000, Er_k_S, Std_S, R2_S), linewidth =4) 
    
    pl.rc('xtick',labelsize=10)
    pl.rc('ytick',labelsize=10)
    pl.xlim(800, 8000)
    pl.xlabel('Length (m)', fontsize = 20)
    pl.ylabel('Intensity (arb.un.)', fontsize = 20)
    pl.legend(fontsize = 16)
    pl.grid()
    pl.tight_layout()
    #pl.savefig(k+ '.png') Save all
    
    N = np.append(N,n)
    Ampl_As = np.append( Ampl_As, e )
    Ampl_S = np.append( Ampl_S, f1 )
    Loss_As = np.append( Loss_As,-d*1000 )
    Loss_S = np.append(Loss_S,-g*1000)
    n+=1

#Coeff-s:
#%%
#Amplitude
pl.figure('Amplitude')
pl.plot(T_arr,Ampl_As,'-o', label='Astokes')
pl.plot(T_arr,Ampl_S,'-o', label='Stokes')

pl.xlabel('Temperature (C)', fontsize = 13)
pl.ylabel('Amplitude (arb.un.)', fontsize = 13)
pl.legend()
pl.grid()
pl.tight_layout()
pl.savefig(path+ 'Amplitude.png')
#%%
#Losses
#%%
pl.figure('Losses')
pl.plot(T_arr,Loss_As,'-o', label='Astokes')
pl.plot(T_arr,Loss_S,'-o', label='Stokes')
pl.xlabel('Temperature (C)', fontsize = 13)
pl.ylabel('Losses (dB/km)', fontsize = 13)
pl.legend()
pl.grid()
pl.tight_layout()
pl.savefig(path+ 'Losses.png')
#%%
# Ballast T
#%%
pl.figure('T Ballast')
pl.plot(T_arr, ballast,'-o')
pl.xlabel('Temperature (C)', fontsize = 13)
pl.ylabel('T Ballast (C)', fontsize = 13)
pl.legend()
pl.grid()
pl.tight_layout()
pl.savefig(path+ 'Amplitude.png')
#%%
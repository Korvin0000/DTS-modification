# DTS-modification
This project dedicated to studying the signals (reflectogramms) of Distributed Fiber Temperature Sensor based on Raman scattering (https://en.wikipedia.org/wiki/Distributed_temperature_sensing).

The code implements the next:
1) Read the number of the files with reflectogramms
2) Substract the zero level (the average of 60 points) of Astokes and Stokes reflectogramms for each file and take into account only the measuring line (from 800 m to 8000 m):
3) 
![bef](https://user-images.githubusercontent.com/87599571/170989883-aad6937f-6c0e-48b3-828b-fbd314d73612.png) ![Figure_1](https://user-images.githubusercontent.com/87599571/170989541-4ed7bc2d-1f93-4bcc-94ee-dac95d9f4e1a.png)

3) Then, I approximate the experimental data of the theoretical dependences. In order to reach it, I use the **scipy.optimize.curve_fit()** function:

![Figure_179](https://user-images.githubusercontent.com/87599571/171039311-7474c1d0-795e-4ec5-9ba6-3661488f6a9b.png)

To estimate the quality of approximation I do the following:
 a) print the fitting parameters with errors (from **covariance matrix**: **np.sqrt(np.diag(res1))[1]**)
 
 b) print **np.std**
 
 c) print the coefficient of determination **r2_score** from **sklearn.metrics**
After all, I save all images.

 
I wrote the code that allows to estimate the deviation between the theoretical predictable and the experimental reflectograms. Then, I added the opportunity to convert reflectogramms to the thermogramms (Distribution of the Temperature on the measuring line). 

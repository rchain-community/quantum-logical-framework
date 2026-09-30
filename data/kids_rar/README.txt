## README ##

Thank you for your interest in the lensing results from:
"The Weak Lensing Radial Acceleration Relation: Constraining Modified Gravity and Cold Dark Matter theories with KiDS-1000"
or Brouwer et al. (2021; which we shall refer to as B21 throughout this file).

Each text file contains one Excess Surface Density (ESD) profile obtained using 1000 degrees^2 of weak gravitational lensing data from the Kilo-Degree Survey (KiDS1000). These ESD profiles correspond to the lensing Radial Acceleration Relation (RAR) results shown in the respective figures of B21, as explained below:


## 1) Filenames, how to find your file


All filenames are built up as follows: "Fig-X_Description_Type.txt".

- "Fig-X": The beginning of the filename indicates the Figure number in B21 to which the data in that file corresponds. Some of the files appear in multiple figures as indicated by the different numbers.

- "Description": The middle of the filename gives a short description of the file content: for example "RAR-KiDS-isolated" contains the Radial Acceleration Relation (RAR) of isolated KiDS-bright galaxies.

- "Type": At the end of the filename indicates the type of data the file contains:

-- Filenames ending in "Nobins" or "bin-N":
These files contain the ESD profile data. If the filename ends in "bin-N", the number N refers to one of the bins in galaxy observable. The type of observable is indicated in the filename: Mass (meaning stellar mass), Color (u-r) or Sersic (index). The bins are ordered from the lowest to highest observable value. Each file contains the ESD profile of the galaxies in that observable bin. If the file ends in "Nobins" then the data is not binned by stellar mass (which means there is only one ESD file).

The columns in the ESD files are defined as follows:
- Radius(Mpc or m/s^2): The mean projected distance from the lens center; in Megaparsec for the rotation curve data, or in meter-per-second-squared for the RAR data.
- ESD_t(h70*M_sun/pc^2): The tangential ESD profile in solarmass-per-parsec-squared. This is the data used to compute the observed gravitational acceleration g_obs.
- ESD_x(h70*M_sun/pc^2): (not needed) The cross-profile merely, which functions as a sanity check, as it should be approximately zero within the error bars.
- error(h70*M_sun/pc^2): The 1-sigma error value on ESD_t, calculated using the lensfit weight "w" and the lensing weight "k".
- bias(1+K): The multiplicative calibration correction, which should always be applied to the ESD as follows:
ESD_t[corrected] = ESD_t / bias, error[corrected] = error / bias.
- variance(e_s): Not needed. The mean variance of the sources in this projected distance bin.
- wk2: (not needed) The lensfit weight times the lensing weight squared.
- w2k2: (not needed) The lensfit weight squared times the lensing weight squared.

-- Filenames ending in "covmatrix":
These files provide the full covariance matrix of the ESD profile for all bins observable and radius/acceleration.

The columns of these files are defined as follows:
- Column 1,2, *_min[m,n]: Both indicate the bin in observable, by giving the minimum value of that bin. If there is no binning, both values are -999.
- Column 3,4, Radius[i,j]: Both indicate the bin in projected radius/acceleration, by giving the mean value of that bin.
- Column 5, covariance: The covariance on the ESD corresponding to bin [m,n,i,j]. The square root of this covariance gives the 1-sigma error on the ESD in that bin.
- Column 6, correlation: (not needed) The correlation corresponding to bin [m,n,i,j]. The diagonal of the covariance is 1 by definition.
- Column 7, bias(1+K[m,i])(1+K[n,j]): The multiplicative calibration correction corresponding to bin [m,n,i,j], which should always be applied to the covariance as follows: covariance[corrected] = covariance / bias.


## 2) Files, how to create your result


# Fig-3_Lensing-rotation-curves_*:

These 4+1 files provide the ESD profiles and covariance matrix used to create the lensing rotation curves in Fig.3 of B21. The number behind each filename refers to one of the four stellar mass bins, with bin limits: log10(M*/(h70^-2 Msun)) = [8.5, 10.3, 10.6, 10.8, 11.0].

The Excess Surface Density (ESD_t) is translated into the circular velocity (v_circ) using Eq.23 from B21:
  v_circ[km/s] = sqrt( 4 * G * ESD_t/bias * Radius*[Mpc/pc] ) * [pc/km] ,
  where [Mpc/pc] = 1e6, and [pc/km] = 3.086e13, and G[pc^3/(Msun*s^2)] = 4.52e-30 pc^2/(Msun*s^2).

To calculate the error values on v_circ, the propagation rules are applied as follows:
  error[v_circ] = v_circ * (error[ESD_t] / ESD_t) .


# Fig-X_RAR_*

These 1+1 files provide the ESD profile and covariance matrix used to create the lensing RAR in Fig.X of B21.

The Excess Surface Density (ESD_t) is translated into the observed gravitational acceleration (g_obs) using Eq.7 from B21:
  g_obs[m/s^2] = 4 * G[pc^3/(Msun*s^2)] * ESD_t/bias * [pc/m] ,
    where [pc/m] = 3.086e16, and G[pc^3/(Msun*s^2)] = 4.52e-30 pc^2/(Msun*s^2).

To error values on g_obs are translated in the same way:
  error[g_obs] = 4 * G[pc^3/(Msun*s^2)] * error[ESD_t]/bias * [pc/m] .


## 3) Questions:

For additional information, please read the sections in Brouwer et al. (2021) corresponding to the respective figures.
If the answer is not in B21 or if you find an error, you can send an email to: margot.brouwer@gmail.com. Thank you!
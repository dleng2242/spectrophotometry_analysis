# Spectrophotometry Analysis

This repo contains code to analyse a spectrophotometry experiment.

There are two notebooks containing the two parts of project: visualising
the calibration data (part 1), and then fitting a model to determine the 
concentration from the absorption (part 2).

Functions to generate the cleaned data from the raw CSV is stored in the
make_dataset module in the "src" folder. 


## Quick start


Create a virtual environment and install the packages from the requirements.txt.
I used conda and so ran  `conda create --name py38_spectro python=3.8` and then
activated it with `conda activate py38_spectro` and then  
`pip install -r requirements.txt` to install the required packages.


## Conclusions and Assumptions

The corrected absorption was calculated by subtracting the blank sample
absorption form the sample absorption for each given wavelength. 

Given the linear relationship between absorption and concentration
a linear model was fit to the calibration data.

$$ A = Ecl $$

Where $A$ is the absorption, $E$ is the absorption coefficient, $c$ is 
sample concentration, and $l$ is the path length. 

First the corrected absorption was calculated, and then the dilution converted
to a concentration. 
Given the noise in the data, only the wavelength of peak absorption was used. 
This was determined to be at 536 nm. 
A linear model was then fit and the absorption coefficient extracted.
The model fit well to the data, with an R squared of 1. 

The absorption coefficient was determined to be $E = 0.0329 \pm 0.00006$ ${cm^{-1}}$.

Given $A$, $E$, $L=1$, the concentration $c$ of the new sample
can be determined:

$$ A = Ecl $$
$$ c = \frac{A}{El} $$

The final concentration of sample X1 was determined to be 44.24 mg/L. 

Further details can be found within the notebooks. The absorption coefficient
is actually wavelength dependent and so an extension would be to include
this in the model to get a more accurate concentration. 



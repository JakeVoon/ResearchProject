# Issues: 
Equation (2) 'atan2' requires two inputs, but there's only one? The paper specifically specified using 'atan2'
In the assumptions, 
Currently unkown variables:
 - radius/cross-sectional area of the MCF
 - Young's and Shear moduli of the MCF
 - Number of cores used in the MCF in the lab

Next steps:
1. Solving IVPs by hand
2. Implementing in code (assume external point force location is known for now)
3. Including segmentation algorithm to find breakpoints (location of external point forces)
3. Noise reduction algorithms
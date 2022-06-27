# Issues: 
Equation (2) : `atan2` requires two inputs, but there's only one? ($\kappa_{app}$ is the 'relative' curvatures of each core, so its only a [$n\times1$] vector) The paper specifically said using `atan2`

In the assumptions, $v=v_0$, but that would result in Equation (6) : $n=0$ at all points because $K_v$ is a constant

Currently unkown variables:
 - radius/cross-sectional area of the MCF
 - Young's and Shear moduli of the MCF
 - Number of cores used in the MCF in the lab

Next steps:
1. Solving IVPs by hand (Solving Equation (3) and Equation (4))
   1. $\hat u$ and $\hat v$ are known constants, therefore the equations should be solvable with the $s=L$ initial conditions 

2. Implementing in code (assume external point force location is known for now)
3. Including segmentation algorithm to find breakpoints (location of external point forces)
3. Noise reduction algorithms
% Defining constants
kappa = 
theta_b = 

r = 

Ixx = 0.25*pi*(r^4);
Izz = 2*Ixx;

J = diag([Ixx,Ixx,Izz]);

G = 
E = 
A = pi*r^2

Kv = diag([G*A,G*A,E*A]);
Ku = diag([E,E,G])*J;

% Equilibrium Equations
dnds = -uhat*n - f;
dmds = -uhat*m - vhat*n - l;

% Constitutuve Equations

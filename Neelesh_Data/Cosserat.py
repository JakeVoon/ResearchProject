import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import integrate

class CosseratRodModel:

    def __init__(self,initial_wave0,core_wavelengths):
        self.wave0 = np.array(initial_wave0)
        self.waves = np.array(core_wavelengths)
        self.strain_sens = 0.784
        self.r = 3.7e-5
        radius = 2e-4
        A = np.pi*radius**2
        Ixx = 0.25*np.pi*(radius**4)
        Iyy = Ixx
        Izz = 2*Ixx
        J = np.diag([Ixx,Iyy,Izz])
        G = 0.5 * (32.3 + 30.8)
        E = 0.5 * (74.8 + 71.2)
        self.Kv = np.diag([G*A,G*A,E*A])
        self.Ku = np.diag([E,E,G])*J

    def skew_symmetric(self,vector):

        np.reshape(vector,(1,3))

        skew_matrix = np.zeros((3,3))

        skew_matrix = np.array([[0, -vector[2], vector[1]], 
                                [vector[2], 0, -vector[0]],
                                [-vector[1], vector[0], 0]])

        return skew_matrix

    def single_core_strain(self,central_core_wave0,central_core_waves,wavelengths,initial_wavelengths):
        term1_num = wavelengths - initial_wavelengths
        term1_denom = self.strain_sens * initial_wavelengths
        term2_num = central_core_waves - central_core_wave0
        term2_denom = self.strain_sens * central_core_wave0

        core_strain = (term1_num/term1_denom) - (term2_num/term2_denom)

        return core_strain

    def get_strain(self):

        change_in_strain = np.zeros((3,25))

        central_core_wave0 = self.wave0[25:50]
        central_core_wave = self.waves[25:50]

        change_in_strain[0,:] = self.single_core_strain(central_core_wave0,central_core_wave,self.waves[0:25],self.wave0[25:50])
        change_in_strain[1,:] = self.single_core_strain(central_core_wave0,central_core_wave,self.waves[50:75],self.wave0[50:75])
        change_in_strain[2,:] = self.single_core_strain(central_core_wave0,central_core_wave,self.waves[75:100],self.wave0[75:100])

        return change_in_strain # 3 rows, each row is one of the cores

    def get_app_curvature(self):

        strain = self.get_strain()

        i_comp = 0
        j_comp = 0

        for n in range(3):
            i_comp = i_comp + (strain[n,:]/self.r) * np.cos(np.deg2rad(120*n))
            j_comp = j_comp + (strain[n,:]/self.r) * np.sin(np.deg2rad(120*n))
        
        apparent_curvatures = np.array([-i_comp,-j_comp])

        return apparent_curvatures # 2 rows, first row is i component and second row is j component

    def get_curvature(self):
        
        app_curvature = self.get_app_curvature()

        curvature = (2/3)*np.linalg.norm(app_curvature,axis=0)

        return curvature

    def get_thetab(self):

        app_curves = self.get_app_curvature()

        theta_b = np.arctan2(app_curves[1,:],app_curves[0,:])

        return theta_b

    def get_u(self):
        curvature = self.get_curvature()
        theta_b = self.get_thetab()

        u = np.zeros((3,25))

        u[0,:] = curvature*np.cos(theta_b)
        u[1,:] = curvature*np.sin(theta_b)

        return u

    def get_m(self):

        u = self.get_u()

        m = np.zeros((3,25))

        for n in range(25):
            a = u[:,n]
            m[:,n] = np.matmul(a,self.Ku)

        return m

    def get_n(self):

        n = np.zeros((3,25))

        m = self.get_m()
        dmds = np.array(np.gradient(m,axis=1))
        u = self.get_u()
        v_hat = self.skew_symmetric(vector=np.array([0,0,1]))

        print(v_hat)

        for i in range(25):
            
            u_hat = self.skew_symmetric(u[:,i])

            v_hat_n = dmds[:,i] + u_hat*m[:,i]

            print(v_hat_n.shape)

            n = np.linalg.inv(-v_hat)*v_hat_n

            n[:,i] = v_hat_n

        return n
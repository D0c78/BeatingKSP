import numpy as np
import ussa1976 as isa

# Class to create rocket data
class rocket: 
    def __init__(self, 
                 I_sp: float = 300,
                 m_p: float = 100,
                 A: float = 0,
                 p_e: float = 0,
                 C_D0: float = 0.5,
                 S: float = 100):
        rocket.I_sp = I_sp
        rocket.m_p = m_p
        rocket.A = A
        rocket.p_e = p_e
        rocket.C_D0 = C_D0
        rocket.S = S

# Class to create environment data
class env:
    def __init__(self,
                 ):
        env.p = lambda h : isa.compute(h, variables=['p'])
        env.rho = lambda h : isa.compute(h, variables=['rho'])

# Define propagator
class propagator:
    def __init__(self, funcSim, t0, tf, y0, method):
        propagator.dy = funcSim
        propagator.t0 = t0
        propagator.tf = tf
        propagator.y0 = y0
        propagator.method = method

    def solve(self):
        from scipy import integrate
        t, y = integrate.solve_ivp(propagator.dy, (propagator.t0, propagator.tf), propagator.y0, propagator.method)

# Define differential system
def 



    

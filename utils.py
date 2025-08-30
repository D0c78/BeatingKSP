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
    def __init__(self, funcSim):
        propagator.dy = funcSim



    

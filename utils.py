import numpy as np
import ussa1976 as isa
import KSP_ussa1967 as KSP_isa

# Constants
g_0 = 9.81 # m s^-2
mu_e = 3.5316000e12 # m^3 s^-2
R_0 = 600e3 # m

# Class to create rocket data
class rocket: 
    def __init__(self, 
                 I_sp: float = 300,
                 dm_p: float = 100,
                 A: float = 0,
                 p_e: float = 0,
                 C_D0: float = 0.5,
                 S: float = 100,
                 m_0: float = 1e3,
                 m_min = None):
        self.I_sp = I_sp
        self.dm_p = dm_p
        self.A = A
        self.p_e = p_e
        self.S = S
        self.C_D0 = C_D0
        self.m_0 = m_0
        if m_min == None: 
            self.m_min = 0.15 * m_0
        else:
            self.m_min = m_min

# Class to create environment data
class env:
    def __init__(self):
        self.p = lambda h : KSP_isa.compute(h).p
        self.rho = lambda h : KSP_isa.compute(h).rho

# Define integrator setup
class int_setup:
        def __init__(self, t0, tf, y0, method, max_step) -> None:
            self.t0 = t0
            self.tf = tf
            self.y0 = y0
            self.method = method
            self.max_step = max_step

# Define propagator
class propagator:
    def __init__(self, rocket: rocket, env: env, funcSim, int_setup: int_setup):
        # Store inputs
        self.funcSim = funcSim
        self.rocket = rocket
        self.env = env
        self.int_setup = int_setup

    def solve(self):
        # Import integrator library
        from scipy import integrate
        
        # Recall parameters
        settings = self.int_setup
        
        # Define function to integrate
        def dy(t, y):
            return self.funcSim(t, y, self.rocket, self.env)
        
        # Integrate
        odeSol = integrate.solve_ivp(dy, (settings.t0, settings.tf), settings.y0, settings.method, max_step = settings.max_step)
        
        return odeSol.t, odeSol.y.T

# Define differential system
def Frocket(t, y: np.ndarray, rocket: rocket, env: env):
    '''
    This defines the physics of the simulations
    y:
    [0] R
    [1] sigma
    [2] v
    [3] gamma
    [4] mass
    '''
    # Useful for ease of reading
    R = y[0]
    v = y[2]
    gamma = y[3]
    mass = y[4]

    # Compute gravity force magnitude
    g = mu_e / R ** 2
    F_g = g * mass
    # Compute drag magnitude
    D = 0.5 * env.rho(R - R_0) * v**2 * rocket.S * rocket.C_D0
    # Compute lift magnitude
    ### Note to self: no rotational model included yet: gravity turn ###
    L = 0
    
    # Check over minimum mass
    if mass > rocket.m_min:
        # Compute thrust magnitude
        T = rocket.I_sp * g_0 * rocket.dm_p
        dm = -rocket.dm_p # dM
    else:
        T = 0
        dm = 0

    # Check terrain
    if t > 0 and R < R_0+10:
        dR = 0
        dSigma = 0
    else:
        dR = v * np.sin(gamma) # dR
        dSigma = -v/R * np.cos(gamma) # dSigma

    dy = [
        dR,
        dSigma,
        (T-D)/mass - g * np.sin(gamma), # dV
        L / mass / v - g/v * np.cos(gamma) * (1 - v**2 / g / R), # dGamma
        dm
    ]

    return dy


    

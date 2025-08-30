import numpy as np
import ussa1976 as isa

# Constants
g_0 = 9.81 # m s^-2
mu_e = 3.5316000e12 # m^3 s^-2
R_0 = 600 # m

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
        rocket.I_sp = I_sp
        rocket.dm_p = dm_p
        rocket.A = A
        rocket.p_e = p_e
        rocket.S = S
        rocket.C_D0 = C_D0
        rocket.m_0 = m_0
        if m_min == None: rocket.m_min = 0.15 * m_0

# Class to create environment data
class env:
    def __init__(self,
                 ):
        env.p = lambda h : isa.compute(h, variables=['p'])
        env.rho = lambda h : isa.compute(h, variables=['rho'])

# Define integrator setup
class int_setup:
        def __init__(self, t0, tf, y0, method) -> None:
            int_setup.t0 = t0
            int_setup.tf = tf
            int_setup.y0 = y0
            int_setup.method = method

# Define propagator
class propagator:
    def __init__(self, rocket: rocket, env: env, funcSim, int_setup: int_setup):
        # Store inputs
        propagator.funcSim = funcSim
        propagator.rocket = rocket
        propagator.env = env
        propagator.int_setup = int_setup

    def solve(self):
        # Import integrator library
        from scipy import integrate
        # Recall parameters
        settings = propagator.int_setup
        # Define function to integrate
        def dy(t, y):
            return propagator.funcSim(t, y, propagator.rocket, propagator.env)
        # Integrate
        t, y = integrate.solve_ivp(dy, (settings.t0, settings.tf), settings.y0, settings.method)

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
    # Compute thrust magnitude
    T = rocket.I_sp * g_0 * rocket.dm_p
    # Compute drag magnitude
    D = 0.5 * env.rho(R - R_0) * v**2 * rocket.S * rocket.C_D0
    # Compute lift magnitude
    ### Note to self: no rotational model included yet: gravity turn ###
    L = 0
    
    dy = [
        v * np.sin(gamma), # dR
        -v/R * np.cos(gamma), # dSigma
        (T-D)/mass - g * np.sin(gamma), # dV
        L / mass / v - g/v * np.cos(gamma) * (1 - v**2 / g / R), # dGamma
        -rocket.dm_p # dM
    ]



    

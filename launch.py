# %% Imports
import utils
import numpy as np
import matplotlib.pyplot as plt

# Initial condition
y0 = np.array([600010, 0, 0.1, 1.5, 10000])

# Define integration settings
int_setup = utils.int_setup(
    t0 = 0,
    tf = 200,
    y0 = y0,
    method = "DOP853",
    max_step=0.05
)

# Define rocket
rocket = utils.rocket(dm_p=150, S=5, C_D0=0.1, m_min=4900)

# Define environment
environment = utils.env()

# Define propagator
propagator = utils.propagator(
    rocket=rocket,
    env=environment,
    funcSim=utils.Frocket,
    int_setup=int_setup
)

# %% Compute a simulation
t, y = propagator.solve()

# %% Visualize simulation
fig_debug = plt.figure()
ax = fig_debug.add_subplot(111)
R = y[:, 0]
sigma = -y[:, 1]
ax.plot(R * sigma, R)
ax.grid()
ax.set_ylim(600e3+1e1, 600e3+15)
ax.set_xlim(0, 5)

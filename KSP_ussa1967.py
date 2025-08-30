import numpy as np
p_0 = 101325.0 # Pa
T_0 = 288.15 # K
a = 6.5e-3 # K m^-1
g_0 = 9.80665 # m s^-2
Rs = 287.053 # J kg^-1 K^-1
h0 = g_0 / a / Rs # m
altitude_correction = 84852 / 70000

# Compute quantities
class compute:
    def __init__(self, h):
        if h < 0:
            raise Exception("Altitude must be 0m or greater")
        
        h = h * altitude_correction # Coherent with KSesP atmosphere limit

        T = 0
        p = 0
        rho = 0
        
        if h >= 0 and h < 11000:
            T = T_0 - a * h
            p = p_0 * (1 - a / T_0 * h) ** h0
            rho = p / Rs / T
        
        if h >= 11000 and h < 20000:
            T = 216.65
            p = 22632.06 * np.exp(-h0 * (h - 11e3) / T)
            rho = p / Rs / T
        
        if h >= 20000 and h < 32000:
            T = 196.65 + h*1e-3
            p = 5474.889 * (216.65 / (216.65 + 1e-3*(h - 20e3))) ** h0
            rho = p / Rs / T

        if h >= 32000 and h < 47000:
            T = 139.05 + 2.8e-3 * h
            p = 868.0187 * (228.65 / (228.65 + 2.8e-3 * (h - 32e3))) ** (h0 / 2.8)
            rho = p / Rs / T

        if h >= 47000 and h < 51000:
            T = 270.65
            p = 110.9063 * np.exp(-h0 * (h - 47e3) / T)
            rho = p / Rs / T

        if h >= 51000 and h < 71000:
            T = 413.45 - 2.8e-3 * h
            p = 66.93887 * (270.65 / (270.65 - 2.8e-3 * (h - 51e3))) ** ( -h0 / 2.8 )
            rho = p / Rs / T

        if h >= 71000 and h <= 84852:
            T = 356.65 - 2e-3 * h
            p = 3.956420 * (214.65 / (214.65 - 2e-3 * (h - 71e3))) ** (-h0 / 2)
            rho = p / Rs / T

        self.p = p
        self.T = T
        self.rho = rho
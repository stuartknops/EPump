import numpy as np
import math
from definePump import epump


def epumpoptimize(prop, deltaP, mdot, MR,Tamb):
    #inputs assumed to be same across pumps
    d_H = .023 #mm, from key sizing
    e_Rs = .002*1.25
    deltaP = deltaP * 6894.76
    
    # Fluid properties
    if prop == "rp1":
        rho = 811  # kg/m^3
        Q = mdot*(1+MR)
    elif prop == "lox":
        rho =  1140 # kg/m^3
        Q = mdot*MR/(1+MR)
    else:
        raise ValueError("Unknown propellant")
    H = deltaP/(rho*9.81)
    
    # Objective function
    def objective(x):
        # x = [n, deltaT]
        n = x[0]
        deltaT = x[1]
        p_all = (n/50000)*40

        ## Define first pump in order to get bearing circulation rate
        #1) size Impeller
        firstpump = epump(Q,n,H,rho,e_Rs)
        print(firstpump.p)

        p_draw = firstpump.p
        # Penalties
        if firstpump.d_2 > 100:
            p_draw += 1e6
        if firstpump.p / p_all > 0.85:
            p_draw += 1e6
        if deltaT > 20:
            p_draw += 1e6
        return p_draw
    return objective
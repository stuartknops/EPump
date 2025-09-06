import numpy as np
import math
from definePump import epumpClass
from defineBearings import bearingClass
from defineSeal import sealClass

# current parameters: ("rp1",460,6.17,2.23,273)
def optimize(prop, deltaP, mdot, MR,Tamb):
    #inputs assumed to be same across pumps
    d_H = .023 #m, from key sizing
    e_Rs = .002*1.25
    deltaP = deltaP * 6894.76
    d_w = .016 #from shaft/key sizing
    d_D = d_w #for axial force
    
    # Fluid properties
    if prop == "rp1":
        rho = 804.59  # kg/m^3
        Q = (mdot/(1+MR)*rho)
    elif prop == "lox":
        rho =  1140 # kg/m^3
        Q = mdot*MR/((1+MR)*rho)
    else:
        raise ValueError("Unknown propellant")
    H = deltaP/(rho*9.81)
    
    # Objective function
    def objective(x):
        # x = [n, deltaT]
        n = x[0]
        deltaT = x[1]
        p_all = (n/50000)*40 # in kW
        eta_V = .9 #only used in axial force calcs, for now an estimate, later from ratio of flowrates

        ## Define first pump in order to get bearing circulation rate
        #1) size Impeller
        firstpump = epumpClass(Q,n,H,rho,e_Rs,d_D,d_H,eta_V)
        print(f"d_2 is equal to {firstpump.d_2}")
        print(f"power is equal to {firstpump.p}")
        #2) select bearings based on rpm and forces. For now most calculations skipped because of selection complications and beam loading
        bearing = bearingClass(n,firstpump.f_ax)        

        eta_V = Q/((Q+bearing.Qdot)*1.03) # assuming 3% leak rate
        p_draw = firstpump.p/1000 #converting to kW
        # Penalties
        if firstpump.d_2 > .1:
            p_draw += 1e6
            print("a")
        if firstpump.p / p_all > 0.85:
            p_draw += 1e6
        if deltaT > 20:
            p_draw += 1e6
        return p_draw
    test = objective([23000,10])
    return test
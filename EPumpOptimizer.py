import numpy as np
import math
from defineImpeller import impellerClass
from defineBearings import bearingClass
from defineSeal import sealClass

# current parameters: ("rp1",460,6.17,2.23,273,135)
def optimize(prop, deltaP, mdot, MR,Tamb,p_tank):
    #inputs assumed to be same across pumps
    d_H = .023 #m, from key sizing
    e_Rs = .002*1.25
    deltaP = deltaP * 6894.76
    d_w = .016 #from shaft/key sizing
    d_D = d_w #for axial force
    
    # Fluid properties
    if prop == "rp1":
        rho = 804.59  # kg/m^3
        Q = mdot/((1+MR)*rho)
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
        eta_V = .95111944218 #only used in axial force calcs, for now an estimate, later from ratio of flowrates


        ## Define first pump in order to get bearing circulation rate
        #units here are very weird. Impeller and shaft in m, seal and bearing in mm
        #deltat in kelvin, pressures are inputted in psi, math in pa, math for bearing done in mpa.
        #1) size Impeller, do beam calcs to find radial forces on bearings
        impeller1 = impellerClass(Q,n,H,rho,e_Rs,d_D,d_H,eta_V)
        impeller1.summary()

        #2) select bearings based on rpm and forces. For now most calculations skipped because of selection complications and beam loading
        UpperBearing = bearingClass(n,"AC",impeller1.f_ax,Tamb,deltaT)     
        lowerBearing = bearingClass(n,"DG",impeller1.f_ax,0,0)
        #3) find heating on bearings, remember to incorporate deltaT's effect on viscosity.
        
        #4) size seals and find heating
        seal = sealClass(lowerBearing.d1,deltaP,p_tank)
        seal.powerLoss(n)
        seal.sealSummary()

        #6) find required florwate
        Qcooling = .000122 #temp
        #5)rerun impeller sizing with new mdot
        Qnew = Q + Qcooling
        eta_Vnew = Q/((Qnew)*1.03) # assuming 3% leak rate
        impeller2 = impellerClass(Qnew,n,H,rho,e_Rs,d_D,d_H,eta_Vnew)
        p_imp = impeller2.p/(1000) #converting to kW, apply hydraulic efficiency and leak rate
        #6) apply all power losses and efficiencies
        p_draw = (p_imp+ seal.p)/impeller2.eta_H*1.03
        # Penalties/constraints
        if impeller1.d_2 > .1:
            p_draw += 1e6
        if impeller1.p / p_all > 0.85:
            p_draw += 1e6
        if deltaT > 20 or deltaT < 2:
            p_draw += 1e6
        if lowerBearing.d1 > 24: #done in mm because that's what the bearing heating calcs are in
            p_draw += 1e6 # breaks the seal code rn. Also generally good, dont want seal face speeds to get too high.
        return p_draw
    test = objective([23000,10])

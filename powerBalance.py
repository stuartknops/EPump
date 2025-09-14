import numpy as np
import math
from defineImpeller import impellerClass
from defineBearings import bearingClass
from defineSeal import sealClass

def pumpPower(prop, deltaP, mdot, MR,Tamb,p_tank,n,deltaT):
        
    d_H = .023 #m, from key sizing
    e_Rs = .002*1.25
    deltaP = deltaP * 6894.76
    d_w = .016 #from shaft/key sizing
    d_D = d_w #for axial force
    
    # Fluid properties
    if prop == "rp1":
        rho = 804.59  # kg/m^3
        Q = mdot/((1+MR)*rho)
        Cp = 2050
    elif prop == "lox":
        rho =  1140 # kg/m^3
        Q = mdot*MR/((1+MR)*rho)
    else:
        raise ValueError("Unknown propellant")
    H = deltaP/(rho*9.81)
        
    p_all = (n/50000)*40 # in kW
    eta_V = .95111944218 #only used in axial force calcs, for now an estimate, later from ratio of flowrates


    ## Define first pump in order to get bearing circulation rate
    #units here are very weird. Impeller and shaft in m, seal and bearing in mm
    #deltat in kelvin, pressures are inputted in psi, math in pa, math for bearing done in mpa.
    #1) size Impeller, do beam calcs to find radial forces on bearings
    impeller1 = impellerClass(Q,n,H,rho,e_Rs,d_D,d_H,eta_V)
    impeller1.summary()

    #2) select bearings based on rpm and forces. For now most calculations skipped because of selection complications
    # assume design has same shaft dimensioning as model as of 9/13
    f_rlower = impeller1.f_r * 23/74
    f_rupper = f_rlower + impeller1.f_r
    upperBearing = bearingClass("AC",Tamb,deltaT)     
    lowerBearing = bearingClass("DG",0,0)
    upperBearing.heating("AC",n,impeller1.f_ax,f_rupper)
    lowerBearing.heating("DG",n,0,f_rlower)
    upperBearing.bearingSummary("AC",impeller1.f_ax,f_rupper)
    lowerBearing.bearingSummary("DG",0,f_rlower)
    #lowerBearing.bearingSummary()
    #3) find heating on bearings, remember to incorporate deltaT's effect on viscosity.

#4) size seals and find heating
    seal = sealClass(lowerBearing.d1,deltaP,p_tank)
    seal.powerLoss(n)
    seal.sealSummary()
    #6) find required florwate
    Mcooling = upperBearing.p/(Cp*deltaT) #temp
    Qcooling = Mcooling/rho
    #5)rerun impeller sizing with new mdot
    Qnew = Q + Qcooling
    eta_Vnew = Q/((Qnew)*1.03) # assuming 3% leak rate
    impeller2 = impellerClass(Qnew,n,H,rho,e_Rs,d_D,d_H,eta_Vnew)
    impeller2.summary()
    p_imp = impeller2.p/(1000) #converting to kW, apply hydraulic efficiency and leak rate
    #6) apply all power losses and efficiencies
    p_draw = (p_imp+ seal.p + upperBearing.p + lowerBearing.p)/(impeller2.eta_H*1.03)
    return p_draw
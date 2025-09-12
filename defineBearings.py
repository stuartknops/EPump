import math
class bearingClass:
    def __init__(self,n,bearingType,f_ax,t,dt):
        if bearingType.upper() == "AC":
            self.f = 1
            self.d1 = 20
            self.d2 = 47
            d_m = .5*(self.d1+self.d2)
            self.tb = t+dt
            self.v1 = y = 8*10**10*self.tb**-4.282
            kz = 4.4
            R1 = 4.33*(10**-7)
            R2 = 2.02
            R3 = 2.44 * (10**-12)

        elif bearingType.upper() == "DG":
            self.f = 1
            self.d1 = 20
        else:
            raise ValueError("Unknown bearing type")

    def heating(self):
        H = self.d2
    def bearingSummary(self,bearingType):
        if bearingType == "AC":
            print("=== Upper Bearing ===")
        else:
            print("=== Lower Bearing ===")
        print(f"Bearing Temp Tb: {self.tb:.4f} K")
        print(f"Viscosity V: {self.v1:.4f} mm^2/s")
        pass
    def bearingHeatSummary(self):
        pass
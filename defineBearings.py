import math
class bearingClass:
    def __init__(self,n,bearingType,f_ax):
        if bearingType.upper() == "AC":
            self.f = 1
        elif bearingType.upper() == "DG":
            self.f = 1
        else:
            raise ValueError("Unknown bearing type")

        
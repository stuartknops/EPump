import math
class impellerClass:
    def __init__(self,vdot,n,H,rho,e_Rs,d_D,d_H,eta_V):
        self.Q = vdot
        self.psi = 1.09
        self.n_q = n*(math.sqrt(vdot))*(H**(-3/4))
        self.d_2 = (84.6 / n) * math.sqrt(H / self.psi)
        if vdot <= 1:
            a = 1 
        elif vdot > 1:
            a = .5
        m = 0.1 * a * ((1/vdot)**(.15)) * ((45/self.n_q)**(0.06))
        eta_opt = 1 - (0.095*((1/vdot)**m)) - (.3*((.35 - math.log10(self.n_q/23))**2)*((1/vdot)**(.05)))
        m = 0.08 * a * ((1/vdot)**(.15)) * ((45/self.n_q)**(0.06))
        self.eta_H =  1 - (0.055*((1/vdot)**m)) - .2*((.26 - math.log10(self.n_q/25))**2)*((1/vdot)**(.1))
        s_ax = self.d_2*.035
        f_d1 = 1.15
        d_Hstar = d_H/self.d_2
        self.d_1 = self.d_2 * f_d1 * math.sqrt(d_Hstar **2 + 0.00148 * self.psi * self.n_q ** ( 4 / 3 ) / ( (eta_V) ** .67 ))
        d_sp = 2*(.001) + self.d_1 + 2*(e_Rs)
        self.f_ax = .9* rho * 9.81 * H * (math.pi/4) * (d_sp**2 - d_D**2)
        self.p = rho*9.81*H*vdot
        
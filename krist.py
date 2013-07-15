import math
import itertools
class Diamond:
    C = 9
    L = 8

    H = 1e-9
    CH3 = 1e-10
    dt =   0.01
    maxt = 100.0

    #Gleb Fake
    #T = 1200
    #k1 = 5.2e14 * math.exp(-6652.8/(1.98*T))*H
    #k2 = 2.0e13*H
    #k4 = 1e4*math.exp(-697.554/(1.98*T))
    #k4_1 = 1e4*math.exp(-697.554/(1.98*T))
    #k5 = 4.79e5 * math.exp(-14248.08/(1.98*T))
    #k6 = 1e16*CH3#1e13*CH3
    #k7 = 6.13e5 * math.exp(-36.17262/(1.98*T))
    #k8 = 0
    #k9 = 6.13e4 * math.exp(-36.17262/(1.98*T))

    #OUR Fake
    T = 1200
    k1 = 5.66e15 * math.exp(-3360/T)*H
    k2 = 2e13*H
    k4 = 1e1
    k4_1 = 20e2
    k5 = 0.01#4.79e13 * math.exp(-7196.8/T)
    k6 = 1e23*CH3#1e13*CH3
    k7 = 6.13e12*math.exp(-18.269/T)
    k8 = 0.5
    k9 = 3.5e21 * math.exp(-31.3/(1.98*T))

    #ORIGINAL
    #k1 = 5.2e13 * math.exp(-3360/T)
    #k2 = 2e13
    #k4 = 1e12 * math.exp(-352.3/T)
    #k5 = 4.79e13 * math.exp(-7196.8/T)
    #k6 = 1e13
    #k7 = 6.13e13 * math.exp(-18.269/T)
   # k8 = 0.5
    #k9 = 3.5e8 * math.exp(-31.3/(1.98*T))

    cc = []
    dc0 = []
    def __init__(self):
        for i in range(self.L):
            self.cc.append([0]* self.C)
            self.dc0.append([0]* self.C)

        self.cc[0][0] = 1

    def main_loop(self):
        vivod = 99
        for x in range(0, int(self.maxt / self.dt)):
            self.cc = self.RUN(self.cc)

            if (x%vivod == 0):    
                print'__________________________________', x+1, 'SHAG,',(x+1)*self.dt,'sec__________________________________'
                for l in range(0, self.L-1):
                    print l+1, 'SLOI ->',
                    v = 0
                    for j in range(0, self.C):
                        v += self.cc[l][j]
                        print "%i:%1.4e " % (j, self.cc[l][j]),
                    print "C = %1.2e" % v

     #       if (x%vivod == 0):    
     #           print'__________________________________', x+1, 'SHAG,',(x+1)*self.dt,'sec__________________________________'
     #           for l in range(0, self.L-1):
     #               v = 0
     #               print'___SLOI', l+1,'____'
     #               for j in range(0, self.C):
     #                   v += self.cc[l][j]
     #                   print self.cc[l][j]
     #               print "C =", v

    def RUN(self, c_prev):
        R, K1, K2, K3, K4 = [], [], [], [], []
        for j in range(0, self.L-1):
            R.append([0]*self.C)
            K1.append([0]*self.C)
            K2.append([0]*self.C)
            K3.append([0]*self.C)
            K4.append([0]*self.C)

        K1 = self.MUL(self.model(c_prev), self.dt)
        K2 = self.MUL(self.model(self.SUM(c_prev, self.DEL(K1, 2))), self.dt)
        K3 = self.MUL(self.model(self.SUM(c_prev, self.DEL(K2, 2))), self.dt)
        K4 = self.MUL(self.model(self.SUM(c_prev, K3)), self.dt)
       # print dc[0][0]
        R = self.SUM(c_prev, self.DEL(self.SUM(self.SUM(K1, self.MUL(K2, 2)), self.SUM(self.MUL(K3, 2), K4)), 6))

        return R

    def MUL(self, mass, m):
        for l in range(0, self.L - 1):
            for i in range(0, self.C):
                mass[l][i] = mass[l][i] * m
        return mass

    def SUM(self, a, b):
        for l in range(0, self.L - 1):
            for i in range(0, self.C):
                a[l][i] = a[l][i] + b[l][i]
        return a

    def DEL(self, d, e):
        for l in range(0,self.L - 1):
            for i in range(0, self.C):
                d[l][i] = d[l][i] / e
        return d

    def model(self, c_prev):
        dc = []
        for i in range(self.L):
           dc.append([0]*self.C)
        for l in range(0, self.L-1):
            for a in range(0, self.C):
                dc[l][a] = 0

        for l in range(0, self.L-1):
        # self.H = count_h(c_prev[l]) * ch
        # S = count_stars(c_prev[l]) * ch

            #Activacia
            #1
            dc[l][0] += (-self.k1 * c_prev[l][0] * self.H)
            dc[l][1] += (self.k1 * c_prev[l][0] * self.H)
            #2
            dc[l][1] += (-self.k1 * c_prev[l][1] * self.H)
            dc[l][2] += (self.k1 * c_prev[l][1] * self.H)
            #3
            dc[l][7] += (self.k1 * c_prev[l][8] * self.H)
            dc[l][8] += (-self.k1 * c_prev[l][8] * self.H)
    #        for i in range(0, C):
    #            print dc[l][i]

            #Deactivacia
            #1
            dc[l][0] += (self.k2 * c_prev[l][1] * self.H)
            dc[l][1] += (-self.k2 * c_prev[l][1] * self.H)
            #2
            dc[l][1] += (self.k2 * c_prev[l][2] * self.H)
            dc[l][2] += (-self.k2 * c_prev[l][2] * self.H)
            #3
            dc[l][7] += (-self.k2 * c_prev[l][7] * self.H)
            dc[l][8] += (self.k2 * c_prev[l][7] * self.H)
    #        for i in range(0, C):
    #            print dc[l][i]

            #Obr dimernoi svyazi
            #1
            dc[l][1] += (-self.k4_1 * c_prev[l][2] * c_prev[l][1])
            dc[l][2] += (-self.k4_1 * c_prev[l][2] * c_prev[l][1])
            dc[l][3] += (self.k4_1 * c_prev[l][2] * c_prev[l][1])
            dc[l][4] += (self.k4_1 * c_prev[l][2] * c_prev[l][1])
            #2
            dc[l][1] += (-self.k4 * c_prev[l][1] ** 2) *2
            dc[l][4] += (self.k4 * c_prev[l][1] ** 2) *2
            #3
            dc[l][2] += (-self.k4 * c_prev[l][2] ** 2) *2
            dc[l][3] += (self.k4 * c_prev[l][2] ** 2) *2
            #4
      #      print'""""', c_prev[l+1][0]
      #      print'""""', c_prev[l][1]
       #     print'""""', c_prev[l][7]
       #     print'""""', c_prev[l][8]

            dc[l][1] += (-self.k4 * c_prev[l][1] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][4] += (self.k4 * c_prev[l][1] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][5] += (self.k4 * c_prev[l][1] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][7] += (-self.k4 * c_prev[l][1] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
       #     print'""""', c_prev[l][5]
            #5
            dc[l][2] += (-self.k4 * c_prev[l][2] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][3] += (self.k4 * c_prev[l][2] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][5] += (self.k4 * c_prev[l][2] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][7] += (-self.k4 * c_prev[l][2] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
#            print'""""', c_prev[l][5]
 #           print '___'
            #6
            dc[l][1] += (-self.k4*c_prev[l][1]*c_prev[l][0])
            dc[l][0] += (-self.k4*c_prev[l][1]*c_prev[l][0])
            dc[l][4] += (self.k4*c_prev[l][1]*c_prev[l][0])*2



            #6
      #      dc[l][5] += (self.k4 * (c_prev[l][8] * c_prev[l+1][0] * c_prev[l][7]) ** 2)
      #      dc[l][7] += (-self.k4 * (c_prev[l][8] * c_prev[l+1][0] * c_prev[l][7]) ** 2)*2
    #        for i in range(0, C):
    #            print dc[l][i]
            #Razriv dimernoi svyazi
            #1
            dc[l][1] += (self.k5 * c_prev[l][3] * c_prev[l][4])
            dc[l][2] += (self.k5 * c_prev[l][3] * c_prev[l][4])
            dc[l][3] += (-self.k5 * c_prev[l][3] * c_prev[l][4])
            dc[l][4] += (-self.k5 * c_prev[l][3] * c_prev[l][4])
            #2
            dc[l][1] += (self.k5 * c_prev[l][4] ** 2)*2
            dc[l][4] += (-self.k5 * c_prev[l][4] ** 2)*2
            #3
            dc[l][2] += (self.k5 * c_prev[l][3] ** 2)*2
            dc[l][3] += (-self.k5 * c_prev[l][3] ** 2)*2
            #4
            dc[l][1] += (self.k5 * c_prev[l][4] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][4] += (-self.k5 * c_prev[l][4] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][5] += (-self.k5 * c_prev[l][4] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][7] += (self.k5 * c_prev[l][4] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
            #5
            dc[l][2] += (self.k5 * c_prev[l][3] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][3] += (-self.k5 * c_prev[l][3] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][5] += (-self.k5 * c_prev[l][3] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][7] += (self.k5 * c_prev[l][3] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
            #6
            dc[l][4] += (-self.k5 * (c_prev[l][4]) ** 2)*2
            dc[l][0] += (self.k5 * (c_prev[l][4] ** 2))
            dc[l][1] += (self.k5 * (c_prev[l][4] ** 2))
   #        for i in range(0, C):
     #           print dc[l][i]

            #Osagdenie metil-radikala
            #1
            dc[l+1][0] += (self.k6 * c_prev[l][4] * c_prev[l][3] * self.CH3)
            dc[l][3] += (-self.k6 * c_prev[l][4] * c_prev[l][3] * self.CH3)
            dc[l][4] += (-self.k6 * c_prev[l][4] * c_prev[l][3] * self.CH3)
            dc[l][8] += (self.k6 * c_prev[l][4] * c_prev[l][3] * self.CH3)*2
            #2
            dc[l+1][0] += (self.k6 * (c_prev[l][3] ** 2) * self.CH3)
            dc[l][3] += (-self.k6 * (c_prev[l][3] ** 2) * self.CH3)*2
            dc[l][7] += (self.k6 * (c_prev[l][3] ** 2) * self.CH3)
            dc[l][8] += (self.k6 * (c_prev[l][3] ** 2) * self.CH3)
            #3
            dc[l+1][0] += (self.k6 * c_prev[l][5] * c_prev[l][3] * self.CH3)
            dc[l][3] += (-self.k6 * c_prev[l][5] * c_prev[l][3] * self.CH3)
            dc[l][5] += (-self.k6 * c_prev[l][5] * c_prev[l][3] * self.CH3)
            dc[l][6] += (self.k6 * c_prev[l][5] * c_prev[l][3] * self.CH3)
            dc[l][8] += (self.k6 * c_prev[l][5] * c_prev[l][3] * self.CH3)

     #       for i in range(0, C):
     #           print dc[l][i]
            #Migracia mostovoi gruppi
            #1
            dc[l][6] += (self.k7 * (c_prev[l][7]**2)* c_prev[l][8]) + (-self.k7 * c_prev[l][6] * c_prev[l][7] * c_prev[l][1])
            dc[l][7] += (-self.k7 * (c_prev[l][7]**2)* c_prev[l][8]) + (self.k7 * c_prev[l][6] * c_prev[l][7] * c_prev[l][1])
            dc[l][8] += (-self.k7 * (c_prev[l][7]**2)* c_prev[l][8]) + (self.k7 * c_prev[l][6] * c_prev[l][7] * c_prev[l][1])
            #2
            dc[l][2] += (self.k7*(c_prev[l][7]**3)) + (-self.k7*c_prev[l][6]*c_prev[l][7]*c_prev[l][2])
            dc[l][6] += (self.k7 * c_prev[l][7]**3) + (-self.k7*c_prev[l][6]*c_prev[l][7]*c_prev[l][2])
            dc[l][7] += (-self.k7 * c_prev[l][7]**3)*2 + (self.k7*c_prev[l][6]*c_prev[l][7]*c_prev[l][2])*2

     #       for i in range(0, C):
     #           print dc[l][i]
            #Travlenie
            #1
            dc[l+1][0] += (-self.k8 * (c_prev[l][8]**2) * c_prev[l+1][0])
            dc[l][4] += (self.k8 * (c_prev[l][8]**2) * c_prev[l+1][0])*2
            dc[l][8] += (-self.k8 * (c_prev[l][8]**2) * c_prev[l+1][0])*2
            #2
            dc[l+1][0] += (-self.k8 * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][3] += (self.k8 * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][4] += (self.k8 * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][7] += (-self.k8 * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
            dc[l][8] += (-self.k8 * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
            #3
            dc[l+1][0] += (-self.k8 * c_prev[l][6]* c_prev[l+1][0] * c_prev[l][8])
            dc[l][6] += (-self.k8 * c_prev[l][6]* c_prev[l+1][0] * c_prev[l][8])
            dc[l][8] += (-self.k8 * c_prev[l][6]* c_prev[l+1][0] * c_prev[l][8])
            dc[l][3] += (self.k8 * c_prev[l][6]* c_prev[l+1][0] * c_prev[l][8])
            dc[l][5] += (self.k8 * c_prev[l][6]* c_prev[l+1][0] * c_prev[l][8])
     #       for i in range(0, C):
     #           print dc[l][i]
            #Migracia vverh
            #1
            dc[l+1][1] += (-self.k9 * c_prev[l][8] * c_prev[l+1][1] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)
            dc[l+1][4] += (self.k9 * c_prev[l][8] * c_prev[l+1][1] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)*2
            dc[l][2] += (-self.k9 * c_prev[l][8] * c_prev[l+1][1] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][8] * c_prev[l+1][1] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)*2
            #2
            dc[l+1][1] += (-self.k9 * c_prev[l][7] * c_prev[l+1][1] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)
            dc[l+1][4] += (self.k9 * c_prev[l][7] * c_prev[l+1][1] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)*2
            dc[l][2] += (-self.k9 * c_prev[l][7] * c_prev[l+1][1] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][7] * c_prev[l+1][1] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)*2
            #3
            dc[l+1][1] += (-self.k9 * c_prev[l][8] * c_prev[l+1][1] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)
            dc[l+1][4] += (self.k9 * c_prev[l][8] * c_prev[l+1][1] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)*2
            dc[l][2] += (-self.k9 * c_prev[l][8] * c_prev[l+1][1] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][8] * c_prev[l+1][1] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)*2
            #4
            dc[l+1][1] += (-self.k9 * c_prev[l][7] * c_prev[l+1][1] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)
            dc[l+1][4] += (self.k9 * c_prev[l][7] * c_prev[l+1][1] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)*2
            dc[l][2] += (-self.k9 * c_prev[l][7] * c_prev[l+1][1] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][7] * c_prev[l+1][1] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)*2
            #5
            dc[l+1][2] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)
            dc[l+1][4] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)
            dc[l+1][3] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)
            dc[l][2] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)*2
            #6
            dc[l+1][2] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)
            dc[l+1][4] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)
            dc[l+1][3] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)
            dc[l][2] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * (c_prev[l][2]**2)*self.CH3)*2
            #7
            dc[l+1][2] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)
            dc[l+1][4] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)
            dc[l+1][3] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)
            dc[l][2] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)*2
            #8
            dc[l+1][2] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)
            dc[l+1][4] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)
            dc[l+1][3] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)
            dc[l][2] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * (c_prev[l][2]**2)*self.CH3)*2
            #3
            dc[l+1][2] += (-self.k9 * c_prev[l][7]*c_prev[l+1][2]*(c_prev[l][7]**3)*self.CH3)
            dc[l][7] += (-self.k9 * c_prev[l][7]*c_prev[l+1][2]*(c_prev[l][7]**3)*self.CH3)*3
            dc[l+1][4] += (self.k9 * c_prev[l][7]*c_prev[l+1][2]*(c_prev[l][7]**3)*self.CH3)*2
            dc[l][6] += (self.k9 * c_prev[l][7]*c_prev[l+1][2]*(c_prev[l][7]**3)*self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][7]*c_prev[l+1][2]*(c_prev[l][7]**3)*self.CH3)
            #4
            dc[l+1][2] += (-self.k9 * c_prev[l][8]*c_prev[l+1][2]*(c_prev[l][7]**3)*self.CH3)
            dc[l][7] += (-self.k9 * c_prev[l][8]*c_prev[l+1][2]*(c_prev[l][7]**3)*self.CH3)*3
            dc[l+1][4] += (self.k9 * c_prev[l][8]*c_prev[l+1][2]*(c_prev[l][7]**3)*self.CH3)*2
            dc[l][6] += (self.k9 * c_prev[l][8]*c_prev[l+1][2]*(c_prev[l][7]**3)*self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][8]*c_prev[l+1][2]*(c_prev[l][7]**3)*self.CH3)
            #5
            #it = [q for q in itertools.product(c_prev[l][8],c_prev[l][7])]
            #for i in range():
            dc[l+1][2] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l][5] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l][3] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l+1][4] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][5] * c_prev[l][3] *self.CH3)*2
            dc[l][6] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l][8] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            #6
            dc[l+1][2] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l][5] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l][3] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l+1][4] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][5] * c_prev[l][3] *self.CH3)*2
            dc[l][6] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l][8] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            #7
            dc[l+1][2] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l][5] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l][3] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l+1][4] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][5] * c_prev[l][3] *self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l][6] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            #8
            dc[l+1][2] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l][5] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l][3] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l+1][4] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][5] * c_prev[l][3] *self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            dc[l][6] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][5] * c_prev[l][3] *self.CH3)
            #9
            dc[l+1][2] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][3] * c_prev[l][3] *self.CH3)
            dc[l][3] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][3] * c_prev[l][3] *self.CH3)*2
            dc[l+1][4] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][3] * c_prev[l][3] *self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][3] * c_prev[l][3] *self.CH3)*2
            #10
            dc[l+1][2] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][3] * c_prev[l][3] *self.CH3)
            dc[l][3] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][3] * c_prev[l][3] *self.CH3)*2
            dc[l+1][4] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][3] * c_prev[l][3] *self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][7] * c_prev[l][3] * c_prev[l][3] *self.CH3)*2
            #11
            dc[l+1][2] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][3] * c_prev[l][3] *self.CH3)
            dc[l][3] += (-self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][3] * c_prev[l][3] *self.CH3)*2
            dc[l+1][4] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][3] * c_prev[l][3] *self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][7] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][3] * c_prev[l][3] *self.CH3)*2
            #12
            dc[l+1][2] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][3] * c_prev[l][3] *self.CH3)
            dc[l][3] += (-self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][3] * c_prev[l][3] *self.CH3)*2
            dc[l+1][4] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][3] * c_prev[l][3] *self.CH3)*2
            dc[l][8] += (self.k9 * c_prev[l][8] * c_prev[l+1][2] * c_prev[l][8] * c_prev[l][3] * c_prev[l][3] *self.CH3)*2
            #13
     #       for i in range(0, C):
     #           print dc[l][i]
        #c_next[l][0] = (-self.k1*c_prev[l][0]*self.H + k2*c_prev[l][1]*S + k6*c_prev[l][4]*c_prev[l][3]*cch3*ch3 + k6*(c_prev[l][3]**2)*cch3*ch3 - k8*c_prev[l][8]*c_prev[l][0]*c_prev[l][7] - k8*(c_prev[l][7]**2)*c_prev[l][0])*dt + c_prev[l][0]
        #c_next[l][1] = (self.k1*c_prev[l][0]*self.H - self.k1*c_prev[l][1]*S + k2*c_prev[l][2]*S - k2*c_prev[l][1]*ch - self.k4*c_prev[l][1]*c_prev[l][2] - self.k4*(c_prev[l][1]**(2)) - self.k4*c_prev[l][1]*c_prev[l][7]*c_prev[l][0]*c_prev[l][8] + self.k5*c_prev[l][3]*c_prev[l][4] + k5*(c_prev[l][4]**(2)) + k5*c_prev[l][4]*c_prev[l][5]*c_prev[l][0]*c_prev[l][8])*dt + c_prev[l][1]
        #c_next[l][2] = (-k2*c_prev[l][2]*S + self.k1*c_prev[l][1]*S - self.k4*c_prev[l][2]*c_prev[l][1] - self.k4*c_prev[l][0]**2 + k5*c_prev[l][3]*c_prev[l][4] + k5*c_prev[l][3]**2)*dt + c_prev[l][2]
        #c_next[l][3] = (self.k4*c_prev[l][2]*c_prev[l][1] + self.k4*c_prev[l][2]**2 - k6*c_prev[l][4]*c_prev[l][3]*cch3*ch3 - k6*c_prev[l][3]*cch3*ch3 + k8*c_prev[l][8]*c_prev[l][0]*c_prev[l][7] + k8*c_prev[l][0]*c_prev[l][7]**2 - k5*c_prev[l][3]*c_prev[l][4] - k5*c_prev[l][3]**2)*dt + c_prev[l][3]
        #c_next[l][4] = (self.k4*c_prev[l][2]*c_prev[l][1] + self.k4*c_prev[l][1]**2 + k4*c_prev[l][1]*c_prev[l][7]*c_prev[l][0]*c_prev[l][8] - k6*c_prev[l][4]*c_prev[l][3]*cch3*ch3 + k8*c_prev[l][8]*c_prev[l][0]*c_prev[l][7] - k5*c_prev[l][3]*c_prev[l][4] - k5*c_prev[l][4]**2 - k5*c_prev[l][4]*c_prev[l][5]*c_prev[l][0]*c_prev[l][8])*dt + c_prev[l][4]
        #c_next[l][5] = (k4*c_prev[l][1]*c_prev[l][7]*c_prev[l][0]*c_prev[l][8] + k4*(c_prev[l][0]**2)*(c_prev[l][7]**2)*(c_prev[l][8]**2) - k5*c_prev[l][4]*c_prev[l][5]*c_prev[l][1]*c_prev[l][8] - k5*(c_prev[l][8]**2)*(c_prev[l][0]**2)*(c_prev[l][5]**2))*dt + c_prev[l][5]
        #c_next[l][6] = ( )*dt + c_prev[l][6]
        #c_next[l][7] = (-k4*c_prev[l][1]*c_prev[l][7]*c_prev[l][0]*c_prev[l][8] - k4*(c_prev[l][0]**2)*(c_prev[l][7]**2)*(c_prev[l][8]**2) + k6*c_prev[l][4]*c_prev[l][3]*cch3*ch3 + k6*(c_prev[l][3]**2)*cch3*ch3 + k5*c_prev[l][4]*c_prev[l][5]*c_prev[l][0]*c_prev[l][8] + k5*(c_prev[l][8]**2)*(c_prev[l][0]**2)*(c_prev[l][5]**2))*dt + c_prev[l][7]
        #c_next[l][8] = (k6*c_prev[l][4]*c_prev[l][3]*cch3*ch3 - k8*c_prev[l][8]*c_prev[l][0]*c_prev[l][7] )*dt + c_prev[l][8]
        return dc
d = Diamond()
d.main_loop()


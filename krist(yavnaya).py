import math
import decimal
C = 9
L = 4

c_prev = []
dc = []
for i in range(L):
    c_prev.append([0]*C)
    dc.append([0]*C)
c_prev[0][0] = 1

H = 10e-9
CH3 = 10e-10
dt =   0.001
maxt = 1
T = 1200

k1 = 5.2e13*  math.exp(-3360/T)
k2 = 2e13
k4 = 1e12 * math.exp(-352.3/T)
k5 = 4.79e13 * math.exp(-7196.8/T)
k6 = 1e13
k7 = 6.13e13 * math.exp(-18.269/T)
k8 = 0.5
k9 = 3.5e8 * math.exp(-31.3/(1.98*T))

# def count_h(c):
#     hn = 2 * c[0] + c[1] + c[4] + c[8]
#     mhn = 2 * sum(c)
#     return hn / mhn
#
# def count_stars(c):
#     sn = 2 * c[2] + c[1] + c[3] + c[7]
#     msn = 2 * sum(c)
#     return sn / msn

for x in range(0, int(maxt / dt)):
    print'__________________________________', x+1, 'SHAG,',(x+1)*dt,'sec__________________________________'

    for l in range(0, L-1):
        for a in range(0, C):
            dc[l][a] = 0

    for l in range(0, L-1):
    # H = count_h(c_prev[l]) * ch
    # S = count_stars(c_prev[l]) * ch

    #Activacia
        #1
        dc[l][0] += (-k1 * c_prev[l][0] * H)
        dc[l][1] += (k1 * c_prev[l][0] * H)
        #2
        dc[l][1] += (-k1 * c_prev[l][1] * H)
        dc[l][2] += (k1 * c_prev[l][1] * H)
        #3
        dc[l][7] += (k1 * c_prev[l][8] * H)
        dc[l][8] += (-k1 * c_prev[l][8] * H)
        #        for i in range(0, C):
        #            print dc[l][i]

        #Deactivacia
        #1
        dc[l][0] += (k2 * c_prev[l][1] * H)
        dc[l][1] += (-k2 * c_prev[l][1] * H)
        #2
        dc[l][1] += (k2 * c_prev[l][2] * H)
        dc[l][2] += (-k2 * c_prev[l][2] * H)
        #3
        dc[l][7] += (-k2 * c_prev[l][7] * H)
        dc[l][8] += (k2 * c_prev[l][7] * H)
        #        for i in range(0, C):
        #            print dc[l][i]

        #Obr dimernoi svyazi
        #1
        dc[l][1] += (-k4 * c_prev[l][2] * c_prev[l][1])
        dc[l][2] += (-k4 * c_prev[l][2] * c_prev[l][1])
        dc[l][3] += (k4 * c_prev[l][2] * c_prev[l][1])
        dc[l][4] += (k4 * c_prev[l][2] * c_prev[l][1])
        #2
        dc[l][1] += (-k4 * c_prev[l][1] ** 2) *2
        dc[l][4] += (k4 * c_prev[l][1] ** 2) *2
        #3
        dc[l][2] += (-k4 * c_prev[l][2] ** 2) *2
        dc[l][3] += (k4 * c_prev[l][2] ** 2) *2
        #4
        #      print'""""', c_prev[l+1][0]
        #      print'""""', c_prev[l][1]
        #     print'""""', c_prev[l][7]
        #     print'""""', c_prev[l][8]

        dc[l][1] += (-k4 * c_prev[l][1] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][4] += (k4 * c_prev[l][1] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][5] += (k4 * c_prev[l][1] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][7] += (-k4 * c_prev[l][1] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        #     print'""""', c_prev[l][5]
        #5
        dc[l][2] += (-k4 * c_prev[l][2] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][3] += (k4 * c_prev[l][2] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][5] += (k4 * c_prev[l][2] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][7] += (-k4 * c_prev[l][2] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        #            print'""""', c_prev[l][5]
        #           print '___'
        #6
        dc[l][1] += (-k4*c_prev[l][1]*c_prev[l][0])
        dc[l][0] += (-k4*c_prev[l][1]*c_prev[l][0])
        dc[l][4] += (k4*c_prev[l][1]*c_prev[l][0])*2



        #6
        #      dc[l][5] += (k4 * (c_prev[l][8] * c_prev[l+1][0] * c_prev[l][7]) ** 2)
        #      dc[l][7] += (-k4 * (c_prev[l][8] * c_prev[l+1][0] * c_prev[l][7]) ** 2)*2
        #        for i in range(0, C):
        #            print dc[l][i]
        #Razriv dimernoi svyazi
        #1
        dc[l][1] += (k5 * c_prev[l][3] * c_prev[l][4])
        dc[l][2] += (k5 * c_prev[l][3] * c_prev[l][4])
        dc[l][3] += (-k5 * c_prev[l][3] * c_prev[l][4])
        dc[l][4] += (-k5 * c_prev[l][3] * c_prev[l][4])
        #2
        dc[l][1] += (k5 * c_prev[l][4] ** 2)*2
        dc[l][4] += (-k5 * c_prev[l][4] ** 2)*2
        #3
        dc[l][2] += (k5 * c_prev[l][3] ** 2)*2
        dc[l][3] += (-k5 * c_prev[l][3] ** 2)*2
        #4
        dc[l][1] += (k5 * c_prev[l][4] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][4] += (-k5 * c_prev[l][4] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][5] += (-k5 * c_prev[l][4] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][7] += (k5 * c_prev[l][4] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
        #5
        dc[l][2] += (k5 * c_prev[l][3] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][3] += (-k5 * c_prev[l][3] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][5] += (-k5 * c_prev[l][3] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][7] += (k5 * c_prev[l][3] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8])
        #6
        dc[l][4] += (-k5 * (c_prev[l][4]) ** 2)*2
        dc[l][0] += (k5 * (c_prev[l][4] ** 2))
        dc[l][1] += (k5 * (c_prev[l][4] ** 2))
        #        for i in range(0, C):
        #           print dc[l][i]

        #Osagdenie metil-radikala
        #1
        dc[l+1][0] += (k6 * c_prev[l][4] * c_prev[l][3] * CH3)
        dc[l][3] += (-k6 * c_prev[l][4] * c_prev[l][3] * CH3)
        dc[l][4] += (-k6 * c_prev[l][4] * c_prev[l][3] * CH3)
        dc[l][8] += (k6 * c_prev[l][4] * c_prev[l][3] * CH3)*2
        #2
        dc[l+1][0] += (k6 * (c_prev[l][3] ** 2) * CH3)
        dc[l][3] += (-k6 * (c_prev[l][3] ** 2) * CH3)*2
        dc[l][7] += (k6 * (c_prev[l][3] ** 2) * CH3)
        dc[l][8] += (k6 * (c_prev[l][3] ** 2) * CH3)
        #3
        dc[l+1][0] += (k6 * c_prev[l][5] * c_prev[l][3] * CH3)
        dc[l][3] += (-k6 * c_prev[l][5] * c_prev[l][3] * CH3)
        dc[l][5] += (-k6 * c_prev[l][5] * c_prev[l][3] * CH3)
        dc[l][6] += (k6 * c_prev[l][5] * c_prev[l][3] * CH3)
        dc[l][8] += (k6 * c_prev[l][5] * c_prev[l][3] * CH3)

        #       for i in range(0, C):
        #           print dc[l][i]
        #Migracia mostovoi gruppi
        #1
        dc[l][6] += (k7 * (c_prev[l][7]**2)* c_prev[l][8]) + (-k7 * c_prev[l][6] * c_prev[l][7] * c_prev[l][1])
        dc[l][7] += (-k7 * (c_prev[l][7]**2)* c_prev[l][8]) + (k7 * c_prev[l][6] * c_prev[l][7] * c_prev[l][1])
        dc[l][8] += (-k7 * (c_prev[l][7]**2)* c_prev[l][8]) + (k7 * c_prev[l][6] * c_prev[l][7] * c_prev[l][1])
        #2
        dc[l][2] += (k7*(c_prev[l][7]**3)) + (-k7*c_prev[l][6]*c_prev[l][7]*c_prev[l][2])
        dc[l][6] += (k7 * c_prev[l][7]**3) + (-k7*c_prev[l][6]*c_prev[l][7]*c_prev[l][2])
        dc[l][7] += (-k7 * c_prev[l][7]**3)*2 + (k7*c_prev[l][6]*c_prev[l][7]*c_prev[l][2])*2

        #       for i in range(0, C):
        #           print dc[l][i]
        #Travlenie
        #1
        dc[l+1][0] += (-k8 * (c_prev[l][8]**2) * c_prev[l+1][0])
        dc[l][4] += (k8 * (c_prev[l][8]**2) * c_prev[l+1][0])*2
        dc[l][8] += (-k8 * (c_prev[l][8]**2) * c_prev[l+1][0])*2
        #2
        dc[l+1][0] += (-k8 * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][3] += (k8 * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][4] += (k8 * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][7] += (-k8 * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        dc[l][8] += (-k8 * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8])
        #3
        dc[l+1][0] += (-k8 * c_prev[l][6]* c_prev[l+1][0] * c_prev[l][8])
        dc[l][6] += (-k8 * c_prev[l][6]* c_prev[l+1][0] * c_prev[l][8])
        dc[l][8] += (-k8 * c_prev[l][6]* c_prev[l+1][0] * c_prev[l][8])
        dc[l][3] += (k8 * c_prev[l][6]* c_prev[l+1][0] * c_prev[l][8])
        dc[l][5] += (k8 * c_prev[l][6]* c_prev[l+1][0] * c_prev[l][8])

        #       for i in range(0, C):
        #           print dc[l][i]
        #Migracia vverh
        #1
        dc[l+1][1] += (-k9 * c_prev[l+1][1] * (c_prev[l][2]**2)*CH3)
        dc[l+1][4] += (k9 * c_prev[l+1][1] * (c_prev[l][2]**2)*CH3)*2
        dc[l][2] += (-k9 * c_prev[l+1][1] * (c_prev[l][2]**2)*CH3)*2
        #2
        dc[l+1][2] += (-k9 * c_prev[l+1][2] * (c_prev[l][2]**2)*CH3)
        dc[l+1][3] += (k9 * c_prev[l+1][2] * (c_prev[l][2]**2)*CH3)
        dc[l+1][4] += (k9 * c_prev[l+1][2] * (c_prev[l][2]**2)*CH3)
        dc[l][2] += (-k9 * c_prev[l+1][2] * (c_prev[l][2]**2)*CH3)*2
        #       for i in range(0, C):
        #           print dc[l][i]
        #c_next[l][0] = (-k1*c_prev[l][0]*self.H + k2*c_prev[l][1]*S + k6*c_prev[l][4]*c_prev[l][3]*cch3*ch3 + k6*(c_prev[l][3]**2)*cch3*ch3 - k8*c_prev[l][8]*c_prev[l][0]*c_prev[l][7] - k8*(c_prev[l][7]**2)*c_prev[l][0])*dt + c_prev[l][0]
        #c_next[l][1] = (k1*c_prev[l][0]*self.H - k1*c_prev[l][1]*S + k2*c_prev[l][2]*S - k2*c_prev[l][1]*ch - k4*c_prev[l][1]*c_prev[l][2] - k4*(c_prev[l][1]**(2)) - k4*c_prev[l][1]*c_prev[l][7]*c_prev[l][0]*c_prev[l][8] + k5*c_prev[l][3]*c_prev[l][4] + k5*(c_prev[l][4]**(2)) + k5*c_prev[l][4]*c_prev[l][5]*c_prev[l][0]*c_prev[l][8])*dt + c_prev[l][1]
        #c_next[l][2] = (-k2*c_prev[l][2]*S + k1*c_prev[l][1]*S - k4*c_prev[l][2]*c_prev[l][1] - k4*c_prev[l][0]**2 + k5*c_prev[l][3]*c_prev[l][4] + k5*c_prev[l][3]**2)*dt + c_prev[l][2]
        #c_next[l][3] = (k4*c_prev[l][2]*c_prev[l][1] + k4*c_prev[l][2]**2 - k6*c_prev[l][4]*c_prev[l][3]*cch3*ch3 - k6*c_prev[l][3]*cch3*ch3 + k8*c_prev[l][8]*c_prev[l][0]*c_prev[l][7] + k8*c_prev[l][0]*c_prev[l][7]**2 - k5*c_prev[l][3]*c_prev[l][4] - k5*c_prev[l][3]**2)*dt + c_prev[l][3]
        #c_next[l][4] = (k4*c_prev[l][2]*c_prev[l][1] + k4*c_prev[l][1]**2 + k4*c_prev[l][1]*c_prev[l][7]*c_prev[l][0]*c_prev[l][8] - k6*c_prev[l][4]*c_prev[l][3]*cch3*ch3 + k8*c_prev[l][8]*c_prev[l][0]*c_prev[l][7] - k5*c_prev[l][3]*c_prev[l][4] - k5*c_prev[l][4]**2 - k5*c_prev[l][4]*c_prev[l][5]*c_prev[l][0]*c_prev[l][8])*dt + c_prev[l][4]
        #c_next[l][5] = (k4*c_prev[l][1]*c_prev[l][7]*c_prev[l][0]*c_prev[l][8] + k4*(c_prev[l][0]**2)*(c_prev[l][7]**2)*(c_prev[l][8]**2) - k5*c_prev[l][4]*c_prev[l][5]*c_prev[l][1]*c_prev[l][8] - k5*(c_prev[l][8]**2)*(c_prev[l][0]**2)*(c_prev[l][5]**2))*dt + c_prev[l][5]
        #c_next[l][6] = ( )*dt + c_prev[l][6]
        #c_next[l][7] = (-k4*c_prev[l][1]*c_prev[l][7]*c_prev[l][0]*c_prev[l][8] - k4*(c_prev[l][0]**2)*(c_prev[l][7]**2)*(c_prev[l][8]**2) + k6*c_prev[l][4]*c_prev[l][3]*cch3*ch3 + k6*(c_prev[l][3]**2)*cch3*ch3 + k5*c_prev[l][4]*c_prev[l][5]*c_prev[l][0]*c_prev[l][8] + k5*(c_prev[l][8]**2)*(c_prev[l][0]**2)*(c_prev[l][5]**2))*dt + c_prev[l][7]
        #c_next[l][8] = (k6*c_prev[l][4]*c_prev[l][3]*cch3*ch3 - k8*c_prev[l][8]*c_prev[l][0]*c_prev[l][7] )*dt + c_prev[l][8]

    v= 0
    for l in range(0, L-1):
        print '________', l+1,'SLOI ________'
        for j in range(0, C):
            c_prev[l][j] += dc[l][j] * dt
            v += c_prev[l][j]
            print c_prev[l][j]
        print v

#print decimal.Decimal(9.53)
# encoding: utf-8

import math
import itertools
class Diamond:
    C = 9
    L = 7

    H = 1e-9
    CH3 = 1e-10
    dt = 0.01
    maxt = 50.01

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

    #OUR Fake #2
    # T = 1200
    # k1 = 2.5e5 # активация
    # k2 = 1e5 # дезактивация
    # k4 = 1e1 # обр. димерной связи
    # k4_1 = k4 * 10 # обр. димерной связи (быстрая)
    # k4_2 = k4 * 0.1 # обр. димерной связи (медленная)
    # k5 = 1 # разрыв димерной связи
    # k6 = 1e4 # осаждение метил-радикала
    # k7 = 1e13 # миграция мостовой группы
    # k8 = 0.5 # травление
    # k9 = 1e17 # миграция вниз

# 0 ->  CH2
# 1 ->  *CH
# 2 ->  **C
# 3 ->  *C-
# 4 ->  -CH
# 5 ->  -C/
# 6 ->  \C/
# 7 ->  *C/
# 8 ->  \CH

    #OUR Fake
    T = 1200
    k1 = 5.66e15 * math.exp(-3360/T) * H
    k2 = 2e13 * H
    k4 = 1e1
    k4_1 = 20e2
    k4_2 = 5
    k5 = 0.01 #4.79e13 * math.exp(-7196.8/T)
    k6 = 1e23 * CH3 #1e13*CH3
    k7 = 6.13e12 * math.exp(-18.269/T)
    k8 = 0.5
    k9 = 3.5e21 * math.exp(-31.3/(1.98*T))

    #ORIGINAL
    # k1 = 5.2e13 * H * math.exp(-3360/T)
    # k2 = 2e13 * H
    # k4 = 1e12 * math.exp(-352.3/T)
    # k4_1 = k4 * 10
    # k5 = 4.79e13 * math.exp(-7196.8/T)
    # k6 = 1e13 * CH3
    # k7 = 6.13e13 * math.exp(-18.269/T)
    # k8 = 0.5
    # k9 = 3.5e8 * math.exp(-31.3/(1.98*T))

    cc = []
    def __init__(self):
        for i in range(self.L):
            self.cc.append([0] * self.C)

        self.cc[0][0] = 1

    def main_loop(self):
        vivod = 100
        f = open("c:/C-Krist.dat","w")
        for x in range(0, int(self.maxt / self.dt)):
            self.cc = self.RUN(self.cc)

            if (x%vivod == 0):
                toel = [0] * self.C
                print'\n__________________________________', x+1, 'SHAG,',(x+1)*self.dt,'sec__________________________________'
                f.write("#_______________________________")
                f.write(str(x+1))
                f.write(" SHAG, ")
                f.write(str((x+1)*self.dt))
                f.write(" sec_______________________________\n")
                for l in range(0, self.L-1):
                    print l+1, 'SLOI->',
                    v = 0
                    f.write('# ')
                    f.write(str(l))
                    f.write(' Sloi->\t')
                    for j in range(0, self.C):
                        toel[j] += self.cc[l][j]
                        v += self.cc[l][j]
                        print "%i:%1.4e " % (j, self.cc[l][j]),

                        f.write(str("%1.4e " % (self.cc[l][j])))
                        f.write(" ")
                    f.write("\n")
                    print "C = %1.2e" % v
                print ' TOTAL ->',
                f.write("TOTAL-> ")
                f.write(str((x+1)*self.dt))
                f.write('\t')
                for j in range(0, self.C):
                    print "%i:%1.4e " % (j, toel[j]),
                    f.write(str("%1.4e  " % (toel[j])))
                print
                f.write('\n')
        f.close()

    def RUN(self, c_prev):
        K1 = self.MUL(self.model(c_prev), self.dt)
        K2 = self.MUL(self.model(self.SUM(c_prev, self.DEL(K1, 2))), self.dt)
        K3 = self.MUL(self.model(self.SUM(c_prev, self.DEL(K2, 2))), self.dt)
        K4 = self.MUL(self.model(self.SUM(c_prev, K3)), self.dt)
        return self.SUM(c_prev, self.DEL(self.SUM(self.SUM(K1, self.MUL(K2, 2)), self.SUM(self.MUL(K3, 2), K4)), 6))

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

    # 0 ->  CH2
    # 1 ->  *CH
    # 2 ->  **C
    # 3 ->  *C-
    # 4 ->  -CH
    # 5 ->  -C/
    # 6 ->  \C/
    # 7 ->  *C/
    # 8 ->  \CH

            #Activacia
            #1
            rate = self.k1 * c_prev[l][0] * self.H
            dc[l][0] += -rate
            dc[l][1] += rate
            #2
            rate = self.k1 * c_prev[l][1] * self.H
            dc[l][1] += -rate
            dc[l][2] += rate
            #3
            rate = self.k1 * c_prev[l][8] * self.H
            dc[l][7] += rate
            dc[l][8] += -rate

            #Deactivacia
            #1
            rate = self.k2 * c_prev[l][1] * self.H
            dc[l][0] += rate
            dc[l][1] += -rate
            #2
            rate = self.k2 * c_prev[l][2] * self.H
            dc[l][1] += rate
            dc[l][2] += -rate
            #3
            rate = self.k2 * c_prev[l][7] * self.H
            dc[l][7] += -rate
            dc[l][8] += rate

            #Obr dimernoi svyazi
            #1
            rate = self.k4_1 * c_prev[l][2] * c_prev[l][1]
            dc[l][1] += -rate
            dc[l][2] += -rate
            dc[l][3] += rate
            dc[l][4] += rate
            #2
            rate = self.k4 * (c_prev[l][1] ** 2)
            dc[l][1] += -rate * 2
            dc[l][4] += rate * 2
            #3
            rate = self.k4_1 * (c_prev[l][2] ** 2)
            dc[l][2] += -rate * 2
            dc[l][3] += rate *2
            #4
            for a in [1, 2]:
                rate = self.k4_2 * c_prev[l][a] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8]
                dc[l][a] += -rate
                if a == 1:
                    dc[l][4] += rate
                else:
                    dc[l][3] += rate
                dc[l][5] += rate
                dc[l][7] += -rate
            #6
            rate = self.k4 * c_prev[l][1]*c_prev[l][0]
            dc[l][1] += -rate
            dc[l][0] += -rate
            dc[l][4] += rate *2

            #Razriv dimernoi svyazi
            #1
            rate = self.k5 * c_prev[l][3] * c_prev[l][4]
            dc[l][1] += rate
            dc[l][2] += rate
            dc[l][3] += -rate
            dc[l][4] += -rate
            #2
            rate = self.k5 * (c_prev[l][4] ** 2)
            dc[l][1] += rate * 2
            dc[l][4] += -rate * 2
            #3
            rate = self.k5 * (c_prev[l][3] ** 2)
            dc[l][2] += rate * 2
            dc[l][3] += (-rate) * 2
            #4
            for a in [4, 3]:
                rate = self.k5 * c_prev[l][a] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8]
                if a == 4:
                    dc[l][1] += rate
                else:
                    dc[l][2] += rate
                dc[l][a] += -rate
                dc[l][5] += -rate
                dc[l][7] += rate

            #Osagdenie metil-radikala
            #1
            rate = self.k6 * c_prev[l][4] * c_prev[l][3] * self.CH3
            dc[l+1][0] += rate
            dc[l][3] += -rate
            dc[l][4] += -rate
            dc[l][8] += rate * 2
            #2
            rate = self.k6 * (c_prev[l][3] ** 2) * self.CH3
            dc[l+1][0] += rate
            dc[l][3] += -rate * 2
            dc[l][7] += rate
            dc[l][8] += rate
            #3
            rate = self.k6 * c_prev[l][5] * c_prev[l][3] * self.CH3
            dc[l+1][0] += rate
            dc[l][3] += -rate
            dc[l][5] += -rate
            dc[l][6] += rate
            dc[l][8] += rate

            #Migracia mostovoi gruppi
            for a in [0, 1, 2]:
                #1
                rate1 = self.k7 * (c_prev[l][7]**2) * c_prev[l][8] * c_prev[l+1][a]
                rate2 = self.k7 * c_prev[l][6] * c_prev[l][7] * c_prev[l][1] * c_prev[l+1][a]
                dc[l][6] += rate1 + (-rate2)
                dc[l][7] += -rate1 + rate2
                dc[l][8] += -rate1 + rate2
                #2
                rate1 = self.k7 * (c_prev[l][7]**3) * c_prev[l+1][a]
                rate2 = self.k7 * c_prev[l][6] * c_prev[l][7] * c_prev[l][2] * c_prev[l+1][a]
                dc[l][2] += rate1 + (-rate2)
                dc[l][6] += rate1 + (-rate2)
                dc[l][7] += (-rate1 + rate2) * 2

            #Travlenie
            #1
            rate = self.k8 * (c_prev[l][8]**2) * c_prev[l+1][0]
            dc[l+1][0] += -rate
            dc[l][3] += rate
            dc[l][4] += rate
            dc[l][8] += -rate * 2
            #2
            rate = self.k8 * c_prev[l][7] * c_prev[l][8] * c_prev[l+1][0]
            dc[l+1][0] += -rate
            dc[l][3] += rate * 2
            dc[l][7] += -rate
            dc[l][8] += -rate
            #3
            rate = self.k8 * c_prev[l][6] * c_prev[l][8] * c_prev[l+1][0]
            dc[l+1][0] += -rate
            dc[l][3] += rate
            dc[l][5] += rate
            dc[l][6] += -rate
            dc[l][8] += -rate

            # TODO: миграция вниз не учитывает атомов входящих в структуры, которые изменяются посредством миграции
            # последнее упоминание по циклах перебора см. в коммите f88c420dd1f425442494aade8a019c295c0208b4
            #Migracia вниз
            for a in [1, 2]:
                rate = self.k9 * c_prev[l+1][a] * (c_prev[l][2]**2) * self.CH3
                dc[l+1][a] += -rate
                if a == 1:
                    dc[l+1][4] += rate * 2
                else:
                    dc[l+1][3] += rate
                    dc[l+1][4] += rate
                dc[l][2] += -rate * 2
                dc[l][8] += rate * 2

            rate = self.k9 * c_prev[l+1][2] * (c_prev[l][7]**3) * self.CH3
            dc[l+1][2] += -rate
            dc[l+1][4] += rate * 2
            dc[l][6] += rate * 2
            dc[l][7] += -rate * 3
            dc[l][8] += rate

            rate = self.k9 * c_prev[l+1][2] * c_prev[l][5] * c_prev[l][3] * self.CH3
            dc[l+1][2] += -rate
            dc[l+1][4] += rate * 2
            dc[l][3] += -rate
            dc[l][5] += -rate
            dc[l][6] += rate
            dc[l][8] += rate

            for a in [1, 2]:
                rate = self.k9 * c_prev[l+1][a] * (c_prev[l][3]**2) * self.CH3
                dc[l+1][a] += -rate
                dc[l][3] += -rate * 2
                if a == 1:
                    dc[l+1][4] += rate * 2
                else:
                    dc[l+1][3] += rate
                    dc[l+1][4] += rate
                dc[l][8] += rate * 2

        return dc

d = Diamond()
d.main_loop()

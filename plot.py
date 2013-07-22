# encoding: utf-8
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt

class Plot:
    totals = []
    times = []

    def addtotal(self, total, time):
        self.totals.append(total)
        self.times.append(time)

    def draw(self):
        mpl.rcParams['font.family'] = 'fantasy'
        mpl.rcParams['font.fantasy'] = 'Comic Sans MS, Arial'
        plt.title(u'График роста концентраций')
        plt.xlabel(u'Время, t')
        plt.ylabel(u'Концентрация, С')
        plt.yscale('log')
        plt.grid()

        lts = ['r-', 'b-', 'g-', 'r^:', 'b^:', 'g^:', 'r*:', 'b*:', 'g*:']

        lines = []
        tt = numpy.array(self.totals).T
        for concs, lt in zip(tt, lts):
            line = plt.plot(self.times, concs, lt)[0]
            lines.append(line)

        names = ['CH2', '*CH', '**C', '*C-', '-CH', '-C/', '\C/', '*C/', '\CH']
        plt.legend(lines, names, loc='best')

        plt.show()






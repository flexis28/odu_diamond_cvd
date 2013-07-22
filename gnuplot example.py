import Gnuplot
import numpy
import math
#Create some data
#x = numpy.linspace(0,10,100)
x = numpy.arange(100)
print x
y1 = x ** 2
#y2 = 10 * numpy.sin(math.pi * x)
#Instantiate Gnuplot object
g = Gnuplot.Gnuplot(persist=1)
#Create the Gnuplot data
d1 = Gnuplot.Data(2, 1)
#d2 = Gnuplot.Data(x, y2, with_='l', title='d2')
#Formatting option
#g('set grid')
#g('set key left ')
#Plot
g.plot(d1)

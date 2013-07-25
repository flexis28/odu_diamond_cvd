import std.stdio;
import std.math;

import genetic.genetic_algorithm;
import genetic.population;
import genetic.rate_population;
import ode;

void main() {

    //auto first = new RatePopulation(
    //    5.2e13 * Ode.H * exp(-3360/Ode.T),
    //    2e13 * Ode.H,
    //    1e1,
    //    0,
    //    1e13 * Ode.CH3,
    //    6.13e13 * exp(-18.269/Ode.T),
    //    0,
    //    3.5e8 * exp(-31300/(1.98*Ode.T)),
    //);

    auto first = new RatePopulation(
        1.21299e+08,  // 1
        34893.6,                   // 2
        586.571, // e12 * exp(-352.3/T),       // 4
        0.423981, // 4.79e13 * exp(-7196.8/T),   // 5
        1000,                 // 6
        3.0559e+21,   // 7
        0, //0.5,                        // 8
        3.32977e+07, // 9
    );

//1.27207e+08 0 1072.57 0 1000 3.61328e+20 0 3.87657e+08

    //auto first = new RatePopulation(
    //    4.54755e+09   0 1000 1.07729e+19 0 57.0281
    //    6771.63,  // 1
    //    84.2457,                   // 2
    //    0, // e12 * exp(-352.3/T),       // 4
    //    0.913916, // 4.79e13 * exp(-7196.8/T),   // 5
    //    1000,                 // 6
    //    1.07729e+19,   // 7
    //    0, //0.5,                        // 8
    //    57.0281, // 9
    //);

    auto ga = new GeneticAlgorithm(0.3, 0.1, first, 50);
    auto best = ga.find();
    best.print();

    //writeln(best.values);
    //writeln(pred(best));
    //writeln(best.apply!(f));
}

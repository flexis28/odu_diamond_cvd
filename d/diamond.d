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

    //auto first = new RatePopulation(
    //    1.21299e+08,  // 1
    //    34893.6,                   // 2
    //    586.571, // e12 * exp(-352.3/T),       // 4
    //    0.423981, // 4.79e13 * exp(-7196.8/T),   // 5
    //    1000,                 // 6
    //    3.0559e+21,   // 7
    //    0, //0.5,                        // 8
    //    3.32977e+07, // 9
    //);

    auto first = new RatePopulation(
        1.044e+10,  // 1
        62495.3,  // 2
        251.817,                   // 4
        0.305421, //              // 5
        1000,                 // 6
        1.74485e+17,   // 7
        0, //0.5,                        // 8
        3.02377e+11, // 9
    );

    auto ga = new GeneticAlgorithm(0.3, 0.1, first, 50);
    auto best = ga.find();
    best.print();

    //writeln(best.values);
    //writeln(pred(best));
    //writeln(best.apply!(f));
}

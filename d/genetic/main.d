import std.stdio;
import std.random;
import genetic_algorithm, population;

pure float f(float x) {
    return 3*x*x - 5*x + 8;
}

void main() {
    enum NP = 10;
    auto svalues = new float[NP];
    for (int i = 0; i < NP; ++i) svalues[i] = i;
    auto stand = new Population(svalues);

    auto fvalues = new float[NP];
    fvalues[] = 0;
    auto first = new Population(fvalues);

    auto ga = new GeneticAlgorithm(0.2, 0.1, first, 50);

    auto pred = (Population a) { return a.diff!(f)(stand); };
    auto best = ga.find(pred);

    writeln(stand.values);
    //writeln(best.values);
    //writeln(pred(best));
    //writeln(best.apply!(f));
}

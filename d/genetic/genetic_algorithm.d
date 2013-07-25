module genetic.genetic_algorithm;

import std.stdio;
import std.algorithm;
import std.conv;
import std.array;
import std.random;
import genetic.population;

class GeneticAlgorithm {
    private enum EPS = 0.01;
    private float _selectFrac, _mutationFrac;

    private Population[] _pops;
    private size_t _popsSize;

    this(float selectFrac, float mutationFrac, Population initPop, size_t popsSize) {
        _selectFrac = selectFrac;
        _mutationFrac = mutationFrac;

        _pops ~= initPop;
        _popsSize = popsSize;

        while (_pops.length < _popsSize) {
            makeChild();
            if (_pops.length % 2 != 0) randomMutate();
        }
    }

    Population find() {
        double[Population] fitnes;

        int n = 0;
        while (true) {
            foreach (pop; _pops) {
                fitnes[pop] = pop.mark;
            }

            sort!((a, b) { return fitnes[a] > fitnes[b]; })(_pops);

            if (n % 10 == 0) {
                write(n, " => ");
                writeln(fitnes[best]);
                best.print();
            }
            n++;

            if (n == 1000) break;

            _pops = _pops[0 .. to!size_t(_pops.length * _selectFrac + 0.5)];
            while (_pops.length < _popsSize) makeChild();

            randomMutate();
        }

        //writeln(n, " ", fitnes[best], ": ", best.values);
        return best;
    }

    private @property Population best() { return _pops[0]; }

    private void makeChild() {
        if (_pops.length == 1) _pops ~= _pops[0].dup;
        auto parents = array(randomSample(_pops, 2));
        _pops ~= parents[0].crossWith(parents[1]);
    }

    private void randomMutate() {
        foreach (pop; _pops) {
            if (uniform(0, 100) - _mutationFrac * 100 > 0) continue;
            pop.mutate(_mutationFrac);
        }
    }
}

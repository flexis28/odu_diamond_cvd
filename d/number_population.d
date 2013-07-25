import std.stdio;
import std.algorithm;
import std.array;
import std.random;
import std.range;

class NumberPopulation {
    private float[] _values;

    this(float[] values) {
        _values = values;
    }

    @property const(float)[] values() {
        return _values;
    }

    Population dup() {
        return new NumberPopulation(_values.dup);
    }

    void mutate(float coef) {
        foreach (ref x; _values) {
            // мутирует по дефолту неболее чем на 50% от всей популяции
            if (coef * 50 - uniform(0, 100) < 0) continue;
            x = x * (coef * 5 - uniform(0, coef * 10)) +
                coef * 125 - uniform(0, coef * 250);
            if (x < 0) x = 0;
        }
    }

    Population crossWith(Population other) {
        auto pairs = zip(_values, other._values);
        auto values = map!((xy) {
            return (xy[0] + xy[1]) * 0.5f;
        })(pairs);
        auto child = new NumberPopulation(array(values));
        child.mutate(0.1);
        return child;
    }

    float diff(alias lambda)(Population other) {
        auto pairs = zip(apply!lambda(), other.apply!lambda());
        auto diffSq = map!((ij) {
            auto d = ij[0] - ij[1];
            return d * d; // квадрат разности
        })(pairs);

        // сумма квадратов разностей
        return reduce!((acc, x) { return acc + x; })(0.0f, array(diffSq));
    }

    float[] apply(alias lambda)() {
        return array(map!(lambda)(_values));
    }
}

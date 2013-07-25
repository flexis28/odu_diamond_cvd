module genetic.population;

interface Population {

    Population dup();
    void mutate(double coef);
    Population crossWith(Population other);

    @property double[] values();

    void print();
    @property double mark();
}

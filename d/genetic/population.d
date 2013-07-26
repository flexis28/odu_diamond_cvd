module genetic.population;

interface Population {

    Population dup();
    void mutate(float coef);
    Population crossWith(Population other);

    @property float[] values();

    void print();
    @property real mark();
}

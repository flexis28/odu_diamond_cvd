import std.stdio;
import std.math : exp, pow;
import std.string;
import genetic.rate_population;

class Ode {
	static public enum C = 9;
	static public enum L = 5;

    public enum double H = 1e-9;
    public enum double CH3 = 1e-10;
    public enum double T = 1200;

    private enum double maxt = 50.01;
    private enum double dt = 0.01;

    private RatePopulation pop;

    this(RatePopulation pop) {
        this.pop = pop;
    }

    auto main_loop() {
        double[C][L] cc;
        for(int l = 0; l < L; l++) cc[l][] = 0;
        cc[0][0] = 1;

//writeln(cc);

    	for (int x = 0; x < (maxt/dt); x++) {
    		cc = RUN(cc);
    	}

        double[C] toel;
        toel[] = 0;
        for (int l = 0; l < L; l++) {
            for (int j = 0; j<C;j++) {
                toel[j] += cc[l][j];
            }
        }

        pop.setCC(cc);
    }

    private auto RUN(in double[C][L] c_prev){
    	double[C][L] K1 = MUL(model(c_prev), dt);
    	double[C][L] K2 = MUL(model(SUM(c_prev,DEL(K1, 2))), dt);
    	double[C][L] K3 = MUL(model(SUM(c_prev, DEL(K2, 2))), dt);
    	double[C][L] K4 = MUL(model(SUM(c_prev, K3)), dt);
    	return SUM(c_prev, DEL(SUM(SUM(K1, MUL(K2, 2)), SUM(MUL(K3,2), K4)), 6));
    }

    private auto MUL(in double[C][L] array, double m){
    	double[C][L] result;
        for(int l = 0; l < L; l++){
    		for(int i = 0; i < C; i++){
    			result[l][i] = array[l][i] * m;
    		}
    	}
    	return result;
    }

    private auto SUM(in double[C][L] a, in double[C][L] b){
        double[C][L] result;
    	for(int l = 0; l < L; l++){
    		for(int i = 0; i < C; i++){
    			result[l][i] = a[l][i] + b[l][i];
    		}
    	}
        return result;
    }

    private auto DEL(in double[C][L] d, double e){
        double[C][L] result;
    	for(int l = 0; l < L; l++){
    		for(int i = 0; i < C; i++){
    			result[l][i] = d[l][i] / e;
    		}
    	}
    	return result;
    }

    private auto model(in double[C][L] c_prev){
    	double rate;
    	double[C][L] dc;
    	for(int l = 0; l < L; l++){
    		dc[l][] = 0;
    	}

    	for(int l = 0; l < L-1; l++){
        	//0 ->  CH2
    		//1 ->  *CH
    		//2 ->  **C
    		//3 ->  *C-
    		//4 ->  -CH
    		//5 ->  -C/
    		//6 ->  \C/
    		//7 ->  *C/
    		//8 ->  \CH

    		//Activacia
    		//1
    		rate = pop.k1 * c_prev[l][0] * H;
            dc[l][0] += -rate;
            dc[l][1] += rate;

            //2
            rate = pop.k1 * c_prev[l][1] * H;
            dc[l][1] += -rate;
            dc[l][2] += rate;
            //3
            rate = pop.k1 * c_prev[l][8] * H;
            dc[l][7] += rate;
            dc[l][8] += -rate;

            //Deactivacia
            //1
            rate = pop.k2 * c_prev[l][1] * H;
            dc[l][0] += rate;
            dc[l][1] += -rate;
            //2
            rate = pop.k2 * c_prev[l][2] * H;
            dc[l][1] += rate;
            dc[l][2] += -rate;
            //3
            rate = pop.k2 * c_prev[l][7] * H;
            dc[l][7] += -rate;
            dc[l][8] += rate;

			//Obr dimernoi svyazi
            //1
            rate = pop.k4_1 * c_prev[l][2] * c_prev[l][1];
            dc[l][1] += -rate;
            dc[l][2] += -rate;
            dc[l][3] += rate;
            dc[l][4] += rate;
            //2
            rate = pop.k4 * pow(c_prev[l][1], 2);
            dc[l][1] += -rate * 2;
            dc[l][4] += rate * 2;
            //3
            rate = pop.k4_1 * pow(c_prev[l][2], 2);
            dc[l][2] += -rate * 2;
            dc[l][3] += rate *2;
            //4
            for(int a = 1; a < 3; a++){
                rate = pop.k4_2 * c_prev[l][a] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8];
                dc[l][a] += -rate;
                if (a == 1) dc[l][4] += rate;
                else dc[l][3] += rate;
                dc[l][5] += rate;
                dc[l][7] += -rate;
            }

			//Razriv dimernoi svyazi
            //1
            rate = pop.k5 * c_prev[l][3] * c_prev[l][4];
            dc[l][1] += rate;
            dc[l][2] += rate;
            dc[l][3] += -rate;
            dc[l][4] += -rate;
            //2
            rate = pop.k5 * pow(c_prev[l][4], 2);
            dc[l][1] += rate * 2;
            dc[l][4] += -rate * 2;
            //3
            rate = pop.k5 * pow(c_prev[l][3], 2);
            dc[l][2] += rate * 2;
            dc[l][3] += (-rate) * 2;
            //4
            for(int a = 3; a < 5; a++){
                rate = pop.k5 * c_prev[l][a] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8];
                if (a == 4) dc[l][1] += rate;
                else dc[l][2] += rate;
                dc[l][a] += -rate;
                dc[l][5] += -rate;
                dc[l][7] += rate;
            }

            //Osagdenie metil-radikala
            //1
            rate = pop.k6 * c_prev[l][4] * c_prev[l][3] * CH3;
            dc[l+1][0] += rate;
            dc[l][3] += -rate;
            dc[l][4] += -rate;
            dc[l][8] += rate * 2;
            //2
            rate = pop.k6 * pow(c_prev[l][3], 2) * CH3;
            dc[l+1][0] += rate;
            dc[l][3] += -rate * 2;
            dc[l][7] += rate;
            dc[l][8] += rate;
            //3
            rate = pop.k6 * c_prev[l][5] * c_prev[l][3] * CH3;
            dc[l+1][0] += rate;
            dc[l][3] += -rate;
            dc[l][5] += -rate;
            dc[l][6] += rate;
            dc[l][8] += rate;

            //Migracia mostovoi gruppi
            for(int a = 0; a < 3; a++){
                //1
                double rate1 = pop.k7 * pow(c_prev[l][7], 2) * c_prev[l][8] * c_prev[l+1][a];
                double rate2 = pop.k7 * c_prev[l][6] * c_prev[l][7] * c_prev[l][1] * c_prev[l+1][a];
                dc[l][6] += rate1 + (-rate2);
                dc[l][7] += -rate1 + rate2;
                dc[l][8] += -rate1 + rate2;
                //2
                rate1 = pop.k7 * pow(c_prev[l][7], 3) * c_prev[l+1][a];
                rate2 = pop.k7 * c_prev[l][6] * c_prev[l][7] * c_prev[l][2] * c_prev[l+1][a];
                dc[l][2] += rate1 + (-rate2);
                dc[l][6] += rate1 + (-rate2);
                dc[l][7] += (-rate1 + rate2) * 2;
			}
            //Travlenie
            //1
            rate = pop.k8 * pow(c_prev[l][8], 2) * c_prev[l+1][0];
            dc[l+1][0] += -rate;
            dc[l][3] += rate;
            dc[l][4] += rate;
            dc[l][8] += -rate * 2;
            //2
            rate = pop.k8 * c_prev[l][7] * c_prev[l][8] * c_prev[l+1][0];
            dc[l+1][0] += -rate;
            dc[l][3] += rate * 2;
            dc[l][7] += -rate;
            dc[l][8] += -rate;
            //3
            rate = pop.k8 * c_prev[l][6] * c_prev[l][8] * c_prev[l+1][0];
            dc[l+1][0] += -rate;
            dc[l][3] += rate;
            dc[l][5] += rate;
            dc[l][6] += -rate;
            dc[l][8] += -rate;


            // TODO: миграция вниз не учитывает атомов входящих в структуры, которые изменяются посредством миграции
            // последнее упоминание по циклах перебора см. в коммите f88c420dd1f425442494aade8a019c295c0208b4
            //Migracia вниз
            for(int a = 1; a < 3; a++){
                rate = pop.k9 * c_prev[l+1][a] * pow(c_prev[l][2], 2) * CH3;
                dc[l+1][a] += -rate;
                if (a == 1) dc[l+1][4] += rate * 2;
                else{dc[l+1][3] += rate;
                    dc[l+1][4] += rate;}
                dc[l][2] += -rate * 2;
                dc[l][8] += rate * 2;
            }

            rate = pop.k9 * c_prev[l+1][2] * pow(c_prev[l][7], 3) * CH3;
            dc[l+1][2] += -rate;
            dc[l+1][4] += rate * 2;
            dc[l][6] += rate * 2;
            dc[l][7] += -rate * 3;
            dc[l][8] += rate;

            rate = pop.k9 * c_prev[l+1][2] * c_prev[l][5] * c_prev[l][3] * CH3;
            dc[l+1][2] += -rate;
            dc[l+1][4] += rate * 2;
            dc[l][3] += -rate;
            dc[l][5] += -rate;
            dc[l][6] += rate;
            dc[l][8] += rate;

            for(int a = 1; a < 3; a++){
                rate = pop.k9 * c_prev[l+1][a] * pow(c_prev[l][3], 2) * CH3;
                dc[l+1][a] += -rate;
                dc[l][3] += -rate * 2;
                if (a == 1) dc[l+1][4] += rate * 2;
                else{dc[l+1][3] += rate;
                    dc[l+1][4] += rate;}
                dc[l][8] += rate * 2;
            }
        }

        return dc;
    }
}

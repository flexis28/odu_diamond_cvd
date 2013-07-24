import std.stdio;
import std.math : exp, pow;
import std.string;

class Diamond {
	private enum C = 9;
	private enum L = 4;

	private double H = 1e-9;
    private double CH3 = 1e-10;
    private double dt = 0.01;
    private double maxt = 10.01;

    //OUR Fake
    private double T = 1200;
    private double k1, k2, k4, k4_1, k4_2, k5, k6 ,k7, k8, k9;

    //ORIGINAL
    //k1 = 5.2e13 * H * math.exp(-3360/T)
    //k2 = 2e13 * H
    //k4 = 1e12 * math.exp(-352.3/T)
    //k4_1 = k4 * 10
    //k5 = 4.79e13 * math.exp(-7196.8/T)
    //k6 = 1e13 * CH3
    //k7 = 6.13e13 * math.exp(-18.269/T)
    //k8 = 0.5
    //k9 = 3.5e8 * math.exp(-31.3/(1.98*T))


    this() {
        k1 = 5.66e15 * exp(-3360/T) * H;
        k2 = 0; //2e13 * H;
        k4 = 1e1;
        k4_1 = 20e2;
        k4_2 = 5;
        k5 = 0; //0.01;
        k6 = 1e13 * CH3;  //1e13*CH3;
        k7 = 6.13e12 * exp(-18269/T);
        k8 = 0; //0.5;
        k9 = 3.5e20 * exp(-31300/(1.98*T));
    }

    auto main_loop() {
        double[C][L] cc;
        for(int l = 0; l < L; l++) cc[l][] = 0;
        cc[0][0] = 1;

//writeln(cc);

    	int vivod = 100;
        auto format = "%d: %1.3e ";
    	for (int x = 0; x < (maxt/dt); x++) {
    		cc = RUN(cc);
            //if (x == 0) writeln(cc);

    		if (x % vivod == 0) {
    			double[C] toel;
                toel[] = 0;

    			writeln("____________ ", x+1, " SHAG, ", (x+1)*dt, " sec____________");
    			for (int l = 0; l < L; l++) {
    				write(l+1, " SLOI-> ");
    				double v = 0;

    				for (int j = 0; j<C;j++) {
    					toel[j] += cc[l][j];
    					v += cc[l][j];
    					printf(format.toStringz, j, cc[l][j]);
    				}
    				writeln("C = ", v);
    			}
    			write("TOTAL -> ");
    			for (int j = 0; j<C; j++) {
                    printf(format.toStringz, j, toel[j]);
                }
                writeln;
    		}
    	}
    }

    auto RUN(in double[C][L] c_prev){
    	double[C][L] K1 = MUL(model(c_prev), dt);
    	double[C][L] K2 = MUL(model(SUM(c_prev,DEL(K1, 2))), dt);
    	double[C][L] K3 = MUL(model(SUM(c_prev, DEL(K2, 2))), dt);
    	double[C][L] K4 = MUL(model(SUM(c_prev, K3)), dt);
    	return SUM(c_prev, DEL(SUM(SUM(K1, MUL(K2, 2)), SUM(MUL(K3,2), K4)), 6));
    }

    auto MUL(in double[C][L] array, double m){
    	double[C][L] result;
        for(int l = 0; l < L; l++){
    		for(int i = 0; i < C; i++){
    			result[l][i] = array[l][i] * m;
    		}
    	}
    	return result;
    }

    auto SUM(in double[C][L] a, in double[C][L] b){
        double[C][L] result;
    	for(int l = 0; l < L; l++){
    		for(int i = 0; i < C; i++){
    			result[l][i] = a[l][i] + b[l][i];
    		}
    	}
        return result;
    }

    auto DEL(in double[C][L] d, double e){
        double[C][L] result;
    	for(int l = 0; l < L; l++){
    		for(int i = 0; i < C; i++){
    			result[l][i] = d[l][i] / e;
    		}
    	}
    	return result;
    }

    auto model(in double[C][L] c_prev){
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
    		rate = k1 * c_prev[l][0] * H;
            dc[l][0] += -rate;
            dc[l][1] += rate;

            //2
            rate = k1 * c_prev[l][1] * H;
            dc[l][1] += -rate;
            dc[l][2] += rate;
            //3
            rate = k1 * c_prev[l][8] * H;
            dc[l][7] += rate;
            dc[l][8] += -rate;

            //Deactivacia
            //1
            rate = k2 * c_prev[l][1] * H;
            dc[l][0] += rate;
            dc[l][1] += -rate;
            //2
            rate = k2 * c_prev[l][2] * H;
            dc[l][1] += rate;
            dc[l][2] += -rate;
            //3
            rate = k2 * c_prev[l][7] * H;
            dc[l][7] += -rate;
            dc[l][8] += rate;

			//Obr dimernoi svyazi
            //1
            rate = k4_1 * c_prev[l][2] * c_prev[l][1];
            dc[l][1] += -rate;
            dc[l][2] += -rate;
            dc[l][3] += rate;
            dc[l][4] += rate;
            //2
            rate = k4 * pow(c_prev[l][1], 2);
            dc[l][1] += -rate * 2;
            dc[l][4] += rate * 2;
            //3
            rate = k4_1 * pow(c_prev[l][2], 2);
            dc[l][2] += -rate * 2;
            dc[l][3] += rate *2;
            //4
            for(int a = 1; a < 3; a++){
                rate = k4_2 * c_prev[l][a] * c_prev[l][7] * c_prev[l+1][0] * c_prev[l][8];
                dc[l][a] += -rate;
                if (a == 1) dc[l][4] += rate;
                else dc[l][3] += rate;
                dc[l][5] += rate;
                dc[l][7] += -rate;
            }

			//Razriv dimernoi svyazi
            //1
            rate = k5 * c_prev[l][3] * c_prev[l][4];
            dc[l][1] += rate;
            dc[l][2] += rate;
            dc[l][3] += -rate;
            dc[l][4] += -rate;
            //2
            rate = k5 * pow(c_prev[l][4], 2);
            dc[l][1] += rate * 2;
            dc[l][4] += -rate * 2;
            //3
            rate = k5 * pow(c_prev[l][3], 2);
            dc[l][2] += rate * 2;
            dc[l][3] += (-rate) * 2;
            //4
            for(int a = 3; a < 5; a++){
                rate = k5 * c_prev[l][a] * c_prev[l][5] * c_prev[l+1][0] * c_prev[l][8];
                if (a == 4) dc[l][1] += rate;
                else dc[l][2] += rate;
                dc[l][a] += -rate;
                dc[l][5] += -rate;
                dc[l][7] += rate;
            }

            //Osagdenie metil-radikala
            //1
            rate = k6 * c_prev[l][4] * c_prev[l][3] * CH3;
            dc[l+1][0] += rate;
            dc[l][3] += -rate;
            dc[l][4] += -rate;
            dc[l][8] += rate * 2;
            //2
            rate = k6 * pow(c_prev[l][3], 2) * CH3;
            dc[l+1][0] += rate;
            dc[l][3] += -rate * 2;
            dc[l][7] += rate;
            dc[l][8] += rate;
            //3
            rate = k6 * c_prev[l][5] * c_prev[l][3] * CH3;
            dc[l+1][0] += rate;
            dc[l][3] += -rate;
            dc[l][5] += -rate;
            dc[l][6] += rate;
            dc[l][8] += rate;

            //Migracia mostovoi gruppi
            for(int a = 0; a < 3; a++){
                //1
                double rate1 = k7 * pow(c_prev[l][7], 2) * c_prev[l][8] * c_prev[l+1][a];
                double rate2 = k7 * c_prev[l][6] * c_prev[l][7] * c_prev[l][1] * c_prev[l+1][a];
                dc[l][6] += rate1 + (-rate2);
                dc[l][7] += -rate1 + rate2;
                dc[l][8] += -rate1 + rate2;
                //2
                rate1 = k7 * pow(c_prev[l][7], 3) * c_prev[l+1][a];
                rate2 = k7 * c_prev[l][6] * c_prev[l][7] * c_prev[l][2] * c_prev[l+1][a];
                dc[l][2] += rate1 + (-rate2);
                dc[l][6] += rate1 + (-rate2);
                dc[l][7] += (-rate1 + rate2) * 2;
			}
            //Travlenie
            //1
            rate = k8 * pow(c_prev[l][8], 2) * c_prev[l+1][0];
            dc[l+1][0] += -rate;
            dc[l][3] += rate;
            dc[l][4] += rate;
            dc[l][8] += -rate * 2;
            //2
            rate = k8 * c_prev[l][7] * c_prev[l][8] * c_prev[l+1][0];
            dc[l+1][0] += -rate;
            dc[l][3] += rate * 2;
            dc[l][7] += -rate;
            dc[l][8] += -rate;
            //3
            rate = k8 * c_prev[l][6] * c_prev[l][8] * c_prev[l+1][0];
            dc[l+1][0] += -rate;
            dc[l][3] += rate;
            dc[l][5] += rate;
            dc[l][6] += -rate;
            dc[l][8] += -rate;


            // TODO: миграция вниз не учитывает атомов входящих в структуры, которые изменяются посредством миграции
            // последнее упоминание по циклах перебора см. в коммите f88c420dd1f425442494aade8a019c295c0208b4
            //Migracia вниз
            for(int a = 1; a < 3; a++){
                rate = k9 * c_prev[l+1][a] * pow(c_prev[l][2], 2) * CH3;
                dc[l+1][a] += -rate;
                if (a == 1) dc[l+1][4] += rate * 2;
                else{dc[l+1][3] += rate;
                    dc[l+1][4] += rate;}
                dc[l][2] += -rate * 2;
                dc[l][8] += rate * 2;
            }

            rate = k9 * c_prev[l+1][2] * pow(c_prev[l][7], 3) * CH3;
            dc[l+1][2] += -rate;
            dc[l+1][4] += rate * 2;
            dc[l][6] += rate * 2;
            dc[l][7] += -rate * 3;
            dc[l][8] += rate;

            rate = k9 * c_prev[l+1][2] * c_prev[l][5] * c_prev[l][3] * CH3;
            dc[l+1][2] += -rate;
            dc[l+1][4] += rate * 2;
            dc[l][3] += -rate;
            dc[l][5] += -rate;
            dc[l][6] += rate;
            dc[l][8] += rate;

            for(int a = 1; a < 3; a++){
                rate = k9 * c_prev[l+1][a] * pow(c_prev[l][3], 2) * CH3;
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

void main() {
	auto d = new Diamond;
	d.main_loop();
}

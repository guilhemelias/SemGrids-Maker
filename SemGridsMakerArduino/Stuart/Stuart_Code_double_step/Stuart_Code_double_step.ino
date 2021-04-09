//motor 1
int M1_EN  = 1;                          
int M1_pwm = 2;
int M1_dir = 3;
int M1_com = 4;
 
//motor 2
int M2_EN = 5;
int M2_pwm = 6;
int M2_dir = 7;
 
//motor 1 paramiters
int M1_max_speed = 2000;                 // steps per second
int M1_max_acc = 2000;                                 // steps per second second
 
//motor 2 paramiters
int M2_max_speed = 2000;                 // steps per second
int M2_max_acc = 2000;                                 // steps per second second
 
int M1_stepsPer_Rot = 3200;                  //steps per rotation
int M2_stepsPer_Rot = 3200;                  //steps per rotation
 
void setup()
{
           // motor 1
           pinMode(M1_com, OUTPUT);
           pinMode(M1_pwm, OUTPUT);
           pinMode(M1_dir, OUTPUT);
 
           //motor2
           pinMode(M2_EN, OUTPUT);
           pinMode(M2_pwm, OUTPUT);
           pinMode(M2_dir, OUTPUT);
 
}
 
void loop(){
           int dir = 1;
           while (true) {
                      move(100, 10, 1, -1*dir, 1*dir);
                      dir = dir*-1;
                      }
 
}
 
long int delaytime(int maxvel, int max_accel, int currentStep) {
 
           double time_perStep = 1.0 / maxvel;
 
           double theat = (currentStep%M1_stepsPer_Rot) / M1_stepsPer_Rot;
 
           double val = (0.8*maxvel)*sin(theat*3.14159268) + (0.2*maxvel);
           return (long int)10000;
}
 
void takeStep(int pwm1, long int dely, int dirpin, int dir) {
           if (dir >= 1) digitalWrite(dirpin, HIGH);
           else digitalWrite(dirpin, LOW);
          
           digitalWrite(pwm1, HIGH);
           _delay_us(dely);
           digitalWrite(pwm1, LOW);
           _delay_us(dely);
 
}
 
void move(int Nsteps1, int Nsteps2, int ratio, int dir1, int dir2) {
           int Nstepsdone1 = 0;
           int Nstepsdone2 = 0;
 
           //step 2 logic
           bool step2 = true;
 
          
           //stepping
           int wileSteps = Nsteps1;
//       if (Nsteps1 < Nsteps2*(1.0/ratio)) wileSteps = Nsteps2;
 
           while (Nstepsdone1 < wileSteps) {
                      //motor 1
                      long int dely1 = delaytime(M1_max_speed,M1_max_acc,Nstepsdone1);
                      takeStep(M1_pwm, dely1, M1_dir, dir1);
                      Nstepsdone1++;
                      //ratio conditions
                      if (Nstepsdone1%ratio==0 && step2==true) {
                                 //motor 2
                                 long int dely2 = delaytime(M2_max_speed, M2_max_acc, Nstepsdone2);
                                 takeStep(M2_pwm, dely2, M2_dir, dir2);
                                 Nstepsdone2++;
                                 if (Nstepsdone2 >= Nsteps2) step2 = false;
                      }
 
           }
 
}

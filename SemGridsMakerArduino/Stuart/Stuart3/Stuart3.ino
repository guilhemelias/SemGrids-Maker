#include "AccelStepper.h"
//#include <time.h>
 
 
//motor 1
int M1_EN = 1;
int M1_pwm = 52;
int M1_dir = 53;
int M1_com = 5;
 
//motor 2
int M2_EN = 9;
int M2_pwm = 10;
int M2_dir = 8;
 

//motor 1 paramiters
int M1_max_speed = 1500;               // steps per second
int M1_max_acc = 200;                                 // steps per second second
int M1_min_speed = 500;
                                                                                            //motor 2 paramiters
int M2_max_speed = 4000;                 // steps per second
int M2_max_acc = 1000;                                 // steps per second second
int M2_min_speed = 1000;
 
int M1_stepsPer_Rot = 3200;                  //steps per rotation
int M2_stepsPer_Rot = 3200;                  //steps per rotation

int nbre_tours=3;
 
void setup()
{
       // motor 1
       pinMode(M1_com, OUTPUT);
       pinMode(M1_EN, OUTPUT);
       pinMode(M1_pwm, OUTPUT);
       pinMode(M1_dir, OUTPUT);
 
       //motor2
       pinMode(M2_EN, OUTPUT);
       pinMode(M2_pwm, OUTPUT);
       pinMode(M2_dir, OUTPUT);
 
       digitalWrite(M1_com, HIGH);
       digitalWrite(M1_EN, LOW);                       // enable motor


}
 
void loop() {
       //delay(4000);
       int dir = 1;
       int i = 0;
       while (i<nbre_tours) {
       
             
              move(3200, 200, 1, 1, 1 * dir);
              i++;
              
       }

           
     delay(100000000);
      

}

 
long int delaytime(int maxvel, int min_value, int currentStep) {
 
       double avrg_val = 1.0*(maxvel - min_value) / 2.0;
 
       double val = avrg_val*sin(currentStep/(3.14159*80)+(3*3.14159/2)) + (avrg_val+ min_value);
 
       //convert to time
       //Serial.print(currentStep);
       //Serial.print("%");
       //Serial.print(M1_stepsPer_Rot);
       //Serial.print("=");
       //Serial.println(currentStep%M1_stepsPer_Rot);
 
       Serial.println(val);
       //Serial.println(1e6 / val);
       ////return 10000;
       return (int)(1e6*(1.0/val));
}
 
void takeStep(int pwm1, long int dely, int dirpin, int dir) {
       if (dir >= 1) 
       digitalWrite(dirpin, HIGH);
       else digitalWrite(dirpin, LOW);
 
       digitalWrite(pwm1, HIGH);
       delayMicroseconds(dely);
       digitalWrite(pwm1, LOW);
       delayMicroseconds(dely);
 
}
 
void move(int Nsteps1, int Nsteps2, int ratio, int dir1, int dir2) {
       int Nstepsdone1 = 0;
       int Nstepsdone2 = 0;
 
       //step 2 logic
       bool step2 = true;
 
 
       //stepping
       int wileSteps1 = Nsteps1;
       int wileSteps2 = Nsteps2;
       //       if (Nsteps1 < Nsteps2*(1.0/ratio)) wileSteps = Nsteps2;
 
       while (Nstepsdone1 < wileSteps1) {
              //motor 1
              long int dely1 = delaytime(M1_max_speed, M1_min_speed, Nstepsdone1);
              takeStep(M1_pwm, dely1, M1_dir, dir1);
              Nstepsdone1++;
              //ratio conditions
              if (Nstepsdone1%ratio == 0 && step2 == true) {
                     //motor 2
                     long int dely2 = delaytime(M2_max_speed, M2_min_speed, Nstepsdone2);
                     takeStep(M2_pwm, dely2, M2_dir, dir2);
                     Nstepsdone2++;
                     if (Nstepsdone2 >= Nsteps2) step2 = false;
              }
 
       }
              
        
       }
 
       
 

 

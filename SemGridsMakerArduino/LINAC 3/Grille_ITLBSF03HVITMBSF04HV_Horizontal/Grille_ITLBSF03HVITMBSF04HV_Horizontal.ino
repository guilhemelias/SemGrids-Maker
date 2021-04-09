//Programme pour grille ITLBSF03HVITMBSF04HV_Horizontal


#include "AccelStepper.h"
//#include <time.h>
AccelStepper stepper(1,10,8);
 
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
int M1_max_speed = 1400;               // steps per second
int M1_max_acc = 200;                                 // steps per second second
int M1_min_speed = 400;
                                                                                            //motor 2 paramiters
int M2_max_speed = 4000;                 // steps per second
int M2_max_acc = 1000;                                 // steps per second second
int M2_min_speed = 1000;
 
int M1_stepsPer_Rot = 3200;                  //steps per rotation
int M2_stepsPer_Rot = 3200;                  //steps per rotation

//Repartition de la grillegrille ITLBSF03HV

int a_tour=5;
float a_pas=1.4;//5 tour -> pas de 1.45mm
int b_tour=6;
float b_pas=0.6;//6 tour -> pas de 0.75mm
int c_tour=8;
float c_pas=0.4;//8 tour -> pas de 0.55mm
int d_tour=6;
float d_pas=0.6;//6 tour pas de 0.75mm
int e_tour=5;
float e_pas=1.4;//5 tour -> pas de 1.45mm

int pos = 0;
float mm_deplacee=0;
int dir=-1; //choix de la direction de la glissiere
           //1=vers la gauche ; -1=vers la droite

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
         //establish motor direction toggle pins
  pinMode(12, OUTPUT); //CH A -- HIGH = forwards and LOW = backwards???
  pinMode(13, OUTPUT); //CH B -- HIGH = forwards and LOW = backwards???
  
  //establish motor brake pins
  pinMode(9, OUTPUT); //brake (disable) CH A
  pinMode(8, OUTPUT); //brake (disable) CH B


       
       


}
 
void loop() {
       delay(2000); //pause de 2s
       int dir = 1;  //choix de la direction
       
       move(3200, 25, 1, -1, 1 * dir); 
       
       
       int a=0;
       while (a<a_tour) {
         GlisCW5(5);
         float pas=a_pas*25;
         move(3200, pas, 1, -1, 1 * dir);
         a++;       
       }
       int b=0;
       while (b<b_tour) {
         GlisCW15(5);
         float pas=b_pas*25;
         move(3200, pas, 1, -1, 1 * dir);
         b++;       
       }
       int c = 0;
       while (c<c_tour) {
         GlisCW15(5);
         float pas=c_pas*25;
         move(3200, pas, 1, -1, 1 * dir);
         c++;
         
       }
       int d=0;
       while (d<d_tour) {
         GlisCW15(5);
         float pas=d_pas*25;
         move(3200, pas, 1, -1, 1 * dir);
         d++;       
       }
       int e=0;
       while (e<e_tour) {
         GlisCW5(5);
         float pas=e_pas*25;
         move(3200, pas, 1, -1, 1 * dir);
         e++;       
       }
       
       move(3200, 25, 1, -1, 1 * dir); 
       
       
       delay (4000);
       


       

           
     
while(-1){} // fin du programme

      

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

void GlisCCW(int delaylegnth)
{
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, HIGH);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
  
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, LOW);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
  
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, LOW);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
    
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, HIGH);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
}

void GlisCW(int delaylegnth){
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, HIGH);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
  
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, HIGH);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
  
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, LOW);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
    
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, LOW);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
}

void GlisCW5(int delaylegnth){
  
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, LOW);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
    
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, HIGH);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
  
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, HIGH);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
  
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, LOW);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
    
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, LOW);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
    
    
}

void GlisCW15(int delaylegnth){
  
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, HIGH);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
  
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, LOW);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
    
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, LOW);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
  
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, HIGH);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
  
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, HIGH);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
  
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, LOW);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
    
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, LOW);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
    
    
  
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, HIGH);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
  
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, HIGH);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
  
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, LOW);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
    
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, LOW);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
  
  
  
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, HIGH);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
  
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, HIGH);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
  
    digitalWrite(9, LOW);  //ENABLE CH A
    digitalWrite(8, HIGH); //DISABLE CH B

    digitalWrite(12, LOW);   //Sets direction of CH A
    analogWrite(3, 255);   //Moves CH A
  
    delay(delaylegnth);
    
    digitalWrite(9, HIGH);  //DISABLE CH A
    digitalWrite(8, LOW); //ENABLE CH B

    digitalWrite(13, LOW);   //Sets direction of CH B
    analogWrite(11, 255);   //Moves CH B
  
    delay(delaylegnth);
    
    
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
                     int delaytime=5;
                     GlisCW(delaytime);
                     Nstepsdone2++;
                     if (Nstepsdone2 >= Nsteps2) step2 = false;
              }
 
       }
              
        
       }

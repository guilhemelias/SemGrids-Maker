///INCLUDES/////////////////////////////////////////////////////////////////////////////////////

//#include <AccelStepper.h>
//#include "AccelStepper.h"
//#include <time.h>
//AccelStepper stepper(1,10,8);

#include <Arduino.h>




///PARAM/////////////////////////////////////////////////////////////////////////////////////

//motor 1
int M1_EN = 1;  //Sortie pour le moteur cadre
int M1_pwm = 52;
int M1_dir = 53;
int M1_com = 5;
 
//motor 2
int M2_EN = 9;  //Sortie pour le moteur glissiere
int M2_pwm = 10;
int M2_dir = 8;
 

//motor 1 parameters
int M1_max_speed = 14000;               // steps per second                                 
int M1_max_acc = 200; 
int M1_min_speed = 4000;                // steps per second second
//motor 2 paramiters

int M2_max_speed = 4000;               // steps per second
int M2_max_acc = 1000;                 // steps per second second
int M2_min_speed = 1000;
                                                                                            

int M1_stepsPer_Rot = 3200;            //steps per rotation
int M2_stepsPer_Rot = 3200;            //steps per rotation








///Repartition grilles/////////////////////////////////////////////////////////////////////////////////////

//commun
int dir = 1;


//Reposition Glissiere
float mm_deplacee=50;
int pas4=mm_deplacee*25;


//Repartition de la grille ITLBSF03HV
int a_tour=5;
float a_pas=3.8;//5 tour -> pas de 3.8mm
int b_tour=7;
float b_pas=2.4;//7 tour -> pas de 2.4mm
int c_tour=6;
float c_pas=1.6;//6 tour -> pas de 1.6mm
int d_tour=7;
float d_pas=2.4;//7 tour pas de 2.4mm
int e_tour=5;
float e_pas=3.8;//5 tour -> pas de 3.8mm


//Repartition grille RegularStep
int regularStep = 1;
int nombre_de_tour=1;
float distGlissiere = regularStep*25;



volatile String buffer;
volatile bool inputComplete = false;




///SETUP&LOOP/////////////////////////////////////////////////////////////////////////////////////

void setup() {
  
  // motor 1
   pinMode(M1_com, OUTPUT);
   pinMode(M1_EN, OUTPUT);
   pinMode(M1_pwm, OUTPUT);
   pinMode(M1_dir, OUTPUT);
 
   //motor2
   pinMode(M2_EN, OUTPUT);
   pinMode(M2_pwm, OUTPUT);
   pinMode(M2_dir, OUTPUT);

   // enable motor
   digitalWrite(M1_com, HIGH);
   digitalWrite(M1_EN, LOW); 

   //establish motor direction toggle pins
   pinMode(12, OUTPUT); //CH A -- HIGH = forwards and LOW = backwards???
   pinMode(13, OUTPUT); //CH B -- HIGH = forwards and LOW = backwards???
  
   //establish motor brake pins
   pinMode(9, OUTPUT); //brake (disable) CH A
   pinMode(8, OUTPUT); //brake (disable) CH B

  Serial.begin(2000000);
  Serial.flush();
}




void loop() {
  delay(5000);
  int nbIndex = 0; 
  int gap = 0; 
  
  if(Serial.available()){
      
      
    String receiveData = Serial.readStringUntil('\r\n');
      
    char data[receiveData.length()+1];  
    char *dataBis[receiveData.length()+1]; 

    receiveData.toCharArray(data,receiveData.length()+1);

    

    char *p = data;
    char *str;
    int val=0;

    while ((str = strtok_r(p, "/", &p)) != NULL){
      dataBis[val]=str;         
      val++;
    } 
      
    char * prgm = dataBis[0]; 
    int resPrgm = strcmp(prgm,"cw");



    if (resPrgm==0){
      char * dir = dataBis[1];
      int nbslide = atoi(dataBis[2]);
      int resDir = strcmp(dir,"L");
      if (resDir == 0){
        int i =0;
        int gap=nbslide*25;
        while(i<=gap){
          GlisCW(5);            
          i++;
        }
      }
      else{
        int i =0;
        int gap=nbslide*25;
        while(i<=gap){
          GlisCCW(5);
          i++;
        }
      }
       
    }
    else{
      nbIndex = atoi(dataBis[1]);

      gap = atoi(dataBis[2]);
          
      float tabSteps[nbIndex];
      int tabLaps[nbIndex];
      for (int i =0;i<(val-2)/2;i++){         
        tabSteps[i]=atof(dataBis[i+3]);
      } 
      for (int i =0;i<(val-2)/2;i++){ 
        tabLaps[i]=atoi(dataBis[i+3+(val-2)/2]);    
        
      } 

      movePrgrm(tabSteps,tabLaps,nbIndex,gap);
    }
     
      
  }
       
  while(-1){}  
 
  //Arret de la boucle

}






///PROGRAMMES/////////////////////////////////////////////////////////////////////////////////////


void movePrgrm(float *tabSteps, int *tabLaps, int nbIndex, int gap){
  
  
  float pasGap = gap*25;
  reposition(pasGap);
  move(3200, 1, 1, -1, 1 * dir);
  for (int i = 0 ; i < nbIndex ; i++){
    int tour =0;    
    int pas = tabSteps[i]*25;   
    while(tour<tabLaps[i]){    
      move(3200, pas, 1, -1, 1 * dir);
      Serial.println("ok");
      tour++;     
    }
  } 
}
 
  
  void reposition(int gap){
    int i =0;
    while(i<=gap){
    //GlisCCW(5);
    GlisCW(5);
    i++;
    }
}



///Fonctions mouvement Bobineuse/////////////////////////////////////////////////////////////////////////////////////

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
                     GlisCW(5);
                     Nstepsdone2++;
                     if (Nstepsdone2 >= Nsteps2) step2 = false;
              }
 
       }
              
        
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
 
      // Serial.println(val);
       //Serial.println(1e6 / val);
       ////return 10000;
       return (int)(1e6*(1.0/val));
}



void takeStep(int pwm1, long int dely, int dirpin, int dir) {
       if (dir >= 1) 
       digitalWrite(dirpin, HIGH);
       else digitalWrite(dirpin, LOW);
      for( int i = 1; i < 11; i++ ){
        digitalWrite(pwm1, HIGH);
        delayMicroseconds(dely);
        digitalWrite(pwm1, LOW);
        delayMicroseconds(dely);
      }
       
 
}







///Fonctiom mouvements glissiere/////////////////////////////////////////////////////////////////////////////////////

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

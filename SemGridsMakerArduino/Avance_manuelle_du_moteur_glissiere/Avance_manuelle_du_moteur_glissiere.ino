#include <AccelStepper.h>

// Define a stepper and the pins it will use
AccelStepper stepper(1,10,8);

int pos = 0;
int mm_deplacee=60;
int dir=-1; //choix de la direction de la glissiere
           //1=vers la gauche ; -1=vers la droite

void setup()
{  
  stepper.setMaxSpeed(1500);
  stepper.setAcceleration(5000);
}

void loop()
{
  if (stepper.distanceToGo() == 0)
  {
    delay(2000);
    pos = dir*200*mm_deplacee;
    stepper.moveTo(pos);\
  }
  stepper.run();
}


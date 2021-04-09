#include <AccelStepper.h>

// Define a stepper and the pins it will use
AccelStepper stepper(1,53,52);

int pos = 0;
int vitesse=1000

void setup()
{  
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(500);
  stepper.speed(1000);
}

void loop()
{
  if (stepper.distanceToGo() == 0)
  {
    delay(4000);
    pos = 3200;
    stepper.moveTo(pos);\
  }
  stepper.run();
}


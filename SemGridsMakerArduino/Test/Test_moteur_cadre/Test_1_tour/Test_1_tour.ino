#include <AccelStepper.h>

// Define a stepper and the pins it will use
AccelStepper stepper(1,53,52);

int pos = 0;

void setup()
{  
  stepper.setMaxSpeed(960);
  stepper.setAcceleration(1000);
}

void loop()
{
  if (stepper.distanceToGo() == 0)
  {
    delay(2000);
    pos = pos+3200;
    stepper.moveTo(pos);\
  }
  stepper.run();
}


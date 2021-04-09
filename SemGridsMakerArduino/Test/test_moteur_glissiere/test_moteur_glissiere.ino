#include <AccelStepper.h>

// Define a stepper and the pins it will use
AccelStepper stepper(1,8,9);

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
    delay(4000);
    pos = +3200;
    stepper.moveTo(pos);\
  }
  stepper.run();
}


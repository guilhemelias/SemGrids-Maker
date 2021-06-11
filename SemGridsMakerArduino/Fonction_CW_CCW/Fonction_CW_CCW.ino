//Programme avance manuelle de la liaison glissiere

int delaylegnth = 4;

void setup() {
  
  //establish motor direction toggle pins
  pinMode(12, OUTPUT); //CH A -- HIGH = forwards and LOW = backwards???
  pinMode(13, OUTPUT); //CH B -- HIGH = forwards and LOW = backwards???
  
  //establish motor brake pins
  pinMode(9, OUTPUT); //brake (disable) CH A
  pinMode(8, OUTPUT); //brake (disable) CH B


  
  
}
float mm_deplacee=20;

int pas4=mm_deplacee*25;

int i =0;
void loop(){
 
 while(i<=pas4){
GlisCCW(delaylegnth);
//GlisCW(delaylegnth);
i++;

}
while(-1){}
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

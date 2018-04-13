//Rotates servo 0-180 degrees taking ultrasound readings. Deg and distance in cm are sent to serial (deg,cm)

#include <Servo.h>  //servo library
Servo myservo;      // create servo object to control servo

int Echo = A4;  
int Trig = A5; 

//Ultrasonic distance measurement Sub function
int Distance_test() {
  digitalWrite(Trig, LOW);   
  delayMicroseconds(2);
  digitalWrite(Trig, HIGH);  
  delayMicroseconds(20);
  digitalWrite(Trig, LOW);   
  float cmdistance = pulseIn(Echo, HIGH);  
  cmdistance= cmdistance / 58;       
  return (int)cmdistance;
}  

void setup() { 
  myservo.attach(3);  // attach servo on pin 3 to servo object
  Serial.begin(9600);    
  pinMode(Echo, INPUT);    
  pinMode(Trig, OUTPUT);  
} 

void loop() { 
  for(int deg=1; deg<180;deg++){
  myservo.write(deg);
  Serial.print(deg);
  Serial.print(",");
  Serial.println(Distance_test());
  delay(50);
}
  /*
  for(int deg=180; deg>0;deg--){
  myservo.write(deg);
  Serial.print(deg);
  Serial.print(",");
  Serial.print(Distance_test());
  delay(50);
}
*/
}

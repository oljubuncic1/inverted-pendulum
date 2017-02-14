/*
  This is a test sketch for the Adafruit assembled Motor Shield for Arduino v2
  It won't work with v1.x motor shields! Only for the v2's with built in PWM
  control

  For use with the Adafruit Motor Shield v2
  ---->	http://www.adafruit.com/products/1438
*/

#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <DistanceGP2Y0A21YK.h>

DistanceGP2Y0A21YK Dist;

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61);

// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *myMotor = AFMS.getMotor(3);
// You can also make another motor on port M2
Adafruit_DCMotor *myOtherMotor = AFMS.getMotor(4);

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  //Serial.println("Adafruit Motorshield v2 - DC Motor test!");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz

  // Set the speed to start, from 0 (off) to 255 (max speed)
  myMotor->setSpeed(150);
  myMotor->run(FORWARD);
  // turn on motor
  myMotor->run(RELEASE);

  myOtherMotor->setSpeed(150);
  myOtherMotor->run(FORWARD);
  // turn on motor
  myOtherMotor->run(RELEASE);

  myMotor->run(FORWARD);
  myOtherMotor->run(FORWARD);

  myOtherMotor->setSpeed(0);
  myMotor->setSpeed(0);

  Dist.begin(1);
  while(!Serial.available());
  Serial.read();

}

int i = 0;
unsigned long newtime = 0;

void loop() {
  //int uptime = micros();

  int angle = analogRead(A0);
  Serial.print("A");
  Serial.print(angle);

  //int distance = Dist.getDistanceCentimeter();
  //Serial.print("D");
  //Serial.println(distance);

  //delayMicroseconds(20000 - (micros() - uptime));

  Serial.print("T");
  unsigned long sent = (micros() - newtime);
  while(sent > 0){
    Serial.print(char(sent%10 + '0'));
    sent /= 10;
  }
  Serial.print('\n');
  newtime = micros();
  
  while (1) {
    if (Serial.available()) {
      i = 0;
      myMotor->run(RELEASE);
      myOtherMotor->run(RELEASE);
      uint8_t spinSpeed = 0;
      while (Serial.available()) {
        spinSpeed = spinSpeed * 10 + Serial.read() - '0';
      }
      //Serial.print("S");
      //Serial.println(spinSpeed);
      if (spinSpeed > 100) {
        spinSpeed -= 100;
        myMotor->run(FORWARD);
        myOtherMotor->run(FORWARD);
      }
      else {
        myMotor->run(BACKWARD);
        myOtherMotor->run(BACKWARD);
      }
      //spinSpeed = spinSpeed * 255;
      spinSpeed = map(spinSpeed, 0, 100, 0, 255);
      myMotor->setSpeed(spinSpeed);
      myOtherMotor->setSpeed(spinSpeed);
      break;
    }
    //  else{
    //    i++;
    //    if(i == 100){
    //      i = 0;
    //      myMotor->run(RELEASE);
    //      myOtherMotor->run(RELEASE);
    //    }
    //  }
    //delayMicroseconds(20000 - (micros() - uptime));
  }
}

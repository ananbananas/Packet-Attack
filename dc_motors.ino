#include <Servo.h>

#define IR_SENSOR_PIN 12
#define SERVO_PIN 9

Servo servoMotor;
bool objectDetected = false;
bool running;

// Motor A connections
int enA = 0;  // Enable pin for Motor A
int in1 = 1;   // Control pin 1 for Motor A
int in2 = 2;   // Control pin 2 for Motor A*/

// Motor B connections
int enB = 6;  // Enable pin for Motor B
int in3 = 7;  // Control pin 1 for Motor B green
int in4 = 8;  // Control pin 2 for Motor B brown

void setup() {
  pinMode(IR_SENSOR_PIN, INPUT);
  servoMotor.attach(SERVO_PIN);
  running = true;
 // Set pins as outputs
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  
  pinMode(enB, OUTPUT);//orange
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  servoMotor.write(0);

}

void loop() {
  if (running && (millis()<15000)) {
    //Serial.println("Running");
    //run motor A
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enA, 200); 
  
  //run motor B 
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, 200);

  if (digitalRead(IR_SENSOR_PIN) == LOW) {
    // Object detected, rotate servo to 180 degrees
    servoMotor.write(90);
    running = false;
  } 
  } else {
    //Stop motors
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    analogWrite(enA, 0); // Stop Motor A
  
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
    analogWrite(enB, 0); // Stop Motor B
  }}


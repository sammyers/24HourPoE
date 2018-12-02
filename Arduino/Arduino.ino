#include <Adafruit_MotorShield.h>
/*     Simple Stepper Motor Control Exaple Code
 *      
 *  by Dejan Nedelkovski, www.HowToMechatronics.com
 *  
 */

// defines pins numbers
#define STEP_PIN 3
#define DIR_PIN 4
#define ACCEPT_POS 500
#define DENY_POS 1000
#define STAMP_TRAVEL_MS 1000
#define STAMP_PAUSE_MS 300

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *stampMotor = AFMS.getMotor(4);

int curPos = 0;

void setup() {
  // Set up the Adafruit motor shield and stamp DC motor
  AFMS.begin();
  stampMotor->setSpeed(150);
  
  // Sets the two pins as Outputs
  pinMode(STEP_PIN, OUTPUT); 
  pinMode(DIR_PIN, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  // Look for command from the computer
  while (Serial.available() > 0) {
    String cmd = Serial.readString();
    if (cmd == "accept") {
      Serial.println("Stamping seal of approval.");
      acceptApplication();
    } else if (cmd == "reject") {
      Serial.println("Rejecting application.");
      rejectApplication();
    } else {
      Serial.print("Unrecognized command: ");
      Serial.print("\"");
      Serial.print(cmd);
      Serial.println("\"");
    }
  }
}

void rejectApplication() {
  // Move the gantry
  moveToPos(DENY_POS);

  // Actuate the stamp
  stamp();
}

void acceptApplication() {
  // Move the gantry
  moveToPos(ACCEPT_POS);

  // Actuate the stamp
  stamp();
}

void moveToPos(int pos) {
  // Determine and set the direction
  int direction = (curPos > pos) ? HIGH : LOW;
  int step = (curPos < pos) ? 1 : -1;
  digitalWrite(DIR_PIN, direction);

  // Move the gantry
  while (curPos != pos) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(500);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(500);
    curPos += step;
  }
}

void stamp() {
  stampMotor->run(FORWARD);
  delay(STAMP_TRAVEL_MS);
  stampMotor->run(RELEASE);
  delay(STAMP_PAUSE_MS);
  stampMotor->run(BACKWARD);
  delay(STAMP_TRAVEL_MS);
  stampMotor->run(RELEASE);
}

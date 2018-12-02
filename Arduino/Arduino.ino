#include <Adafruit_MotorShield.h>
#include <Servo.h>
/*     Simple Stepper Motor Control Exaple Code
 *      
 *  by Dejan Nedelkovski, www.HowToMechatronics.com
 *  
 */

// defines pins numbers
#define STEP_PIN 3
#define DIR_PIN 4
#define GATE_SERVO_PIN 11
#define GANTRY_ACCEPT_POS 500
#define GANTRY_REJECT_POS 2000
#define GATE_CLOSED_POS 90
#define GATE_OPEN_POS 0
#define GATE_OPEN_MS 10000
#define STAMP_TRAVEL_MS 1000
#define STAMP_PAUSE_MS 300

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *stampMotor = AFMS.getMotor(1);
Servo gateServo;

int curGantryPos = GANTRY_REJECT_POS;
int curGatePos = GATE_CLOSED_POS;

void setup() {
  // Set up the Adafruit motor shield and stamp DC motor
  AFMS.begin();
  stampMotor->setSpeed(150);

  // Set up the gate servo
  gateServo.attach(GATE_SERVO_PIN);
  gateServo.write(GATE_CLOSED_POS);
  
  // Sets the two pins as Outputs
  pinMode(STEP_PIN, OUTPUT); 
  pinMode(DIR_PIN, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  // Look for command from the computer
  while (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'a') {
      Serial.println("Stamping seal of approval.");
      acceptApplication();
    } else if (cmd == 'r') {
      Serial.println("Rejecting application.");
      rejectApplication();
    } else {
      Serial.print("Unrecognized command: ");
      Serial.print("\"");
      Serial.print(cmd);
      Serial.println("\"");
    }
    // Clear the serial buffer in case there were multiple commands sent
    // TODO: Fix this kiosk-side
    Serial.flush();
  }
}

void rejectApplication() {
  // Move the gantry
  moveToPos(GANTRY_REJECT_POS);

  // Actuate the stamp
  Serial.println("Stamping application");
  stamp();
}

void acceptApplication() {
  // Move the gantry
  moveToPos(GANTRY_ACCEPT_POS);

  // Actuate the stamp
  Serial.println("Stamping application");
  stamp();

  // Open the gate for the desired amount of timme
  Serial.println("Opening gate");
  setGatePos(GATE_OPEN_POS);
  delay(GATE_OPEN_MS);
  Serial.print("Closing gate");
  setGatePos(GATE_CLOSED_POS);
}

void moveToPos(int pos) {
  // Determine and set the direction
  int direction = (curGantryPos > pos) ? HIGH : LOW;
  int step = (curGantryPos < pos) ? 1 : -1;
  digitalWrite(DIR_PIN, direction);

  // Move the gantry
  while (curGantryPos != pos) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(500);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(500);
    curGantryPos += step;
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

void setGatePos(int pos) {
  int step = (curGatePos > pos) ? -1 : 1;
  while (curGatePos != pos) {
    gateServo.write(curGatePos);
    curGatePos += step;
    delay(10);
  }
}

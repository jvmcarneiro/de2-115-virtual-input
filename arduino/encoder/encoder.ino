/* Byte message meaning:
 * Sent:
 *   40 - "Is there a GUI out there?"
 *   42 - "Ok GUI, got you."
 *   50 - "Still there, GUI?"
 * Received:
 *   41 - "Hi Arduino, GUI here."
 *   90 - "Power the board on and off."
 *   00 - "Button 3 changed state."
 *   01 - "Button 2 changed state."
 *   02 - "Button 1 changed state."
 *   03 - "Button 0 changed state."
 *   04 - "Switch 17 changed state."
 *   05 - "Switch 16 changed state."
 *   06 - "Switch 15 changed state."
 *   07 - "Switch 14 changed state."
 *   08 - "Switch 13 changed state."
 *   09 - "Switch 12 changed state."
 *   10 - "Switch 11 changed state."
 *   11 - "Switch 10 changed state."
 *   12 - "Switch 9 changed state."
 *   13 - "Switch 8 changed state."
 *   14 - "Switch 7 changed state."
 *   15 - "Switch 6 changed state."
 *   16 - "Switch 5 changed state."
 *   17 - "Switch 4 changed state."
 *   18 - "Switch 3 changed state."
 *   19 - "Switch 2 changed state."
 *   20 - "Switch 1 changed state."
 *   21 - "Switch 0 changed state."
 */

byte power_pin = 2;
byte control_pin = 8;
int power_state = LOW;

byte received;
byte bitread;
bool is_connected;

unsigned long start_millis;
unsigned long current_millis;

void setup() 
{
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  digitalWrite(control_pin, LOW);
  digitalWrite(power_pin, LOW);
  is_connected = false;
}

void loop() 
{
  // Send beacon via serial and wait for answer
  while(!Serial.available()) {
    Serial.print(40);
  }
  received = Serial.read();

  // Confirm connection
  if (!is_connected) {
    if (received == 41) {
      Serial.print(42);
      is_connected = true;
    }
  }

  // Read received byte as bits and set output pins 
  else if (received >= 0 && received < 32) {
    for (int j = 0; j++; j<5) {
     bitread = bitRead(received, j);
     digitalWrite(j+3, bitread);
    }
    delay(0.001);
    digitalWrite(control_pin, HIGH);
    delay(0.001);
    digitalWrite(control_pin, LOW);
  }

  // Toggle fpga power
  else if(received == 90) {
    if(power_state){
      power_state = LOW;
    }else {
      power_state = HIGH;
    }
    digitalWrite(power_pin, power_state);
  }
}

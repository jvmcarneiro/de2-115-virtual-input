/** Message translation table **
 * Write:
 *   40 - "Is there a GUI out there?"
 *   42 - "Ok GUI, got you."
 *   50 - "I'm already paired."
 *   91 - "Power toggle succeeded."
 *   92 - "Power toggle failed."
 * Read:
 *   41 - "Hi Arduino, GUI here."
 *   88 - "End connection."
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
 **/

/** Currently using only 4 output data pins due to limited availability. **/

byte power_pin = 2;
byte control_pin = 3;
int power_state = LOW;

int received;
byte bitread;
//bool is_sent = false;
bool is_connected = false;
bool is_power_blocked = false;

unsigned long beam_millis = millis(); // timestamp for last beam sent
//unsigned long sent_millis;            // ts for output clock state change
unsigned long input_millis;           // ts for last input received
unsigned long power_on_millis;        // ts for how long the board is on
unsigned long power_off_millis;       // ts for last power toggle

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
  pinMode(9, OUTPUT);

  for (int j = 4; j<10; j++)
    digitalWrite(j, LOW);
}

void loop() 
{
  while(!Serial.available()) {     
    // Send beacon every 1 second
    if ((millis() - beam_millis) > 1000) {
      beam_millis = millis();
      if (is_connected)
        Serial.write(50);
      else
        Serial.write(40);
    }

    // Change output control signal state
    //if (is_sent && (millis() - sent_millis) > 100) {
    //  digitalWrite(control_pin, LOW);
    //  is_sent = false;
    //}

    // Unblock fpga power in 10 sec after last toggle
    if (is_power_blocked && (millis() - power_off_millis) > 10000)
      is_power_blocked = false;

    // Disconnect and turn off fpga if user is idle for 10 min
    if (is_connected && (millis() - input_millis) > 595000) {
      is_connected = false;
      if (power_state) {
        is_power_blocked = true;
        power_state = LOW;
        digitalWrite(power_pin, power_state);
        power_off_millis = millis();
      }
    }

    // Turn fpga off after 10 min of use
    if (power_state && (millis() - power_on_millis) > 600000) {
      is_power_blocked = true;
      power_state = LOW;
      digitalWrite(power_pin, power_state);
      power_off_millis = millis();
    }
  }
  input_millis = millis();
  received = Serial.read();

  // Confirm connection
  if (!is_connected) {
    if (received == 41) {
      Serial.write(42);
      is_connected = true;
    }
  }

  // Disconnect and power off fpga
  else if (received == 88) {
    is_connected = false;
    if (power_state) {
      is_power_blocked = true;
      power_off_millis = millis();
      power_state = LOW;
      digitalWrite(power_pin, power_state);
    }
  }

  // Read received byte as bits and set output pins 
  else if (received >= 0 && received < 22) {
    for (int j = 0; j<6; j++) {
      bitread = bitRead(received, j);
      digitalWrite(j+4, bitread);
    }
    delay(1);
    digitalWrite(control_pin, HIGH);
    delay(1);
    digitalWrite(control_pin, LOW);
    //is_sent = true;
    //sent_millis = millis();
  }

  // Reset fpga to initial state 
  else if (received == 127) {
    for (int j = 0; j<6; j++) {
      digitalWrite(j+4, HIGH);
    }
    delay(1);
    digitalWrite(control_pin, HIGH);
    delay(1);
    digitalWrite(control_pin, LOW);
    //is_sent = true;
    //sent_millis = millis();
  }

  // Toggle fpga power
  else if(received == 90) {
    if (is_power_blocked) 
      Serial.write(92);
    else if (power_state) {
      is_power_blocked = true;
      power_off_millis = millis();
      power_state = LOW;
      digitalWrite(power_pin, power_state);
      Serial.write(91);
    } else {
      is_power_blocked = true;
      power_off_millis = millis();
      power_state = HIGH;
      digitalWrite(power_pin, power_state);
      Serial.write(91);
    }
  }
}

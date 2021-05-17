byte power_pin = 2;
int power_state = LOW;

int received;
bool is_powered = false;
bool is_connected = false;
bool is_power_blocked = false;

unsigned long beam_millis = millis(); // timestamp for last beam sent
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
  for (int i=3; i<10; i++)
    digitalWrite(i, LOW);
  digitalWrite(power_pin, LOW);
}

void loop() 
{
  while(!Serial.available()) {     
    if (is_powered) {
      delay(3000);
      digitalWrite(3, HIGH);
      delay(1000);
      digitalWrite(4, HIGH);
      delay(1000);
      digitalWrite(5, HIGH);
      delay(1000);
      digitalWrite(6, HIGH);
      delay(1000);
      digitalWrite(7, HIGH);
      delay(1000);
      digitalWrite(8, HIGH);
      delay(1000);
      digitalWrite(9, HIGH);
      delay(1000);
      for (int i=3; i<10; i++)
        digitalWrite(i, LOW);
    }

    // Send beacon every 1 second
    if ((millis() - beam_millis) > 1000) {
      beam_millis = millis();
      if (is_connected)
        Serial.write(50);
      else
        Serial.write(40);
    }

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
      is_powered = true;
      is_power_blocked = true;
      power_off_millis = millis();
      power_state = HIGH;
      digitalWrite(power_pin, power_state);
      Serial.write(91);
    }
  }
}

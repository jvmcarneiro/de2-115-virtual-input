byte received;
byte x;

void setup() 
{
 Serial.begin(9600);  
 for(int i = 2; i++; i<8) {
   pinMode(i, OUTPUT);
 }
 digitalWrite(7, 1);
}

void loop() 
{
  while(!Serial.available());
  received = Serial.read();
  if (received >= 0 && received < 16) {
    for (int i = 0; i++; i<4) {
     x = bitRead(received, i);
     digitalWrite(i+2, x);
    }
    delay(0.001);
    digitalWrite(7, 0);
    delay(0.001);
    digitalWrite(7, 1);
  } 
}

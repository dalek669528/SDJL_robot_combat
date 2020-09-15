int delta = 1000;         // incoming serial byte

void setup() {
  // start serial port at 9600 bps:
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
  while (!Serial) {}
}

void loop() {
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    String str = Serial.readString();
    // read second analog input, divide by 4 to make the range 0-255:
    delta = str.toInt();
    Serial.print("Serial read:");
    Serial.println(delta);
    delay(500);
  }
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(delta);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(delta);
}

int times = 0;         // incoming serial byte

void setup() {
  // start serial port at 9600 bps:
  Serial.begin(9600);
  while (!Serial) {}
}

void loop() {
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    String str = Serial.readString();
    times++;
    delay(5);
    // read second analog input, divide by 4 to make the range 0-255:
    Serial.print("Serial read:");
    Serial.print(times);
    Serial.print(" ");
    Serial.print(str);
  }
}

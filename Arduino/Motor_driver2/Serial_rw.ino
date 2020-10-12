void Serial_rw(){
  if (Serial.available() > 0) {
    // get incoming byte:
    String str = Serial.readStringUntil('\n');
    A.pwm = (str.substring(0,str.indexOf(' '))).toInt();
    str = str.substring(str.indexOf(' ')+1);
    B.pwm = (str.substring(0,str.indexOf(' '))).toInt();
    str = str.substring(str.indexOf(' ')+1);
    C.pwm = (str.substring(0,str.indexOf(' '))).toInt();
    D.pwm = (str.substring(str.indexOf(' ')+1)).toInt();

  }
  Serial.print(timer);
  Serial.print(", ");
  Serial.print(pwm_test);
  Serial.print(", ");
  Serial.print(A.encoder);
  Serial.print(", ");
  Serial.print(B.encoder);
  Serial.print(", ");
  Serial.print(C.encoder);
  Serial.print(", ");
  Serial.print(D.encoder);
  Serial.print("\n");
}

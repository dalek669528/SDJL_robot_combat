
float X, Y, theta;
float now_angle[4] = {0};
int encoder;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
  while (!Serial) {}
}

void loop() {
  Serial_rw();
}

void Serial_rw(){
  if (Serial.available() > 0) {
    String str = Serial.readStringUntil('\n');
    if(str != ""){
      char* c_str = str.c_str();
      int msg_type = atoi( strtok(c_str, " ") );
      int control_type = 0;
      switch (msg_type){
        case 0:
          Serial.println("reset");
        case 1: //Control pose
          control_type = atoi( strtok(NULL, " ") );
          X = atof( strtok(NULL, " ") );
          Y = atof( strtok(NULL, " ") );
          theta = atof(strtok(NULL, " "));
          break;
        case 2: //Control arm
          control_type = atoi( strtok(NULL, " ") );
          for(int i=0; i<4; i++)
            now_angle[i] = atof(strtok(NULL, " "));
          break;
        case 3: //Control slide
          control_type = atoi( strtok(NULL, " ") );
          encoder = atoi(strtok(NULL, " "));
          break;
        case 4:
          printInfo();
          break;
        default:
          break;
      }
    }
  }
}

void printInfo(){
    Serial.print(millis());
    Serial.print(" ");
    Serial.print(12.5);
    Serial.print(" ");
    Serial.print(X);
    Serial.print(" ");
    Serial.print(Y);
    Serial.print(" ");
    Serial.print(theta);
    Serial.print(" ");
    Serial.print(now_angle[0]);
    Serial.print(" ");
    Serial.print(now_angle[1]);
    Serial.print(" ");
    Serial.print(now_angle[2]);
    Serial.print(" ");
    Serial.print(now_angle[3]);
    Serial.print(" ");
    Serial.print(encoder);
    Serial.print("\n");
    
}

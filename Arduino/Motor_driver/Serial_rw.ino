void Serial_rw(){
    if (Serial.available() > 0) {
        String str = Serial.readStringUntil('\n');
        if(str != ""){
            char* c_str = str.c_str();
            int msg_type = atoi( strtok(c_str, " ") );
            String substr = strtok(NULL, "");
            switch (msg_type){
                case 0:
                    arm.workType = 112;
                    car.control_type = -3;
                    car.reset();
                    slide.reset();
                case 1: //Control pose
                    car.Serial_r(substr);
                    break;
                case 2: //Control arm
                    arm.Serial_r(substr);
                    break;
                case 3: //Control slide
                    slide.Serial_r(substr);
                    break;
                case 4:
                    print_type = atoi(substr.c_str());
                    break;
                default:
                    arm.workType = 112;
                    car.control_type = -3;
                    car.reset();
                    slide.reset();
                    break;
            }
        }
    }
}

void printInfo(){
        double V = analogRead(AD);
        Serial.print(timer);
        Serial.print(" ");
        Serial.print(V/18.21);
        Serial.print(" ");
        Serial.print(car.X);
        Serial.print(" ");
        Serial.print(car.Y);
        Serial.print(" ");
        Serial.print(car.theta);
        Serial.print(" ");
        Serial.print(arm.Y);
        Serial.print(" ");
        Serial.print(arm.Z);
        Serial.print(" ");
        Serial.print(arm.is_motion_finish());
        Serial.print(" ");
        Serial.print(slide.encoder);
        Serial.print(" ");
        Serial.print(slide.desire_encode);
        Serial.print(" ");
        Serial.print("\n");
        
}

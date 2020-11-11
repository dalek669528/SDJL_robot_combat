void processInfo(){
  
    String intput_string =Serial.readString();
    char* intput_string_c = intput_string.c_str();
    char* workTypeString = NULL;
    int counter=0;
    float desireAngle_array[4];
    float pointYZ[2];
  
    if(intput_string != ""){
        workTypeString = strtok(intput_string_c," ");
        int workType = atof(workTypeString);
        char* substr = strtok(NULL," ");

        Serial.print("Working type : ");
        Serial.println(workType);
        
        switch(workType) {

            case 111:
                moveServoGroup(0, SERVO_GETBACK_STATE);
                
                break;

            case 112:
                moveServoGroup(0, SERVO_READY_STATE);
                
                break;

            case 121:
                do{
                    float angle=atof(substr);
                    desireAngle_array[counter]=angle;
                    substr = strtok(NULL," ");
                    counter++;
                }while(substr);
                moveServoGroup(0, desireAngle_array);
                break;


            case 211:

                break;
          
            case 221:
                do{
                    float axis=atof(substr);
                    pointYZ[counter]=axis;
                    substr = strtok(NULL," ");
                    counter++;
                }while(substr);

                if(pointYZ[0] > ARM_PICK_LOWER_BOUND && pointYZ[0] < ARM_PICK_UPPER_BOUND){
                    //pointYZ[1] = ARM_PICK_HEIGHT;
                    moveServo(3, 30);
                    movetoPoint(0, pointYZ);
                    //Pick up
                    moveServo(3, 60);
                    //
                    moveServoGroup(0, SERVO_PICKUP_STATE);   
                }
                break;

            case 222:

                do{
                    float axis=atof(substr);
                    pointYZ[counter]=axis;
                    substr = strtok(NULL," ");
                    counter++;
                }while(substr);
                
                movetoPoint(60, pointYZ);
                moveServo(3, 30);
                moveServoGroup(0, SERVO_READY_STATE);
                
                break;


            
            case 231:

                break;
            case 1:
                //autoPick();
                moveServoGroup(0, SERVO_READY_STATE);
                break;
            case 2:
                fantasyBaby();
                break;
            case 3:
               
                
                break;
            default:
                break;
        }
    }
}

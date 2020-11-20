Slide::Slide(){
    control_type = pwm = encoder = 0;
    Kp = Ki = Kd = 0;
    err = err_sum = err_past = 0;
    MAX_ENCODER = 250;
    MIN_ENCODER = 0;
    is_init = false;
}
void Slide::set_PID(float p, float i, float d, float pb, float ib, float db){
    Kp = p;
    Ki = i;
    Kd = d;
    Kp_b = pb;
    Ki_b = ib;
    Kd_b = db;
}

void Slide::PWM_Calculate(){
    if(!is_init){
        encoder = 10;
        desire_encode = 0;
        control_type = 2; 
    }
    
    if(control_type == 2){
        
        desire_encode = (desire_encode >= MAX_ENCODER) ? MAX_ENCODER : desire_encode;
        desire_encode = (desire_encode <= MIN_ENCODER) ? MIN_ENCODER : desire_encode;

        err = desire_encode - encoder;
        err = (err >=  20) ?  20 : err;
        err = (err <= -20) ? -20 : err;
        err_sum += err;
        if(err > 0)
            pwm = Kp * err + Ki * err_sum + Kd * (err - err_past);
        else if(err < 0)
            pwm = Kp_b * err + Ki_b * err_sum + Kd_b * (err - err_past);
        else{
            pwm = 0;
            err_sum = 0;
        }
        if(pwm >= S_MAX_PWM || pwm <= -S_MAX_PWM){
            err_sum -= err;
        }
        err_past = err;
    }
    else
        desire_encode = encoder;
        
}
void Slide::reset_error(){
    err = 0;
    err_sum = 0;
    err_past = 0;
    pwm = 0;
}

void Slide::Slide_Control(){
    if(digitalRead(button)){
        is_init = true;
        reset_error();
        encoder = 0;
        if(desire_encode < 10)
            desire_encode = 10;
    }
    if( (encoder < (MAX_ENCODER + 10)) && (encoder > (MIN_ENCODER - 10)) ){
        if((pwm < 0)) { //反转
            analogWrite(Motor_S1, (-pwm) > 255 ? 255 : (-pwm));
            analogWrite(Motor_S2, 0);
        }
        else{ //正转
            analogWrite(Motor_S1, 0);
            analogWrite(Motor_S2, pwm > 255 ? 255 : pwm);
        }
    }
    else
        reset();
}

void Slide::Serial_r(String str){
    int control_type_past = control_type;
    reset_error();
    char* intput_string_c = str.c_str();
    if (str != "") {
        control_type = atoi( strtok(intput_string_c, " "));
        switch (control_type){
            case 1:
                pwm = atoi(strtok(NULL, " "));
                break;
            case 2:
                desire_encode = atoi(strtok(NULL, " "));
                break;
            case 3:
                control_type = control_type_past;
                encoder = 0;
                break;
            case 4:
                control_type = control_type_past;
                Kp = atof(strtok(NULL, " "));
                Ki = atof(strtok(NULL, " "));
                Kd = atof(strtok(NULL, " "));
                break;
            case 5:
                control_type = control_type_past;
                Kp_b = atof(strtok(NULL, " "));
                Ki_b = atof(strtok(NULL, " "));
                Kd_b = atof(strtok(NULL, " "));
                break;
            default:
                control_type = -3;
                control_type_past = control_type = 0;
                desire_encode = encoder;
                pwm = 0;
                break;
        }
    }
}

void Slide::printInfo(){
    Serial.print(control_type);
    Serial.print(" ");
    Serial.print(Kp);
    Serial.print(" ");
    Serial.print(Ki);
    Serial.print(" ");
    Serial.print(Kd);
    Serial.print(" / ");
    Serial.print(Kp_b);
    Serial.print(" ");
    Serial.print(Ki_b);
    Serial.print(" ");
    Serial.print(Kd_b);
    Serial.print(" | ");
    Serial.print(err);
    Serial.print(" ");
    Serial.print(err_sum);
    Serial.print(" ");
    Serial.print(err_past);
    Serial.print(" ");
    Serial.print(pwm);
    Serial.print(" Desire: ");
    Serial.print(desire_encode);
    Serial.print(" / ");
    Serial.println(encoder);
}

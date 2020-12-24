void Car::Serial_r(String str){
    reset_error();
    if(str.indexOf(' ') != -1){
        char* c_str = str.c_str();
        control_type = atoi( strtok(c_str, " ") );
        switch(control_type){
            case 1:
                A.pwm = atoi( strtok(NULL, " ") );
                B.pwm = atoi( strtok(NULL, " ") );
                C.pwm = atoi( strtok(NULL, " ") );
                D.pwm = atoi( strtok(NULL, " ") );
                break;
            case 2:
                A.desire_V = atof( strtok(NULL, " ") );
                B.desire_V = atof( strtok(NULL, " ") );
                C.desire_V = atof( strtok(NULL, " ") );
                D.desire_V = atof( strtok(NULL, " ") );
                break;
            case 3:
                desire_Vx = atof( strtok(NULL, " ") );
                desire_Vy = atof( strtok(NULL, " ") );
                desire_w = atof( strtok(NULL, " ") ) * PI / 180.0;
                break;
            case 4:
                desire_X = atof( strtok(NULL, " ") );
                desire_Y = atof( strtok(NULL, " ") );
                desire_theta = atoi( strtok(NULL, " ") );
                desire_theta = (desire_theta > 180) ? (desire_theta - 360) : desire_theta;
                desire_theta = (desire_theta < -180) ? (desire_theta + 360) : desire_theta;
                break;
                break;
            case 5:
                desire_X += atof( strtok(NULL, " ") );
                desire_Y += atof( strtok(NULL, " ") );
                desire_theta += atoi( strtok(NULL, " ") );
                desire_theta = (desire_theta > 180) ? (desire_theta - 360) : desire_theta;
                desire_theta = (desire_theta < -180) ? (desire_theta + 360) : desire_theta;
                break;
            case -2:
                desire_X = X = atof( strtok(NULL, " ") );
                desire_Y = Y = atof( strtok(NULL, " ") );
                desire_theta = theta = atof( strtok(NULL, " ") );
                break;
            case -1:
                int changePID, p, i, d; 
                changePID = atoi( strtok(NULL, " ") );
                p = atof( strtok(NULL, " ") );
                i = atof( strtok(NULL, " ") );
                d = atof( strtok(NULL, " ") );
                switch(changePID){
                    case 0:
                        A.set_PID(p, i, d);
                        break;
                    case 1:
                        B.set_PID(p, i, d);
                        break;
                    case 2:
                        C.set_PID(p, i, d);
                        break;
                    case 3:
                        D.set_PID(p, i, d);
                        break;
                    case 4:
                        p_Kp = p;
                        p_Ki = i;
                        p_Kd = d;
                        break;
                }
                control_type = past_control_type;
            default:
                control_type = -3;
                reset();
        }
        past_control_type = control_type;
    }
    else{
        past_control_type = control_type = -3;
        car_stop();
    }
}
    
void Car::printInfo(){
    Serial.print(print_timer);
    Serial.print(" ");
    Serial.print(control_type);
    Serial.print(" ");
    Serial.print(X);
    Serial.print(" ");
    Serial.print(Y);
    Serial.print(" ");
    Serial.print(theta);
    Serial.print(" / ");
    Serial.print(Vx);
    Serial.print(" ");
    Serial.print(Vy);
    Serial.print(" ");
    Serial.print(w);
    Serial.print(" / ");
    Serial.print(A.v);
    Serial.print(" ");
    Serial.print(B.v);
    Serial.print(" ");
    Serial.print(C.v);
    Serial.print(" ");
    Serial.print(D.v);
    Serial.print(" / ");
    Serial.print(p_Kp);
    Serial.print(" ");
    Serial.print(p_Ki);
    Serial.print(" ");
    Serial.print(p_Kd);
    Serial.print(" \n");
}

void Car::PWM_Calculate(){
    
    A.speed_renew(timer);
    B.speed_renew(timer);
    C.speed_renew(timer);
    D.speed_renew(timer);
    
    Vx = (-A.v + B.v - C.v + D.v)/4;
    Vy = (A.v + B.v + C.v + D.v)/4;



    w = (A.v + B.v - C.v - D.v)/(4*(W+L)) * 180 / PI;
    X += (-A.delta_x + B.delta_x - C.delta_x + D.delta_x)/4;
    Y += (A.delta_x + B.delta_x + C.delta_x + D.delta_x)/4;
    theta += ((A.delta_x + B.delta_x - C.delta_x - D.delta_x)/(4*(W+L))) * 180 / PI;
    theta = (theta > 180) ? (theta - 360) : theta;
    theta = (theta < -180) ? (theta + 360) : theta;

    if(control_type >= 4){
        position_PID();
    }
    if(control_type >= 3){
        A.desire_V = - desire_Vx + desire_Vy + desire_w*(W+L);
        B.desire_V =     desire_Vx + desire_Vy + desire_w*(W+L);
        C.desire_V = - desire_Vx + desire_Vy - desire_w*(W+L);
        D.desire_V =     desire_Vx + desire_Vy - desire_w*(W+L);
    }
    if(control_type > 1){
        A.pwm_calculate();
        B.pwm_calculate();
        C.pwm_calculate();
        D.pwm_calculate();
    }
}

void Car::position_PID()
{
    pos_err[0] = desire_X - X;
    pos_err[1] = desire_Y - Y;

    pos_err_sum[0] += pos_err[0];
    pos_err_sum[1] += pos_err[1];
 
    desire_Vx = pos_err[0]*p_Kp + pos_err_sum[0]*p_Ki + (pos_err[0] - pos_err_past[0])*p_Kd;
    desire_Vy = pos_err[1]*p_Kp + pos_err_sum[1]*p_Ki + (pos_err[0] - pos_err_past[0])*p_Kd;

    pos_err_past[0] = pos_err[0];
    pos_err_past[1] = pos_err[1];


    if(abs(pos_err[0]) < 1 && abs(pos_err[1]) < 1){
        pos_err[2] = desire_theta - theta;
        if(pos_err[2]>180)
            pos_err[2] -= 360;
        else if(pos_err[2] <= -180){
            pos_err[2] += 360;
        }
        pos_err_sum[2] += pos_err[2];
        desire_w = (pos_err[2]*p_Kp + pos_err_sum[2]*p_Ki + (pos_err[0] - pos_err_past[0])*p_Kd) * PI / 180.0;
        pos_err_past[2] = pos_err[2];
    }
    else{
        desire_w = 0;
    }
    
}

void Car::Car_Control(){
    if(A.pwm < 0) { //反转
        analogWrite(MotorA1, 0); //MotorA1置0时电机反转
        analogWrite(MotorA2, (-A.pwm) > MAX_PWM ? MAX_PWM : (-A.pwm));
    }
    else { //正转
        analogWrite(MotorA1, A.pwm > MAX_PWM ? MAX_PWM : A.pwm);
        analogWrite(MotorA2, 0); //MotorA2置0时电机正转
    }
    
    if(B.pwm < 0) { //反转
        analogWrite(MotorB1, 0); //MotorB1置0时电机反转
        analogWrite(MotorB2, (-B.pwm) > MAX_PWM ? MAX_PWM : (-B.pwm));
    }
    else { //正转
        analogWrite(MotorB1, B.pwm > MAX_PWM ? MAX_PWM : B.pwm);
        analogWrite(MotorB2, 0); //MotorB2置0时电机正转
    }
    if(C.pwm < 0) { //反转
        analogWrite(MotorC1, 0); //MotorB1置0时电机反转
        analogWrite(MotorC2, (-C.pwm) > MAX_PWM ? MAX_PWM : (-C.pwm));
    }
    else { //正转
        analogWrite(MotorC1, C.pwm > MAX_PWM ? MAX_PWM : C.pwm);
        analogWrite(MotorC2, 0); //MotorB2置0时电机正转
    }
    if(D.pwm < 0) { //反转
        analogWrite(MotorD1, 0); //MotorB1置0时电机反转
        analogWrite(MotorD2, (-D.pwm) > MAX_PWM ? MAX_PWM : (-D.pwm));
    }
    else { //正转
        analogWrite(MotorD1, D.pwm > MAX_PWM ? MAX_PWM : D.pwm);
        analogWrite(MotorD2, 0); //MotorB2置0时电机正转
    }
//    const int half_pwm = 128; 
//    analogWrite(MotorC2, half_pwm); //MotorC1置0时电机反转
//    if(C.pwm < 0) { //反转
//        analogWrite(MotorC1, (half_pwm- ( (-C.pwm) > MAX_PWM ? MAX_PWM : (-C.pwm)) ) );
//    }
//    else { //正转
//        analogWrite(MotorC1, C.pwm>MAX_PWM ? (MAX_PWM + half_pwm) : (C.pwm + half_pwm ));
//    }
//
//    if(D.pwm < 0) { //反转
//        analogWrite(MotorD1, (half_pwm- ( (-D.pwm) > MAX_PWM ? MAX_PWM : (-D.pwm)) ) );
//        analogWrite(MotorD2, 0 );
//
//    }
//    else { //正转
//        analogWrite(MotorD1, D.pwm>MAX_PWM ? (MAX_PWM + half_pwm) : (D.pwm + half_pwm ));
//        analogWrite(MotorD2, 255);
//    }
}

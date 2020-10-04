#ifndef WHEEL_H
#define WHEEL_H
class Wheel{
  public:
    int pwm;
    int encoder, encoder_past;
    double Kp, Ki, Kd;
    double deg, w, v;
    Wheel(){
      pwm = encoder = encoder_past = 0;
      Kp = Ki = Kd = 0;
      deg = w = v = 0;
    }
    Wheel(int p){
      pwm = p;
      encoder = encoder_past = 0;
      Kp = Ki = Kd = 0;
      deg = w = v = 0;
    }
    void speed_cal(){
      deg = (encoder - encoder_past) / CPR * PI * 2 * TIRE_RADIUS;
      v = (encoder - encoder_past)/CPR*PI*2*TIRE_RADIUS/(millis()-SpeedTimer)*1000; //cm/sec
      SpeedTimer = millis();
      encoder_past = encoder;
    }
};

#endif

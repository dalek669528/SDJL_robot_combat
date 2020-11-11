#ifndef WHEEL_H
#define WHEEL_H
#define CPR 390 //count per round
#define TIRE_RADIUS 3 //3cm
class Wheel{
  public:
    int pwm;
    long encoder, encoder_past;
    double Kp, Ki, Kd;
    double x, w, v;
    uint32_t SpeedTimer;
    Wheel(){
      pwm = encoder = encoder_past = 0;
      Kp = Ki = Kd = 0;
      x = w = v = 0;
    }
    Wheel(int p){
      pwm = p;
      encoder = encoder_past = 0;
      Kp = Ki = Kd = 0;
      x = w = v = 0;
      SpeedTimer = millis();
    }
    void speed_renew(){
      x = (encoder - encoder_past) / CPR * PI * 2 * TIRE_RADIUS;
      v = (encoder - encoder_past)/CPR*PI*2*TIRE_RADIUS/(millis()-SpeedTimer)*1000; //cm/sec
      SpeedTimer = millis();
      encoder_past = encoder;
    }
};

#endif

#ifndef WHEEL_H
#define WHEEL_H
#define CPR 390 //count per round
#define TIRE_RADIUS 3 //3cm
class Wheel{
  public:
    int pwm;
    long encoder, encoder_past;
    float Kp, Ki, Kd;
    float delta_x, w, v;
    float desire_V;
    uint32_t SpeedTimer;
    float err, err_sum, err_past;
    Wheel(){
      pwm = encoder = encoder_past = 0;
      Kp = Ki = Kd = 0;
      delta_x = w = v = 0;
      err = err_sum = err_past = 0;
    }
    Wheel(int p){
      pwm = p;
      encoder = encoder_past = 0;
      Kp = Ki = Kd = 0;
      delta_x = w = v = 0;
      SpeedTimer = millis();
    }
    void set_PID(float p, float i, float d){
      Kp = p;
      Ki = i;
      Kd = d;
    }
    void speed_renew(uint32_t timer){
      delta_x = (float)(encoder - encoder_past) / CPR * PI * 2 * TIRE_RADIUS;
      v = delta_x / (timer-SpeedTimer)*1000; //cm/sec
      SpeedTimer = timer;
      encoder_past = encoder;
    }
    void pwm_calculate(){
      float desire_V_temp = desire_V;
      if(desire_V_temp > 25){
        desire_V_temp = 25;
      }
      else if(desire_V_temp < -25){
        desire_V_temp = -25;
      }
      err = desire_V_temp - v;
      err_sum += err;
      pwm = Kp * err + Ki * err_sum + Kd * (err - err_past);
      err_past = err;
    }
    void reset_error(){
      err = 0;
      err_sum = 0;
      err_past = 0;
      pwm = 0;
    }
};

#endif

#include <Servo.h>   //載入函式庫，這是內建的，不用安裝


//#define SERVO1_PIN 11
//#define SERVO2_PIN 10
//#define SERVO3_PIN 9
//#define SERVO4_PIN 6
#define SERVO1_PIN A3
#define SERVO2_PIN A4
#define SERVO3_PIN A5
#define SERVO4_PIN A6

struct motor_struct {
    Servo myservo;
    float desireAngle = 0;
    int pwm_past = 1500;//transform(90)
};

int motor_speed = 20;
motor_struct motor_array[4];

unsigned long time;

void setup() {
    Serial.begin(9600);  //設定通訊速率
    motor_array[0].myservo.attach(SERVO1_PIN, 500, 2500); // 修正脈衝寬度範圍
    motor_array[1].myservo.attach(SERVO2_PIN, 500, 2500); // 修正脈衝寬度範圍
    motor_array[2].myservo.attach(SERVO3_PIN, 500, 2500); // 修正脈衝寬度範圍
    motor_array[3].myservo.attach(SERVO4_PIN, 500, 2500); // 修正脈衝寬度範圍
    motor_array[0].myservo.writeMicroseconds(1500);
    motor_array[1].myservo.writeMicroseconds(1500);
    motor_array[2].myservo.writeMicroseconds(1500);
    motor_array[3].myservo.writeMicroseconds(1500);
//    float angle_array[4] = {120, -60, -60, 30};
//    for(int i=0;i<4;i++)
//      motor_array[i].pwm_past = transform(angle_array[i]);
    
//    moveServoGroup(1, angle_array);
}

void loop() {   

  while (Serial.available()>0) {   //如果暫存器有訊號則不斷讀取直到沒有
    Serial.print("Time: ");
    time = millis();
    Serial.println(time); //prints time since program started
    
//    processInfo();
    
    Serial.print("Time: ");
    time = millis();
    Serial.println(time); //prints time since program started
  }
}

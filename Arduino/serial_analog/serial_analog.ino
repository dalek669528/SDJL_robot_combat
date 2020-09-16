//////////////////TBN四路驱动引脚接线///////////////////////////
//电机-------------TBN四路驱动丝印标识----------ESP8266主板引脚
//电机-------------DATA_ABC牛角座-----------ESP8266主板引脚
//                     EN(使能)------------2
//                     5V-----------------5V
//                     AD-----------------A0
//                     G------------------GND
//                     A1-----------------3
//                     A2-----------------5
//                     B1-----------------6
//                     B2-----------------9
//                     C1-----------------10
//                     C2-----------------11

//电机-------------DATA_D牛角座--------------ESP8266主板引脚
//                     5V------------------(与DATA_ABC牛角座5V引脚导通，两者可以只接通1个)
//                     G-------------------(与DATA_ABC牛角座5V引脚导通，两者可以只接通1个)
//                     EN------------------(与DATA_ABC牛角座5V引脚导通，两者可以只接通1个)
//                     D2------------------13
//                     D1------------------12
//                     NC(悬空)------------
//                     NC(悬空)------------
//                     NC(悬空)------------
//                     NC(悬空)------------
//                     NC(悬空)------------
//直流电机A-------------MotorA
//直流电机B-------------MotorB
//直流电机C-------------MotorC
//直流电机D-------------MotorD
//电机-------------TBN四路驱动丝印标识----------ESP8266主板引脚

static const uint8_t D0   = 16;
static const uint8_t D1   = 5;
static const uint8_t D2   = 4;
static const uint8_t D3   = 0;
static const uint8_t D4   = 2;
static const uint8_t D5   = 14;
static const uint8_t D6   = 12;
static const uint8_t D7   = 13;
static const uint8_t D8   = 15;
static const uint8_t RX   = 3;
static const uint8_t TX   = 1;

const uint8_t EN = 2;
const uint8_t AD = A0;
const uint8_t MotorA1 = D1;
const uint8_t MotorA2 = D2;
int pwm = 10;         // incoming serial byte

void setup() {
  //引脚功能初始化
  pinMode(AD, INPUT);
  pinMode(EN, OUTPUT);
  pinMode(MotorA1, OUTPUT);
  pinMode(MotorA2, OUTPUT);
  
  digitalWrite(EN, 1); 
  analogWrite(MotorA1, 0);
  analogWrite(MotorA2, 0);
  Serial.begin(115200);
  while (!Serial) {}
}

void SetPowerA(int direction, int power)
{
  int pwm=255*power/100; //输出到模拟引脚的PWM信号范围为0~255
  if(direction==1) //正转
  {
   analogWrite(MotorA1, 0); //MotorA1置0时电机正转
   analogWrite(MotorA2, pwm); 
  }
  else if(direction==0) //反转
  {
   analogWrite(MotorA1, pwm);
   analogWrite(MotorA2, 0); //MotorA2置0时电机反转
  }
}

void loop() {
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    String str = Serial.readString();
    // read second analog input, divide by 4 to make the range 0-255:
    pwm = str.toInt();
    Serial.print("Serial read:");
    Serial.println(pwm);
    double V=analogRead(AD);
    Serial.print(V/18.21);
    Serial.print(" V");
    Serial.print(V);
    Serial.println("V");
    delay(500);
  }
  SetPowerA(1, pwm);
  delay(2000);
}

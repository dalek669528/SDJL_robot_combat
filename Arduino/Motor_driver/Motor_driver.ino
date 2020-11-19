#include "Car.h"
#include "Arm.h"

Car car;
Arm arm;
Slide slide;

int period = 50;
int print_period = 250;
uint32_t timer;
uint32_t timer2;
uint32_t print_timer;
int print_type = 0;

void setup(){
    Pin_init();
    arm.init();
    slide.set_PID(6, 0.03, 5, 15, 0.5, 15);
    timer = millis();
    Serial.begin(115200);
    while (!Serial) {}    // wait for serial port to connect.
}

void loop() {
    timer2 = millis();
    if(timer2 >= timer + period){
        timer = (timer2/(period))*(period);
        Serial_rw();
        car.PWM_Calculate();
        slide.PWM_Calculate();
        arm.Routine();
        arm.Arm_Control();
//        switch(print_type){
//            case 2:
//                car.printInfo();
//                break;
//            case 3:
//                arm.printInfo(-1);
//                break;
//            case 4:
//                slide.printInfo();
//                break;
//            default:
//                break;
//        }
    }
    if(timer2 >= print_timer + print_period){
        print_timer = (timer2/(print_period))*(print_period);
        switch(print_type){
            case 1:
                printInfo();
                break;
            case 2:
                car.printInfo();
                break;
            case 3:
                arm.printInfo(-1);
                break;
            case 4:
                slide.printInfo();
                break;
            default:
                break;
        }
    }
    car.Car_Control();
    slide.Slide_Control();
}

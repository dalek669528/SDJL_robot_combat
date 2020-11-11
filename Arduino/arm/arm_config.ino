//Servo const variable
static const int SERVO_OFFSET[4]       = {0,    90,  90,   0};
static const int SERVO_POSITIVE[4]     = {1,    -1,  -1,   1};
static const int SERVO_LOWER_BOUND[4]  = {0,     0,   0,  30};
static const int SERVO_UPPER_BOUND[4]  = {180, 180, 180,  90};
//static const uint8_t SERVO_INIT_STATE[4]  = {180, 180, 180,  90};

//Servo state
static const float   SERVO_GETBACK_STATE[4] = {90,   80,   0,  30};
static const float   SERVO_READY_STATE[4]   = {120, -60, -60,  30};
static const float   SERVO_PICKUP_STATE[4]  = {120, -60, -60,  60};
static const float   SERVO_LENGTH[3]        = {10.6, 7.8, 14};
//static const float   ARM_AXIS_OFFSET       = 6.9;
static const float   ARM_AXIS_OFFSET        = 0;

//Pick const variable
static const float   ARM_PICK_HEIGHT       = 14;
static const float   ARM_PICK_LOWER_BOUND  = 12;
static const float   ARM_PICK_UPPER_BOUND  = 40;

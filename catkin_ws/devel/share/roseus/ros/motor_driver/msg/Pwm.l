;; Auto-generated. Do not edit!


(when (boundp 'motor_driver::Pwm)
  (if (not (find-package "MOTOR_DRIVER"))
    (make-package "MOTOR_DRIVER"))
  (shadow 'Pwm (find-package "MOTOR_DRIVER")))
(unless (find-package "MOTOR_DRIVER::PWM")
  (make-package "MOTOR_DRIVER::PWM"))

(in-package "ROS")
;;//! \htmlinclude Pwm.msg.html


(defclass motor_driver::Pwm
  :super ros::object
  :slots (_pwmA _pwmB ))

(defmethod motor_driver::Pwm
  (:init
   (&key
    ((:pwmA __pwmA) 0)
    ((:pwmB __pwmB) 0)
    )
   (send-super :init)
   (setq _pwmA (round __pwmA))
   (setq _pwmB (round __pwmB))
   self)
  (:pwmA
   (&optional __pwmA)
   (if __pwmA (setq _pwmA __pwmA)) _pwmA)
  (:pwmB
   (&optional __pwmB)
   (if __pwmB (setq _pwmB __pwmB)) _pwmB)
  (:serialization-length
   ()
   (+
    ;; int32 _pwmA
    4
    ;; int32 _pwmB
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _pwmA
       (write-long _pwmA s)
     ;; int32 _pwmB
       (write-long _pwmB s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _pwmA
     (setq _pwmA (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _pwmB
     (setq _pwmB (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get motor_driver::Pwm :md5sum-) "0c46853c782ce10c35ceede0e24a5cb8")
(setf (get motor_driver::Pwm :datatype-) "motor_driver/Pwm")
(setf (get motor_driver::Pwm :definition-)
      "int32 pwmA
int32 pwmB

")



(provide :motor_driver/Pwm "0c46853c782ce10c35ceede0e24a5cb8")



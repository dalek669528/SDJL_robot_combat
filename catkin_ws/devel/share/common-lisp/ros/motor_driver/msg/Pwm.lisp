; Auto-generated. Do not edit!


(cl:in-package motor_driver-msg)


;//! \htmlinclude Pwm.msg.html

(cl:defclass <Pwm> (roslisp-msg-protocol:ros-message)
  ((pwmA
    :reader pwmA
    :initarg :pwmA
    :type cl:integer
    :initform 0)
   (pwmB
    :reader pwmB
    :initarg :pwmB
    :type cl:integer
    :initform 0))
)

(cl:defclass Pwm (<Pwm>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Pwm>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Pwm)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name motor_driver-msg:<Pwm> is deprecated: use motor_driver-msg:Pwm instead.")))

(cl:ensure-generic-function 'pwmA-val :lambda-list '(m))
(cl:defmethod pwmA-val ((m <Pwm>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motor_driver-msg:pwmA-val is deprecated.  Use motor_driver-msg:pwmA instead.")
  (pwmA m))

(cl:ensure-generic-function 'pwmB-val :lambda-list '(m))
(cl:defmethod pwmB-val ((m <Pwm>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motor_driver-msg:pwmB-val is deprecated.  Use motor_driver-msg:pwmB instead.")
  (pwmB m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Pwm>) ostream)
  "Serializes a message object of type '<Pwm>"
  (cl:let* ((signed (cl:slot-value msg 'pwmA)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'pwmB)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Pwm>) istream)
  "Deserializes a message object of type '<Pwm>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'pwmA) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'pwmB) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Pwm>)))
  "Returns string type for a message object of type '<Pwm>"
  "motor_driver/Pwm")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Pwm)))
  "Returns string type for a message object of type 'Pwm"
  "motor_driver/Pwm")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Pwm>)))
  "Returns md5sum for a message object of type '<Pwm>"
  "0c46853c782ce10c35ceede0e24a5cb8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Pwm)))
  "Returns md5sum for a message object of type 'Pwm"
  "0c46853c782ce10c35ceede0e24a5cb8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Pwm>)))
  "Returns full string definition for message of type '<Pwm>"
  (cl:format cl:nil "int32 pwmA~%int32 pwmB~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Pwm)))
  "Returns full string definition for message of type 'Pwm"
  (cl:format cl:nil "int32 pwmA~%int32 pwmB~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Pwm>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Pwm>))
  "Converts a ROS message object to a list"
  (cl:list 'Pwm
    (cl:cons ':pwmA (pwmA msg))
    (cl:cons ':pwmB (pwmB msg))
))

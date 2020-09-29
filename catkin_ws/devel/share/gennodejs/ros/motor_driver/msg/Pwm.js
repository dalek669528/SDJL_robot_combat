// Auto-generated. Do not edit!

// (in-package motor_driver.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Pwm {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.pwmA = null;
      this.pwmB = null;
    }
    else {
      if (initObj.hasOwnProperty('pwmA')) {
        this.pwmA = initObj.pwmA
      }
      else {
        this.pwmA = 0;
      }
      if (initObj.hasOwnProperty('pwmB')) {
        this.pwmB = initObj.pwmB
      }
      else {
        this.pwmB = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Pwm
    // Serialize message field [pwmA]
    bufferOffset = _serializer.int32(obj.pwmA, buffer, bufferOffset);
    // Serialize message field [pwmB]
    bufferOffset = _serializer.int32(obj.pwmB, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Pwm
    let len;
    let data = new Pwm(null);
    // Deserialize message field [pwmA]
    data.pwmA = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [pwmB]
    data.pwmB = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'motor_driver/Pwm';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0c46853c782ce10c35ceede0e24a5cb8';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 pwmA
    int32 pwmB
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Pwm(null);
    if (msg.pwmA !== undefined) {
      resolved.pwmA = msg.pwmA;
    }
    else {
      resolved.pwmA = 0
    }

    if (msg.pwmB !== undefined) {
      resolved.pwmB = msg.pwmB;
    }
    else {
      resolved.pwmB = 0
    }

    return resolved;
    }
};

module.exports = Pwm;

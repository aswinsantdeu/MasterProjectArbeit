import time, os
import threading
import socket
from dronekit import connect

#current_time = int(time.time() * 1e9) # Current Timestamp

# Connect to Pixhawk
vehicle = connect("/dev/ttyACM0", baud=57600, wait_ready=True)
vehicle.wait_ready(’autopilot_version’)

def pixhawk_logger():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
          s.connect(("localhost", 5000)) # Connect to the local socket server on the port 5000
          while vehicle:
                  roll = vehicle.attitude.roll
                  pitch = vehicle.attitude.pitch
                  yaw = vehicle.attitude.yaw
                  print(f"Roll={roll}")
                  print(f"Pitch={pitch}")
                  print(f"Yaw={yaw}")
                  gndspeed = vehicle.groundspeed
                  #pv_airspeed.post(vehicle.airspeed, timestamp = current_time)
                  #vehicle.parameters["ARMING_CHECK"] = 0
                  #print(vehicle.parameters["ARMING_CHECK"])
                  vehicle.armed = True
                  Vehicle_armed = int(vehicle.armed)
                  #print(Vehicle_armed)
                  #print(f"Is vehicle armable ? {vehicle.is_arm)
                  Vehicle_state = vehicle.system_status.state
                  #print(Vehicle_state)
                  Vehicle_mode = vehicle.mode.name
                  #print(Vehicle_mode)
                  pwm1_min = vehicle.parameters.get("RC1_MIN", 0.0)
                  pwm1_max = vehicle.parameters.get("RC1_MAX", 0.0)
                  pwm3_min = vehicle.parameters.get("RC3_MIN", 0.0)
                  pwm3_max = vehicle.parameters.get("RC3_MAX", 0.0)
                  throttle = vehicle.channels[3] or 0.0 # Default to 0.0 if None
                  print("ThrottleRCIN:",throttle)
                  rudder = vehicle.channels[1] or 0.0 # Default to 0.0 if None
                  print("RudderRCIN",rudder)
                  #def listener(vehicle, name, message):
                  #
                  global ThrottleOP,RudderOP
                  #
                  #
                  ThrottleOP = message.servo1_raw
                  RudderOP
                  = message.servo3_raw
                  #vehicle.add_message_listener(’SERVO_OUTPUT_RAW’,listener)
                  print()
                  throttle_percentage = (throttle- pwm3_min) / (pwm3_max- pwm3_min) * 100
                  rudder_percentage = (rudder- pwm1_min) / (pwm1_max- pwm1_min) * 100
                  batteryvoltage = vehicle.battery.voltage or 0.0 # Default to 0.0 if None
                  batterycurrent = vehicle.battery.current or 0.0 # Default to 0.0 if None
                  message = f"pixhawk:{roll},{pitch},{yaw},{gndspeed},{Vehicle_armed},{throttle_percentage},{rudder_percentage},{batteryvoltage},{batterycurrent}|"
                  #print(message)
                  s.sendall(message.encode())
                  time.sleep(1)
            
if __name__ == ’__main__’:
        pixhawk_logger()

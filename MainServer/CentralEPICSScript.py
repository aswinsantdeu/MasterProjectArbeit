import time, os
import threading
import socket
from p4p.client.thread import Context
from p4p.nt import NTScalar
from p4p.server import Server
from p4p.server.thread import SharedPV
from dronekit import connect
#current_time = int(time.time() * 1e9) # Current Timestamp
# Define EPICS PVs
pv_roll = SharedPV(nt=NTScalar(’d’), initial=0.0)
pv_pitch = SharedPV(nt=NTScalar(’d’), initial=0.0)
pv_yaw = SharedPV(nt=NTScalar(’d’), initial=0.0)
pv_groundspeed = SharedPV(nt=NTScalar(’d’), initial=0.0)
#pv_airspeed = SharedPV(nt=NTScalar(’d’), initial=0.0)
pv_armed = SharedPV(nt=NTScalar(’d’), initial=0.0) # Integer for armed status (0/1)
#pv_state = SharedPV(nt=NTScalar(’s’), initial="Idle")
#pv_mode = SharedPV(nt=NTScalar(’s’), initial="Idle")
#pv_pwm_min = SharedPV(nt=NTScalar(’d’), initial=0.0) # Channel 3 Min PWM
#pv_pwm_max = SharedPV(nt=NTScalar(’d’), initial=0.0) # Channel 3 Max PWM
#pv_pwm_trim = SharedPV(nt=NTScalar(’d’), initial=0.0) # Channel 3 Trim PWM
#pv_ch_ThrPwmOutput = SharedPV(nt=NTScalar(’d’), initial=0.0) # Channel 3 Throttle Output in PWM
pv_ThrOutput = SharedPV(nt=NTScalar(’d’), initial=0.0) # Channel 3 Throttle Output in Percentage
pv_RudOutput = SharedPV(nt=NTScalar(’d’), initial=0.0) # Channel 1 Rudder Output in Percentage
pv_battery_voltage = SharedPV(nt=NTScalar(’d’), initial=0.0) # Voltage
pv_battery_current = SharedPV(nt=NTScalar(’d’), initial=0.0) # Current
pv_temperature = SharedPV(nt=NTScalar(’d’), initial=0.0)
pv_torque = SharedPV(nt=NTScalar(’d’), initial=0.0)
pv_RPM = SharedPV(nt=NTScalar(’d’), initial=0.0)
pv_VendorID = SharedPV(nt=NTScalar(’d’), initial=0.0)
pv_MotorVoltage = SharedPV(nt=NTScalar(’d’), initial=0.0)

HOST = "localhost"
PORT = 5000

# PV Update Handlers
@pv_roll.put
@pv_pitch.put
@pv_yaw.put
@pv_groundspeed.put
#@pv_airspeed.put
@pv_armed.put
#@pv_state.put
#@pv_mode.put
#@pv_pwm_min.put
#@pv_pwm_max.put
#@pv_pwm_trim.put
#@pv_ch_ThrPwmOutput.put
@pv_ThrOutput.put
@pv_RudOutput.put
@pv_battery_voltage.put
@pv_battery_current.put
@pv_temperature.put
@pv_torque.put
@pv_RPM.put
@pv_VendorID.put
@pv_MotorVoltage.put
def handle(pv, op):
  pv.post(op.value()) # Store and update subscribers
  op.done()
def logger_client(conn,addr):
    print(f"Connection established with {addr}")
    with conn:
        buffer = ""
        while True:
              try:
                  data = conn.recv(1024)
                  if not data:
                          break
                  buffer += data.decode().strip() #Append data to buffer
                  print(buffer)
                  while "|" in buffer:
                        payload, buffer = buffer.split("|",1) #Split at |
                        try:
                            ID, val = payload.split(":",1) #Split ID and val
                            val = list(map(float,val.split(","))) #Map list
                            print(f"ID: {ID}, Value: {val}")
                        except ValueError:
                            print(f"Malformed Message: {payload}")
                        if ID == "pixhawk":
                                  print("Posting Pixhawk Data to Epics..")
                                  pv_roll.post(val[0])
                                  pv_pitch.post(val[1])
                                  pv_yaw.post(val[2])
                                  pv_groundspeed.post(val[3])
                                  pv_armed.post(val[4])
                                  pv_ThrOutput.post(val[5])
                                  pv_RudOutput.post(val[6])
                                  pv_battery_voltage.post(val[7])
                                  pv_battery_current.post(val[8])
                        elif ID == "gantner":
                                  print("Posting Gantner Data to Epics..")
                                  pv_temperature.post(val[0])
                                  pv_torque.post(val[1])
                                  pv_RPM.post(val[2])
                        elif ID == "faulhaber":
                                  print("Posting Faulhaber Data to Epics..")
                                  pv_VendorID.post(val[0])
                                  pv_MotorVoltage.post(val[1])
                        else:
                                  print(f"Unkown ID: {ID}")

               except Exception as e:
                      print(f"Error handling client {addr}:{e}")
                      break


if __name__ == ’__main__’:
    # Create EPICS Server and register PVs
    S = Server(providers=[{
                            ’pv:roll’: pv_roll,
                            ’pv:pitch’: pv_pitch,
                            ’pv:yaw’: pv_yaw,
                            ’pv:groundspeed’: pv_groundspeed,
                            #’pv:airspeed’: pv_airspeed,
                            ’pv:armed’: pv_armed,
                            #’pv:state’: pv_state,
                            #’pv:mode’: pv_mode,
                            #’pv:channel3minpwm’: pv_pwm_min,
                            #’pv:channel3maxpwm’: pv_pwm_max,
                            #’pv:channel3trimpwm’: pv_pwm_trim,
                            #’pv:channel3ThrottlePWMoutput’: pv_ch_ThrPwmOutput,
                            ’pv:Throttleoutput’: pv_ThrOutput,
                            ’pv:Rudderoutput’: pv_RudOutput,
                            ’pv:batteryvoltage’: pv_battery_voltage,
                            ’pv:batterycurrent’: pv_battery_current,
                            ’pv:Temperature’: pv_temperature,
                            ’pv:Torque’: pv_torque,
                            ’pv:RPM’: pv_RPM,
                            ’pv:VendorID’: pv_VendorID,
                            ’pv:MotorVoltage’: pv_MotorVoltage,
                            }])
print(S.conf())
print("EPICS Server Running...Process Variables Updating...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
      server.bind(("localhost", 5000)) # Define local socket server on the port 5000
      server.listen()
      print(f"Listening for connections on {HOST}:{PORT}...")
      while True:
            conn,addr = server.accept()
            client_thread = threading.Thread(target = logger_client, args=(conn,addr))
            client_thread.start()

from pymodbus.client import ModbusTcpClient
import time
import socket
import struct

ip = ’192.168.178.22’ # IP of Gantner DAQ

client = ModbusTcpClient(ip, port = 10000) #Port defined for ModbusTCP Server from GI Testbench

if client.connect():
    print("Connected to Gantner Systems Server")
  
def Gantner_logger():
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 5000)) # Connect to the local socket server on the port 5000
              while(1):
                      result_temp = client.read_holding_registers(address=1009, count=2)
                      raw_temp = result_temp.registers
                      #print("Raw Temp Value", raw_temp)
                      result_torque = client.read_holding_registers(address=1003, count=2)
                      raw_torque = result_torque.registers
                      #print("Raw Torque Value", raw_torque)
                      result_rpm = client.read_holding_registers(address=1005, count=2)
                      raw_rpm = result_rpm.registers
                      #print("Raw RPM Value", raw_rpm)
                      #Little Endian Order
                      #combined = (raw_temp[1] << 16) | raw_temp[0]
                      #temperatureL = struct.unpack(’<f’, struct.pack(’<I’,combined))[0]
                      #Big Endian order
                      combinedTemp = (raw_temp[0] << 16) | raw_temp[1]
                      temperatureB = struct.unpack(’>f’, struct.pack(’>I’,combinedTemp))[0]
                      combinedTorque = (raw_torque[0] << 16) | raw_torque[1]
                      torqueB = struct.unpack(’>f’, struct.pack(’>I’,combinedTorque))[0]
                      combinedRPM = (raw_rpm[0] << 16) | raw_rpm[1]
                      rpmB = struct.unpack(’>f’, struct.pack(’>I’,combinedRPM))[0]
                      #Swapped Endian order
                      #combined = (raw_temp[0] << 16) | raw_temp[1]
                      #temperatureS = struct.unpack(’<f’, struct.pack(’<I’,combined))[0]
                      message = f"gantner:{temperatureB},{torqueB},{rpmB}|"
                      s.sendall(message.encode())
                      print("Temperature in C ", temperatureB)
                      print("Torque in Nm", torqueB)
                      print("Speed in RPM", rpmB)
                      print()
                      time.sleep(1)
              client.close()
        
if __name__ == ’__main__’:
          Gantner_logger()

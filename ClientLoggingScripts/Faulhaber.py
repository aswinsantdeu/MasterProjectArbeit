"""
Faulhaber Object Dictionary: Important Indexes
0x6060--> Operation Mode
0x6040--> Control Word
0x6040--> Status Word
0x607A--> Target Position
0x60FF--> Target Velocity
0x6071--> Target Torque
0x6080--> Max Motor Speed
0x6081--> Profile Velocity
0x6083--> Acceleration
0x6084--> Deceleration
0x6085--> QuickStop Deceleration
0x2317--> Configuring PWM input
0x2340.02--> Motor Voltage Output DC (in multiples of 10mv)
Actual Position--> 0x6064
Actual Velocity--> 0x606C
Ambient Temperature--> 0x232A.08
Actual Torque--> 0x6077
Actual Current Value--> 0x6078
Baud Rate--> 0x2400.02
Actual Values-->0x2360
0x2329.01,02,03--> Motor Rated Current,Continous Current,Peak Current in mA
Important Command Codes
0x00
Function
Bootup
0x01 SDORead
0x02 SDOWrite
0x04 ControlWord
0x04 StatusWord
0x07 EMCY Message
Boot Up Command Sequence--> Faulhaber Drive Functions Pg 15
Steps Summary,
1_After Power up (Switch On Disabled state)
2_Give the Shutdown command : controlword = 0x0006 (Switch On Disabled state--> Ready to Switch on State)
3_Give Switch On command : controlword = 0x0007 (Ready to Switch on State--> Switch on state)
(Can be bypassed by directly giving Enable Operation cmd)
4_Give Enable Operation Cmd : controlword = 0x000F (Switch on state--> Operation Enabled State)
(Status light continuous Green, Output Stage enabled)
SOF NodeID EOF
Command Frame : [0x53 DataLen 0x01 CommandCode Data CRC 0x45]
<-----------Payload--------->
QuickUse Payload Example for the Command Frame (CommandFrame without SOF,EOF and CRC)
OperationEnable : 0x06,0x01,0x04,0x0F,0x00
OperationDisable : 0x06,0x01,0x04,0x07,0x00
Shutdown : 0x06,0x01,0x04,0x06,0x00
ReadStatusWord: 0x07,0x01,0x01,0x41,0x60,0x00
Read VendorID : 0x07,0x01,0x01,0x18,0x10,0x01
Soft Reset : 0x04,0x01,0x00
Read Motor Voltage : 0x07,0x01,0x01,0x40,0x23,0x02
"""


import serial
import time
import socket

# Configure the serial connection
ser = serial.Serial(
                    port=’/dev/ttyACM2’, # Replace with your port
                    baudrate=115200,
                    # Replace with the Faulhaber baud rate
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1    # Timeout in seconds
                    )
if ser.is_open:
      print("Connected to Faulhaber ESC")
  
POLYNOM = 0xD5       # Used for checksum calculation

  
# Function to calculate checksum for by Faulhaber
def calc_crc_byte(u8_byte, u8_crc):
        u8_crc ˆ= u8_byte
        for _ in range(8): # Process each bit
              if u8_crc & 0x01:
                  u8_crc = (u8_crc >> 1) ˆ POLYNOM
              else:
                  u8_crc >>= 1
        return u8_crc


#Checksum calculation for whole telegram (without SOF and EOF)
def calculate_checksum(data):
      checksum = 0xFF     # Initial CRC value
      for byte in data:
          checksum = calc_crc_byte(byte, checksum) # Update the CRC with each byte
      return checksum


# Function to send command and receive response
def send_command(frame):
      if not ser.is_open:
              ser.open()
      ser.write(bytearray(frame)) # Send the command frame as bytes
      time.sleep(1)
      ser.flush()
      # Read the response
      response = ser.read(ser.in_waiting or 1) # Read all available bytes
      return response


# Construct the CommandFrame according to Faulhaber protocol used for RS232/USB
def CommandFrame(sof,eof,data):
        checksum = calculate_checksum(data) # Calculate checksum
        frame = [sof] + data + [checksum] + [eof] # Full frame with checksum
        print("Sending frame:"," ".join(f"{byte:02X}" for byte in frame)) # To view in hex
        response = send_command(frame)
        print("Responded frame:"," ".join(f"{byte:02X}" for byte in response))
        return response


# Main execution
try:
    sof = 0x53 # Start of Frame
    eof = 0x45 # End of Frame
    data1 = [0x07,0x01,0x01,0x18,0x10,0x01] # Read for VendorID.
    data2 = [0x07,0x01,0x01,0x40,0x23,0x02] # Read Motor Voltage
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
          s.connect(("localhost", 5000)) # Connect to the local socket server on the port 5000
          while 1:
                  print("VendorID")
                  response1 = CommandFrame(sof,eof,data1)
                  response1Data = response1[7:11] #Extract VendorIdData from the frame
                  print("Responded data:"," ".join(f"{byte:02X}" for byte in response1Data))
                  VID = int.from_bytes(response1Data,byteorder=’little’, signed=False)       #Decode
                  print("VendorID:",VID)
                  print()
                  time.sleep(1)
                  print("MotorVoltage")
                  response2 = CommandFrame(sof,eof,data2)
                  response2Data = response2[7:9]                       #Extract VendorIdData from the frame
                  print("Responded data:"," ".join(f"{byte:02X}" for byte in response2Data))
                  MotorVolt = int.from_bytes(response2Data,byteorder=’little’, signed=False)    #Decode
                  print("MotorVoltage:",MotorVolt)
                  print()
                  message = f"faulhaber:{VID},{MotorVolt}|"
                  s.sendall(message.encode())
                  time.sleep(1)           # Wait 1 second before the next iteration
finally:
    ser.close()

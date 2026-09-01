# MasterProjectArbeit
Integrated Control, Data acquisition and Transmission for Autonomous Ships

The project focuses on achieving integrated control for an autonomous ship with real time data
acquisition and transmission back to the base station, with a system on chip (Raspberry Pi
5B) acting as a central hub in the ship. 
Features a Pixhawk 6X flight controller (from Holybro) used for autonomous vehicle navigation and collecting crucial vehicle-relevant data such as IMU, groundspeed, battery level, and so on.  
Data from Pixhawk (RC control) is fed to the Motor Controller (MC from Faulhaber) for the ship's motors. 
A Data Acquisition System (DAQ) (from Gantner Instruments) is integrated to collect sensor data from Torque/RPM sensors connected to the ship motors. Additional sensors can be integrated on the ship, whose data will flow via this DAQ.
The RPi communicates to the Pixhawk via Mavlink protocol to access or override(R/W) vehicle relevant parameters. The MC and RPi are separately communicating via USB serial communication
following CiA 301 and CiA 402 protocols (CAN in Automation) used by Faulhaber. Whereas the
DAQ and RPi are connected via Modbus protocol. 
In this project architecture, the RPi acts as the publisher connected with multiple subscribers. Individual communications with these subscribers ensures real time data collection. 
An EPICS base is hosted and running on the RPi to store the real-time collected data points as process variables in a synchronous way. 
These are then sent to a bucket on an InfluxDB server also running on the RPi through a telemetry radio network. An Influx client can be called from the base station to access these
process variables on the radio network and hence retrieve the data points sent from the ship.

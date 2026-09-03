import time, os
import influxdb_client
from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from p4p.client.thread import Context


current_time = int(time.time() * 1e9) # Current Timestamp

#Initialize InfluxDB
apitoken = "JRDO-wQtp9kOsMRVz7tGNorSW1fYNvpTPABx7Q_zJMjcPgpzTnuJ4ASapLXTBTSHw3T9j1t4FHtX8cjaDWW4_A=="
org = "DLR"
url = "http://localhost:8086"
database_client = influxdb_client.InfluxDBClient(url=url, token=apitoken, org=org)
write_api = database_client.write_api(write_options=SYNCHRONOUS)
bucket = "DLRVIS"


# Callback Handlers along with current timestamp to sync with InfluxDB Timestamp
def cb_roll(V):
    point = Point("roll").field("value", V.raw.value).tag("unit", "degrees").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
def cb_pitch(V):
    point = Point("pitch").field("value", V.raw.value).tag("unit", "degrees").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
def cb_yaw(V):
    point = Point("yaw").field("value", V.raw.value).tag("unit", "degrees").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
def cb_groundspeed(V):
    point = Point("groundspeed").field("value", V.raw.value).tag("unit", "m/s").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
#def cb_airspeed(V):
    #point = Point("airspeed").field("value", V.raw.value).tag("unit", "m/s").time(current_time, WritePrecision.NS)
    #write_api.write(bucket=bucket, org=org, record=point)
  
def cb_VehicleArmed(V):
    point = Point("VehicleArmed").field("value", V.raw.value).tag("unit", "bool").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
#def cb_VehicleState(V):
    #point = Point("VehicleState").field("value", V.raw.value).time(current_time, WritePrecision.NS)
    #write_api.write(bucket=bucket, org=org, record=point)

#def cb_VehicleMode(V):
    #point = Point("VehicleMode").field("value", V.raw.value).time(current_time, WritePrecision.NS)
    #write_api.write(bucket=bucket, org=org, record=point)

def cb_ThrottleOut(V):
    point = Point("ThrottleOutput").field("value", V.raw.value).tag("unit", "%").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
def cb_RudderOut(V):
    point = Point("RudderOutput").field("value", V.raw.value).tag("unit", "%").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
def cb_battery_voltage(V):
    point = Point("battery_voltage").field("value", V.raw.value).tag("unit", "V").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
def cb_battery_current(V):
    point = Point("battery_current").field("value", V.raw.value).tag("unit", "A").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
def cb_temperature(V):
    point = Point("Temperature").field("value", V.raw.value).tag("unit", " C ").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
def cb_torque(V):
    point = Point("Torque").field("value", V.raw.value).tag("unit", "Nm").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
def cb_MotorSpeed(V):
    point = Point("MotorSpeed").field("value", V.raw.value).tag("unit", "RPM").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
def cb_FaulhaberVendorID(V):
    point = Point("FaulhaberVendorID").field("value", V.raw.value).time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
def cb_MotorVoltage(V):
    point = Point("MotorVoltage").field("value", V.raw.value).tag("unit", "mV").time(current_time, WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
  
if __name__ == ’__main__’:
      ctxt = Context(’pva’)
      print("Starting Callbacks")
      ctxt.monitor(’pv:Temperature’, cb_temperature)
      ctxt.monitor(’pv:roll’, cb_roll)
      ctxt.monitor(’pv:pitch’, cb_pitch)
      ctxt.monitor(’pv:yaw’, cb_yaw)
      ctxt.monitor(’pv:groundspeed’, cb_groundspeed)
      #ctxt.monitor(’pv:airspeed’, cb_airspeed)
      ctxt.monitor(’pv:armed’, cb_VehicleArmed)
      #ctxt.monitor(’pv:state’, cb_VehicleState)
      #ctxt.monitor(’pv:mode’, cb_VehicleMode)
      ctxt.monitor(’pv:Throttleoutput’, cb_ThrottleOut)
      ctxt.monitor(’pv:Rudderoutput’, cb_RudderOut)
      ctxt.monitor(’pv:battery:voltage’, cb_battery_voltage)
      ctxt.monitor(’pv:battery:current’, cb_battery_current)
      #ctxt.monitor(’pv:Temperature’, cb_temperature)
      ctxt.monitor(’pv:Torque’, cb_torque)
      ctxt.monitor(’pv:RPM’, cb_MotorSpeed)
      ctxt.monitor(’pv:VendorID’, cb_FaulhaberVendorID)
      ctxt.monitor(’pv:MotorVoltage’, cb_MotorVoltage)
      print("Collecting data...")
      while True:
            pass

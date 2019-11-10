#!/usr/bin/env python
import greengrasssdk
import platform
from threading import Timer
import time
import bme680
import json
import datetime
import urllib3
import socket

def get_public_ip():
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://api.ipify.org')
    ip = r.data.decode('UTF-8')
    return ip

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

deviceId = ''
try:
    deviceId = get_public_ip()
    print(f'INFO: launching from public ip address: {deviceId}')
except:
    deviceId = get_local_ip()
    print(f'INFO: launching from local ip address: {deviceId}')
# else:
#     deviceId = 'Covington01'
#     print(f'INFO: unable to fetch public or local ip adress. setting deviceId to {deviceId}')

client = greengrasssdk.client('iot-data')
try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)
except Exception as e:
    sensor = None
    print(f'Error: couldnt initialize the bme680: {str(e)}')
    output = {
        "deviceId": deviceId,
        "dateTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "error": f'Error: couldnt initialize the bme680: {str(e)}'
    }
    client.publish(topic='sensor/bme680', payload=f'{json.dumps(output)}')

def makeDict(data):
    dataDict = {
        "temperature_C": float(f'{data.temperature:.2f}'),
        "pressure_hPa": float(f'{data.pressure:.2f}'),
        "humidity_RH": float(f'{data.humidity:.2f}'),
        "gas_resistance_Ohm": float(f'{data.gas_resistance:.2f}') or 0
    }

    return dataDict

## GreenGrass running stuff
def greengrass_run():
    output = {}
    if sensor is not None and sensor.get_sensor_data():
        output = makeDict(sensor.data)
    elif sensor is None:
        output["error"] = "Sensor is not initialized"
    output["deviceId"] = deviceId
    output["dateTime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(json.dumps(output))
    client.publish(topic='sensor/bme680', payload=f'{json.dumps(output)}')

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(5, greengrass_run).start()


# Execute the function above
greengrass_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return

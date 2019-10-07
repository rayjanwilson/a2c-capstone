

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import bme680
import json
import time
import boto3
import os
import datetime
import time
#import greengrasssdk

#client = greengrasssdk.client('iot-data')
# Load Env. variables
host = 'a36kfvedphfc5u-ats.iot.us-east-1.amazonaws.com'
client_id = 'iot-data'
topic = 'simulator/weather'
deviceId = 'Burlington01'

#certs
rootCAPath = '/greengrass/certs/root.ca.pem'
certificatePath = '/greengrass/certs/c615d5fb62.cert.pem'
privateKeyPath = '/greengrass/certs/c615d5fb62.private.key'

# Init AWSIoTMATTClient
myAWSIoTMQTTClient = None

# --- MQTT connection ---
myAWSIoTMQTTClient = AWSIoTMQTTClient(client_id)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
print('Connecting to AWS IoT...')
myAWSIoTMQTTClient.connect()
print('Successfully Connected!')

sensor = bme680.BME680()

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

while True:
	if sensor.get_sensor_data():
		new_shadow = "{0:.2f} C,{1:.2f} hPa,{1:.2f} %RH".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity)
		if sensor.data.heat_stable:
			new_shadow_gas = ("{0},{1} Ohms".format(new_shadow, sensor.data.gas_resistance))
			print(new_shadow_gas)
		else:	
			print(new_shadow)
		data = {}
		data['deviceId'] =  deviceId
		data['Time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
		data['Temperature'] = sensor.data.temperature
		data['Humidity'] = sensor.data.humidity
		data['Pressure'] = sensor.data.pressure
		myAWSIoTMQTTClient.publish(topic, json.dumps(data), 1)
		time.sleep(150)

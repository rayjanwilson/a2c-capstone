#!/usr/bin/env python
import greengrasssdk
import platform
from threading import Timer
import time
import bme680

client = greengrasssdk.client('iot-data')

sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

## GreenGrass running stuff
def greengrass_run():
    output = 'no data'
    if sensor.get_sensor_data():
        output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
            sensor.data.temperature,
            sensor.data.pressure,
            sensor.data.humidity)
        if sensor.data.heat_stable:
            output = '{0},{1:.2f} Ohms'.format(
                output,
                sensor.data.gas_resistance)
    print(output)
    client.publish(topic='hello/world', payload='{}'.format(output))

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(5, greengrass_run).start()


# Execute the function above
greengrass_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return

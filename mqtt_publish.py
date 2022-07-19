import time
import paho.mqtt.client as paho
import numpy as np
import threading

broker = '5g-vue.projects.uom.lk'
port = 1883
topic = "/group14a"
client_id = 'group14a'
username = 'iot_user'
password = 'iot@1234'

client = paho.Client(client_id)
client.username_pw_set(username, password)
client.connect(broker)
client.loop_start()

""""This is a Sensor class. Each Sensor object initilize with its properties"""
class Sensor:
    def __init__(self, sensor_topic, max_val=None, min_val=None, start=None, probability=None, period=10):
        self.topic =  topic + "/" + sensor_topic
        self.period = period
        self.max_val = max_val
        self.min_val = min_val
        self.val = start
        self.probability = probability  # only used in triggering sensors i.e. smoke and occupancy sensors

def CO2_thread_function(sensor):
    while True:
        rand_num = np.random.randint(-20, 20) # sensor value will be vary around the mean
        sensor.val = sensor.val + 0.2*rand_num
        sensor.val = max(sensor.min_val, min(sensor.max_val, sensor.val)) # keep within boundary conditions
        client.publish(sensor.topic, sensor.val)  # publish
        print("publishing ", sensor.topic,"\t\t\t", sensor.val)
        time.sleep(sensor.period)

def smoke_thread_function(sensor):
    while True:
        rand_num = np.random.uniform(0, 1)
        if (rand_num < sensor.probability): # if the uniform random value is less than given probability, publish the data
            client.publish(sensor.topic, 1)  # publish
            print("publishing ", sensor.topic,"\t\t\t", 1)
            time.sleep(sensor.period)   # after publishing the data, it wait 10 seconds. Because publishing interval for a sensor should not be less than 10 seconds(given in assignment)
        time.sleep(1) # check the probabilty in each second.

def pressure_thread_function(sensor):
    while True:
        rand_num = np.random.uniform(-1, 1) # sensor value will be vary around the mean
        sensor.val = sensor.val + 0.01*rand_num
        sensor.val = max(sensor.min_val, min(sensor.max_val, sensor.val))
        client.publish(sensor.topic, sensor.val)  # publish
        print("publishing ", sensor.topic,"\t\t", sensor.val)
        time.sleep(sensor.period)

def occupancy_thread_function(sensor):
    while True:
        rand_num = np.random.uniform(0, 1) 
        if (rand_num < sensor.probability): # if the uniform random value is less than given probability, publish the data
            client.publish(sensor.topic, 1)  # publish
            print("publishing ", sensor.topic,"\t\t", 1)
            time.sleep(sensor.period) # after publishing the data, it wait 10 seconds. Because publishing interval for a sensor should not be less than 10 seconds(given in assignment)
        time.sleep(1) # check the probabilty in each second.

def production_counting_thread_function(sensor):
    while True:
        rand_num = np.random.randint(-50, 50) # sensor value will be vary around the mean
        sensor.val = sensor.val + rand_num
        sensor.val = max(sensor.min_val, min(sensor.max_val, sensor.val))
        client.publish(sensor.topic, sensor.val)  # publish
        print("publishing ", sensor.topic,"\t\t", sensor.val)
        time.sleep(sensor.period)

def level_thread_function(sensor):
    while True:
        rand_num = np.random.uniform(-1, 0) # since the level is always decreasing, generate only negative values
        sensor.val = sensor.val + rand_num
        if sensor.val < sensor.min_val: # if the level is lower than the minimum level, we assume that tank will be filled automatically to its maximum
            sensor.val = sensor.max_val
        client.publish(sensor.topic, sensor.val)  # publish
        print("publishing ", sensor.topic,"\t\t\t", sensor.val)
        time.sleep(sensor.period)

def fuel_capacity_thread_function(sensor):
    while True:
        rand_num = np.random.uniform(-0.1, 0) # since the fuel level is always decreasing, generate only negative values
        sensor.val = sensor.val + rand_num
        if sensor.val < sensor.min_val: # if the fuel level is lower than the minimum level, we assume that fuel is pumped to tank automatically until its maximum
            sensor.val = sensor.max_val
        client.publish(sensor.topic, sensor.val)  # publish
        print("publishing ", sensor.topic,"\t\t", sensor.val)
        time.sleep(sensor.period)

CO2_01_sensor = Sensor("CO2_01", max_val=5000, min_val=400, start=450, period=15)                                   # CO2 density in the manufacturing environment in ppm.
CO2_02_sensor = Sensor("CO2_02", max_val=5000, min_val=400, start=1500, period=30)                                  # CO2 density in the exausting pipes in ppm.
smoke_01_sensor = Sensor("smoke_01", probability=0.02)                                                              # smoke detecting sensor --> Fire. probability of triggering 2%
pressure_01_sensor = Sensor("pressure_01", max_val=10, min_val=0, start=4, period=25)                               # pressure in the mixing area
pressure_02_sensor = Sensor("pressure_02", max_val=10, min_val=0, start=1.01325, period=20)                         # pressure in the manufacturing environment
occupancy_01_sensor = Sensor("occupancy_01", probability=0.03)                                                      # Indicate a presence of a person in the controlling room. probability of occurance 3%
production_counting_01_sensor = Sensor("counting_01", max_val=1000, min_val=0, start=500, period=60)                # Count the no. of bottles passing on the conveyor belt in a minute.
level_01_sensor = Sensor("level_01", max_val=6, min_val=1, start=5, period=30)                                      # Water level in the water tank.
level_02_sensor = Sensor("level_02", max_val=4, min_val=1, start=10, period=45)                                     # Beverage level in the beverage tank.
fuel_capacity_sensor = Sensor("fuel_capacity", max_val=2, min_val=0.1, start=1, period=60)                          # Generator Fuel Capacity.

if __name__ == "__main__":
    CO2_01_thread = threading.Thread(target=CO2_thread_function, args=(CO2_01_sensor,))
    CO2_02_thread = threading.Thread(target=CO2_thread_function, args=(CO2_02_sensor,))
    smoke_01_thread = threading.Thread(target=smoke_thread_function, args=(smoke_01_sensor,))
    pressure_01_thread = threading.Thread(target=pressure_thread_function, args=(pressure_01_sensor,))
    pressure_02_thread = threading.Thread(target=pressure_thread_function, args=(pressure_02_sensor,))
    occupancy_01_thread = threading.Thread(target=occupancy_thread_function, args=(occupancy_01_sensor,))
    production_counting_01_thread = threading.Thread(target=production_counting_thread_function, args=(production_counting_01_sensor,))
    level_01_thread = threading.Thread(target=level_thread_function, args=(level_01_sensor,))
    level_02_thread = threading.Thread(target=level_thread_function, args=(level_02_sensor,))
    fuel_capacity_thread = threading.Thread(target=fuel_capacity_thread_function, args=(fuel_capacity_sensor,))

    CO2_01_thread.start()
    CO2_02_thread.start()
    smoke_01_thread.start()
    pressure_01_thread.start()
    pressure_02_thread.start()
    occupancy_01_thread.start()
    production_counting_01_thread.start()
    level_01_thread.start()
    level_02_thread.start()
    fuel_capacity_thread.start()

import serial 
import time 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv

SERIAL_PORT = 'COM19'
BOUND_RATE = 115200


arduino = serial.Serial(SERIAL_PORT, BOUND_RATE, timeout=0.1) 
timeValue = []
temperature = []
pressure = []
humidity = []
voltage = []
shuntVoltage = []
current = []
power = []
powerConsum = []



def read_and_process_data():
    line = arduino.readline().decode('utf-8').strip()
    if line.strip() != "":
        print("Line: " + line)
        sensorValues = line.split(', ')
        temperature.append(float(sensorValues[0]))
        pressure.append(int(sensorValues[1]))
        humidity.append(int(sensorValues[2]))
        voltage.append(float(sensorValues[3]))
        shuntVoltage.append(float(sensorValues[4]))
        current.append(int(sensorValues[5]))
        power.append(float(sensorValues[6]))
        powerConsum.append(float(sensorValues[7]))
        timeValue.append(int(sensorValues[8]))


def update_plot(frame):
    read_and_process_data()
    plt.cla()
    plt.subplot(2,3,1)
    plt.plot(timeValue, temperature,'r', label='Temp')
    plt.subplot(2,3,2)
    plt.plot(timeValue, humidity,'b',  label='Humi')
    plt.subplot(2,3,3)
    plt.plot(timeValue, pressure,'k',  label='Pres')
    plt.subplot(2,3,4)
    plt.plot(timeValue, voltage,'g',  label='Voltage')
    plt.subplot(2,3,5)
    plt.plot(timeValue, current,'y',  label='Current')
    plt.subplot(2,3,6)
    plt.plot(timeValue, power,'m',  label='Power')
    plt.plot(timeValue, powerConsum,'b',  label='Power')


def on_close(event):
    with open('arduino_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for [t, temp, press, humi, volt, shunVolt, curr, powe, poweCons] in zip(
                timeValue, temperature, pressure, humidity, voltage, shuntVoltage, current, power, powerConsum):
            writer.writerow([t, temp, press, humi, volt, shunVolt, curr, powe, poweCons])
    
fig, ax = plt.subplots()
fig.canvas.mpl_connect('close_event', on_close)
ani = FuncAnimation(fig, update_plot, interval=10)
plt.show()
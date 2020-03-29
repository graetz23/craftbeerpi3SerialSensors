#
# craftbeerpi3SerialSensors
#
# Passive sensor that opens a serial console and sends sensor data ..
#
# Christian
# graetz23@gmail.com
# created 28032020
# version 29032020
#
# MIT License
#
# Copyright (c) 2020 craftbeerpi3SerialSensors Christian (graetz23@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import os, sys, threading, time, serial
from modules import cbpi, app
from modules.core.hardware import SensorPassive
from modules.core.props import Property

# for listing arduino's ttyACM0, ttyACM1, ..., in hardware settings
def getTTYACM():
    try:
        arr = []
        for portTTY in os.listdir('/dev'):
            if (portTTY.startswith("ttyACM")):
                arr.append(portTTY)
        return arr
    except:
        return [] # not found then list nothing

# for listing arduino's possible baud rates in hardware settings
def getBaudRate():
    arr = [9600,19200,38400,57600,115200]
    return arr

class myThread (threading.Thread):

    value = 0
    baud = 9600

    def __init__(self, sensor_name, sensor_baud):
        threading.Thread.__init__(self)
        self.sensor_name = sensor_name
        self.sensor_baud = sensor_baud
        myThread.port = "/dev/" + self.sensor_name
        myThread.baud = self.sensor_baud
        self.ser = serial.Serial(myThread.port, myThread.baud)
        self.ser.write(str("CBP3SerialSensor")) # for testing
        self.value = 0
        self.runnig = True

    def shutdown(self):
        if self.ser.isOpen():
            self.ser.close()
        pass

    def stop(self):
        if self.ser.isOpen():
            self.ser.close()
        self.runnig = False

    def run(self):

        while self.runnig:
            try:
                if not self.ser.isOpen():
                    self.ser = serial.Serial(myThread.port, myThread.baud)
                # below is working well
                seperator = " " # TODO make seperator selectable
                for idx, val in cbpi.cache["sensors"].iteritems():
                    sensorTemp = cbpi.cache.get("sensors")[idx].instance.last_value;
                    self.ser.write(str(sensorTemp))
                    self.ser.write(seperator)
                app.logger.info("SerialSensor sent data")
                # for an own value read the system temperature
                res = os.popen('vcgencmd measure_temp').readline()
                temp = float(res.replace("temp=","").replace("'C\n",""))
                self.value = temp
            except:
                pass

            time.sleep(4)

@cbpi.sensor
class SerialSensors(SensorPassive):
    sensor_name = Property.Select("arduino's /dev/ttyACM?", getTTYACM(), description="Possible devices where an arduino is connected; if empty, no arduino connected.")
    sensor_baud = Property.Select("arduino's baud rate", getBaudRate(), description="Select the baud rate defined in your arduino program.")

    def init(self):

        self.t = myThread(self.sensor_name, self.sensor_baud)

        def shutdown():
            shutdown.cb.shutdown()

        shutdown.cb = self.t
        self.t.start()

    def stop(self):
        try:
            self.t.stop()
        except:
            pass

    def read(self):
        if self.get_config_parameter("unit", "C") == "C":
            self.data_received(round(self.t.value, 2))
        else:
            self.data_received(round(9.0 / 5.0 * self.t.value + 32, 2))

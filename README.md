## CraftBeerPi3 SerialSensors Plugin

### Introduction
SerialSensors is a plugin for [CraftBeerPi3 (CBP3)](https://github.com/Manuel83/craftbeerpi3) that sends all sensor data via serial console; e.g. to an arduino.

![craftbeerpi3SerialSensor](craftbeerpi3SerialSensor.jpg)

### HowTo
Clone or download/unzip to your *craftbeerpi3/modules/plugins/* directory, restart: *sudo /etc/init.d/craftbeerpiboot restart*, and also reload on web application side.

Select **SerialSensors** as a *passive sensor*. It searches for */dev/ACMX* (X:={0,1,2,..,N-1} and let you select the *baud rate* and to which connected arduino to talk to.

Select if you want to have the system temperature as an extra value that is shown and send; if not, the sensor shows a _zero_, best you hide it then.

Select if you want to have a _start-up message_. This is good for having arduino recognizing a restart of the sensor - or not.

### Data
All sensor data is sent out as: "sensorValue1 sensorValue2 sensorValue3 sensorValueN", currently seperated by a whitespaces. For example: "55.1 63 72.2 78.3".

### Visualization
Connect an arduino via USB port to one of *craftBeerPi's* USB ports. Flash the [LiquidCrystal - Serial Input](https://www.arduino.cc/en/Tutorial/LiquidCrystalSerialDisplay) example, connecting some 20x2 LCD display to arduino; you can use a lot of wires or like mine an _i2c driver_; see photo.

### Processing
However you can process the sensor data for an own application using arduino and some electronics.

### Remarks
Everything was coded using:
  - [**atom**](https://atom.io/) editor,
  - [**python**](https://www.python.org/); v2.7,
  - [**Gnome**](https://www.gnome.org/) windows manager,
  - and [**debian**](https://www.debian.org/) GNU/Linux,

Tried out on / by:
  - [**arduino leonardo**](https://www.arduino.cc/),
  - [LiquidCrystal - Serial Input](https://www.arduino.cc/en/Tutorial/LiquidCrystalSerialDisplay),
  - [**raspberry pi 2B**](https://www.raspberrypi.org/),
  - [**CraftBeerPi3**](http://web.craftbeerpi.com/),
  - and [**raspbian**](https://www.raspberrypi.org/downloads/raspbian/) buster.

have fun.

## ChangeLog

The date string implies the version of the plugin

**29032020**
  - set up repository, added readme and photo,
  - added menu to select the baud rate the arduino runs on,
  - added menu to select if system's temperature should be shown and sent,
  - added menu to select if a start-up / recognizing message should be sent,
  - fixed bug on closing serial console while *stop* or *shutdown*.

**28032000**
  - added menu to detect and select the port of the serial console,
  - set up files and first test runs on openingn serial console to arduino,
  - crawled through CraftBeerPi3 to understand data structures.

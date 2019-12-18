## 1. How To Write Firmware（windows）
Step1：Install serial port driver
The download address of the CH340 serial port driver is: https://github.com/SmartArduino/DoHome/blob/master/DoHome_HomeKit_Moon_Light/Drive/ch341ser.7z

Step2：Installation of programming tools
Install programming tool：
http://espressif.com/en/support/download/other-tools

step3：Firmware download：
https://github.com/SmartArduino/DoHome/tree/master/DoHome_HomeKit_Temperature_Humidity_Sensor/Firmware

step4：After downloading the programming tool and firmware successfully, select ESP8266 as the chip type. The following address is used for firmware download.

|firmware          |download link                    |
|--------------|-----------------------------|
|homekit_serson_ac.bin| 0x0000                            |

Step5：Burn the relevant bin file After selecting the appropriate serial port, configure the serial port number, serial port baud rate, etc. as shown below, and press START to start downloading the program.

<img src="../README_IMAGE/3.png" width="400" />

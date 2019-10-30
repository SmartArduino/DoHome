English | <a href="./READMECN.md">中文版</a>

# Dohome upgrades to Homekit firmware

## 1.Introduction

&emsp;Why do we need to Upgrade the Dohome to Homekit?
When we talk about Upgrade the Dohome to Homekit,  actually we upgrade the Dohome light . Because the dohome firmware is based on the NONOS SDK development, while the homekit is based on the ESP-OPEN-RTOS SDK. The SDK of each of them is different.  And the BootLoader boot file is different too. So Dohome cannot be upgraded to Homekit directly. It needs to downloaded the intermediate temporary firmware to burns the boot of ESP-OPEN-RTOS to run the homekit firmware.

## 2.software and tools that needed

### 2.1 Software

upgrade tools:

&emsp;&emsp;Download: http://support.doiting.com/DoHome.zip

&emsp;&emsp;Download DoHome_JRE_32.zip intermediate temporary firmware if your computer is a 32-bit system and DoHome_JRE_64.zip intermediate temporary firmware for a 64-bit system.

Intermediate temporary firmware:

&emsp;&emsp;Download: http://support.doiting.com/DoHome.zip

### 2.22 Hardware
&emsp;&emsp;Dohome light strip controller

## 3.Upgrade steps

### 3.1 Connecting Dohome_xxxx Hotspots

&emsp;&emsp;Power on the light strip controller, connect the hot spot Dohome_xxxx (xxxx is id),password: 12345678. Connect successfully, then move to next step.

![图片](./doc/tu2.png)

Note: If the light strip controller has been configured with wifi, power on and off for three times continuously, the hot spot will be reset.

### 3.2 Upgrade to temporary firmware

&emsp;&emsp;Open the upgrade tool `DoHome_v212.exe` on the computer to enter the DoHome upgrade interface, fill `mid_u1.bin` temporary firmware in u1 path, `mid_u2.bin` temporary firmware in u2 path;  fill in Device IP: `192.168.4.1`

![图片](./doc/tu1.png)

(the rest do not needed to fill in).Click Start upgrading to start the upgrade.

### 3.3 Upgraded
&emsp;&emsp;Wait for the progress bar to go to 100%, indicating that the upgrade is complete; the module will restart and create a hotspot: `dohome_updata_XXXXXXXXXXXX`

![图片](./doc/tu3.png)

 connect this hotspot,Use your browser to visit: `http://192.168.4.1`
and enter your home wifi name and password.

![图片](./doc/tu4.png)

The browser will download the latest homekit lights firmware and boot after the light strip controller is connected to this hotspot

During this process, the light will switch between power-off and flashing(i.e. power-off-flash- power-off-flash……）.Wait until the light strip turns’ red-green-blue-white’( the color) and then keep white. Then upgrade is completed. The hot `Homekit_xxxx` will pop up

![图片](./doc/tu5.png)

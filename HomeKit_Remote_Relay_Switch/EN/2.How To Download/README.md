## Download the firmware instructions using the downloader
step1：Remove the distribution network module on the remote relay, plug in the downloader, and connect to your computer using the usb data cable.
Download link for downloader： 
https://item.taobao.com/item.htm?spm=a1z10.5-c.w4002-1811579842.51.3e8c4a9duXJDv0&id=581769095945

step2：After connecting with the PC, click the link below to download the relevant firmware.。

bootloader_bin：https://github.com/SmartArduino/DoHome/tree/master/DoHome_HomeKit_Firmware/bootloader application_bin：https://github.com/SmartArduino/DoHome/tree/master/DoHome_HomeKit_Firmware/plug_01

step3:After the firmware download is successful, click the link below to download the firmware download tool. Firmware download tool address：https://www.espressif.com/sites/default/files/tools/flash_download_tools_v3.6.7.zip

Step4：Check the firmware you want to download on the download tool. The address is as follows:。

|firmware             | download link      |
| ----------------- | -------------| 
| rboot.bin         | 0x0000       | 
| blank_config.bin  | 0x1000       | 
| homekit_plug_01relays.bin            | 0x2000       | 

Step5：Select the serial port that the downloader connects to your PC, click to download

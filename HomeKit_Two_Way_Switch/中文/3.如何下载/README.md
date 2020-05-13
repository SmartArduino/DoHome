## 使用下载器下载固件说明

step1：将二路继电器上的配网模组取下，插上下载器后，使用usb数据线与你的计算机连接。
下载器的购买链接：

https://item.taobao.com/item.htm?spm=a1z10.5-c.w4002-1811579842.25.23cc4e786tXfZl&id=602394770230

step2点击击如下链接地址下载两路继电器固件：

支持Homekit、HA的固件：
https://github.com/SmartArduino/DoHome/blob/master/HomeKit_Four_Way_Switch/Firmware/homekit_ha_two_way_relay_v1.1.0.bin

带有点动设置新版固件：
https://github.com/SmartArduino/DoHome/blob/master/HomeKit_Two_Way_Switch/Firmware/multiple_sensors_relay2jog.bin

step3：点击如下链接下载固件下载工具。

固件下载工具地址：https://www.espressif.com/sites/default/files/tools/flash_download_tools_v3.6.7.zip

下载工具下载完成后，芯片类型选择8266，选择合适的串口点击START按钮开始下载

  <img src="../README_IMAGE/9.png" width="400" />


Step4在下载工具上勾选需要下载的固件，其中的地址填写如下表。

| 固件              | 下载地址      |
| ----------------- | -------------| 
| multiple_relay2.bin            | 0x0000       | 


Step5选择好下载器与你pc机连接的串口，点击下载

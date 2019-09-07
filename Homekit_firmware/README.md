# 固件下载说明
## 1.下载工具：
[flash_download_tools_v3.6.7.zip](https://www.espressif.com/sites/default/files/tools/flash_download_tools_v3.6.7.zip "flash_download_tools_v3.6.7.zip")

## 2.下载软件设置
固件使用1MB(8mbit) flash,512k+512k布局

| 固件              | 下载地址      |
| ----------------- | -------------| 
| rboot.bin         | 0x0000       | 
| blank_config.bin  | 0x1000       | 
| u1.bin            | 0x2000       | 
| u2.bin            | 0x81000      | 

注：u1与u2仅需下载其中一个，地址不能互换

SPIFlash config:
```
SPI SPEED: 40MHZ
SPI MODE:  DOUT
FLASH SIZE: 8Mbit
```
![markdown](https://github.com/SmartArduino/DoHome/blob/master/Homekit_firmware/doc/20190907134747.png "config")

## 3.硬件接线

下载时需要GPIO0 拉低，然后RST拉低一下，模块复位后检测到GPIO0处于低电平，模块进入下载模式

最小系统：
![markdown](https://github.com/SmartArduino/DoHome/blob/master/Homekit_firmware/doc/esp-m%E6%A8%A1%E5%9D%97%E6%9C%80%E5%B0%8F%E7%B3%BB%E7%BB%9F.png "config")

## 4.设备管脚对应表
### （1）美规/欧规插座

| 功能         | GPIO        |
| ------------ | ------------| 
| 按键         | GPIO4       | 
| 继电器       | GPIO12      | 
| 指示灯       | GPIO5       | 

### （2）中国国标插座

| 功能         | GPIO        |
| ------------ | ------------| 
| 按键         | GPIO13      | 
| 继电器       | GPIO14      | 
| 指示灯       | GPIO12      | 

### （3）球泡灯

| 功能         | GPIO         |
| ------------ | -------------| 
| 红色（r）    | GPIO12       | 
| 绿色（g）    | GPIO14       | 
| 蓝色（b）    | GPIO5        | 
| 白色（w）    | GPIO4        | 

### （4）灯带控制器

| 功能         | GPIO         |
| ------------ | -------------| 
| 红色（r）    | GPIO15       | 
| 绿色（g）    | GPIO13       | 
| 蓝色（b）    | GPIO4        | 
| 白色（w）    | GPIO5        | 

## 4.固件测试
下载完成后，模块串口硬件输出log信息，波特率74880，模块正常输出log，不重启为正常
```
ESP-Open-SDK ver: 0.0.1 compiled @ Sep  4 2019 11:06:33
phy ver: 273, pp ver: 8.3


|======================================
|Firmware version: 1.2.3
|Copyright: DOIT Sep  6 2019 14:04:33
|Chip type: HOMEKIT
|======================================
!!!!!!!!!!!
This firmware is for dev-board
!!!!!!!!!!!
!!!!!!!!!!!
This is DEBUG firmware, has output info
!!!!!!!!!!!
This device is IS_STRIP_NO_IR
curr slot 0
reset reason: 0
flash init
>>>>>
router_ssid hex: 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
PARA_SECETOR=7c, SSID_INFO_SECTOR=7d
saved SSID: , passwd: 
<<<<<
reset_count=0
>>> write reset count 1
```
## 5.技术支持

技术支持QQ群：637971101
邮箱：song@doit.am



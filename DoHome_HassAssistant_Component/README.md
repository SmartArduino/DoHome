# DoHome_HomeAssistant_Components
[English Version](./README_EN.md)  

将DoHome设备接入HomeAssistant的插件

* 局域网自动发现
* 支持设备：单孔插座、RGB彩灯、温湿度、人体检测、温湿度+光照+人体+继电器、两路继电器、四路继电器

<img src="./image/index.png" height="400"> 


## 插座、联络继电器、四路继电器
* 支持局域网控制和设备状态反馈    
<img src="./image/switch_control.png" height="150"> 

## 彩色灯
* 支持全彩RGB和的亮度调节    
<img src="./image/light_control.png" height="300"> 

## 传感器
* 支持温湿度、光照、人气检测    
<img src="./image/sensor.png" height="80"> 

## 使用说明
### 1 添加插件
将custom_components目录文件放到HomeAssistant的配置目录/config/custom_components

### 2 修改配置文件
编辑HomeAssistant配置文件configuration.yaml，添加以下代码
```
dohome:
  discovery_ip: '192.168.9.255'    #用于发现设备的广播IP，该参数可省略
  discovery_retry: 3                    #内网发现尝试次数，该参数可省略
```
#### 配置说明
1. 若你再Linux或Windows下使用Python安装HomeAssistant，可省去discovery_ip参数。甚至可以直接添加`dohome:`即可
2. 若你使用Docker构建HomeAssistant，在使用此插件需要添加discovery_ip参数，IP为连接的路由网关IP的广播IP，及当你的本地IP为192.168.9.17时，只需将最后一位改为255，即`discovery_ip: '192.168.9.255'`
3. 内网发现是插件加载时进行扫描的，可认为HA在启动的扫描，扫描时间为discovery_retry*5秒，长时间的扫描将影响HA的启动，默认次数为2次

## 注意
* Docker构建HomeAssistant需要映射6091端口，使用UDP协议


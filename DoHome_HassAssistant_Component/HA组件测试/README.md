# 1.准备
1. 解压调试工具TCPUDPDbg
2. 关闭手机DoHome APP，最好直接断开WIFI，防止影响测试
# 2.测试设备是否支持局域网发现
1. 创建链接    
    ->广播     
    ->目标IP：225.255.255.255   端口：6091    
    ->本机端口 指定:6091    
2. 点击右边的 广播包发送选项 -> 直接OK
3. 点击连接标签页上的连接
4. 在发送区输入```cmd=ping```
5. 点击发送
### 说明    
* 接收区有2条以上数据(序号0为本机发包数据)，则表明当前局域网有支持局域网发现的设备
* 点击查看数据，重点查看设备类型device_type
* 支持设备：_DT-PLUG、_DT-WYRGB、_REALY2、_REALY4、_STRIPE、_THIMR、_MOTION
* 没有广播消息请更新固件：https://github.com/SmartArduino/DoHome
# 3.HomeAssistant组件局域网发现测试
1. 配置好组件
2. 使用刚才的TCPUDPDbg，清空接收区
3. 重启Hass
### 说明    
* 若接收区有端口不为6091的数据，数据为```cmd=ping```，则表明HA组件配置没问题
* 按道理调试工具也可以接受到DoHome设备回复HA组件的消息
* HA启动20秒后，没有广播信息请检查IP配置，或端口问题（docker需要映射6091/udp）


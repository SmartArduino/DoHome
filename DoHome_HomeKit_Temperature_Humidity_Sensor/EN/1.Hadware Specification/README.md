## 1.Product appearance

<img src="../README_IMAGE/1.png" width="400" />

<img src="../README_IMAGE/2.png" width="400" />

## 2. Parameter description

|parameter                   |Numerical value                                         |
|-----------------------|-------------------------------------------|
|product name：               | HomeKit_DoHome Temperature and Humidity Collector                 |
|Size：                  |L40mm*W40mm*H18mm                      |
|Temperature measurement range：           |-40℃-80℃                                   |
|Temperature measurement accuracy：           |+-0.5℃                                      |
|Humidity measurement range：           |0-99.9%                                     |
|Humidity measurement accuracy：           |+-%3RH                                      |
|Temperature resolution：             |0.1%℃                                      |
|Humidity resolution：             |0.1%RH                                      |
|Power consumption：                  |350uA                                       |
|Supply voltage：              |3.1-5.5V                                     |

## 3. Interface Description


 <img src="../README_IMAGE/11.png" width="200" />         <img src="../README_IMAGE/13.png" width="200" />
 
The MCU uses the GPIO-5 pin as the data transmission pin with the temperature and humidity sensor. The specific pin wiring is as follows：

 <img src="../README_IMAGE/12.png" width="350" /> 
 
|PIN                   |NAME                     |PROGRAM                  |
|-----------------------|-------------------------|---------------------|
|1                       |VDD                         |power 3.1-5.5V                    |
|2                       |SDA                         |Serial data bi-directional port                  |
|3                       |GND                         |Ground                    |
|4                       |SCL                         |Serial data input (grounded for single bus)                    |

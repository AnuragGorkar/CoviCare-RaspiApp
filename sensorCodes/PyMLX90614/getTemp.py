from smbus2 import SMBus
from mlx90614 import MLX90614


bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
ambientTemp = 0
objectTemp = 0
for i in range(5):
    try:
        ambientTemp = ambientTemp + sensor.get_ambient()
        objectTemp = objectTemp + sensor.get_object_1()
    except:
        print(0.0)
bus.close()
print(round(objectTemp/5, 2))
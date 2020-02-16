'''
        Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
	http://www.electronicwings.com
'''
import smbus			#import SMBus module of I2C
from time import sleep          #import

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

class acc:
        def __init__(gyro):
                gyro.bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
                gyro.Device_Address = 0x68   # MPU6050 device address
                gyro.MPU_Init()
        def MPU_Init(gyro):
                #write to sample rate register
                gyro.bus.write_byte_data(gyro.Device_Address, SMPLRT_DIV, 7)
                
                #Write to power management register
                gyro.bus.write_byte_data(gyro.Device_Address, PWR_MGMT_1, 1)
                
                #Write to Configuration register
                gyro.bus.write_byte_data(gyro.Device_Address, CONFIG, 0)
                
                #Write to Gyro configuration register
                gyro.bus.write_byte_data(gyro.Device_Address, GYRO_CONFIG, 24)
                
                #Write to interrupt enable register
                gyro.bus.write_byte_data(gyro.Device_Address, INT_ENABLE, 1)

        def read_raw_data(gyro,addr):
                #Accelero and Gyro value are 16-bit
                high = gyro.bus.read_byte_data(gyro.Device_Address, addr)
                low = gyro.bus.read_byte_data(gyro.Device_Address, addr+1)
            
                #concatenate higher and lower value
                value = ((high << 8) | low)
                
                #to get signed value from mpu6050
                if(value > 32768):
                        value = value - 65536
                return value






import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import smbus
import time

# Define some device parameters
I2C_ADDR = 0x27  # I2C address of the LCD
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

LCD_BACKLIGHT = 0x08  # On
# LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Open I2C interface
# bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1


class LCD_I2C_16X2(Node):
    
    def __init__(self):
        super().__init__('lcd_i2c_16x2')
        self.get_logger().info('LCD_I2C_16X2 Node has been started.')
        self.subscription = self.create_subscription(
            String,
            'lcd_print',  
            self.listener_callback,
            10)
        self.lcd_init()
    
    def listener_callback(self, msg):
        try:
            numLine, message = msg.data.split("::")
            if(numLine == "1"):
                self.lcd_string(message, LCD_LINE_1)   
                self.get_logger().info("print : "+ message + "on the line : " + numLine)
                
            elif (numLine == "2"):
                self.lcd_string(message, LCD_LINE_2)   
                self.get_logger().info("print : "+ message + "on the line : " + numLine)
                
            else: 
                self.get_logger().info("\"" + msg.data + " \"Can not be printing")
        except Exception as e:
            self.get_logger().info(f"An error occured: {e}")
    
    def lcd_init(self):
        self.lcd_byte(0x33, LCD_CMD)  # 110011 Initialize
        self.lcd_byte(0x32, LCD_CMD)  # 110010 Initialize
        self.lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
        time.sleep(E_DELAY)

    def lcd_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

        # High bits
        bus.write_byte(I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)

        # Low bits
        bus.write_byte(I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        time.sleep(E_DELAY)
        bus.write_byte(I2C_ADDR, (bits | ENABLE))
        time.sleep(E_PULSE)
        bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
        time.sleep(E_DELAY)

    def lcd_string(self, message, line):
        message = message.ljust(LCD_WIDTH, " ")
        self.lcd_byte(line, LCD_CMD)
        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)


def main():
    rclpy.init()
    node = LCD_I2C_16X2()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()

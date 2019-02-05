# //*****************************************************************************
# * | File        :	  epd5in83.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * |	This version:   V3.0
# * | Date        :   2018-11-06
# * | Info        :   python2 demo
# * 1.Remove:
#   digital_write(self, pin, value)
#   digital_read(self, pin)
#   delay_ms(self, delaytime)
#   set_lut(self, lut)
#   self.lut = self.lut_full_update
# * 2.Change:
#   display_frame -> TurnOnDisplay
#   set_memory_area -> SetWindow
#   set_memory_pointer -> SetCursor
#   get_frame_buffer -> getbuffer
#   set_frame_memory -> display
# * 3.How to use
#   epd = epd2in7.EPD()
#   epd.init(epd.lut_full_update)
#   image = Image.new('1', (epd5in83.EPD_WIDTH, epd5in83.EPD_HEIGHT), 255)
#   ...
#   drawing ......
#   ...
#   epd.display(getbuffer(image))
# ******************************************************************************//
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and//or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


import epdconfig
from PIL import Image
import RPi.GPIO as GPIO
import time

# Display resolution
EPD_WIDTH       = 600
EPD_HEIGHT      = 448

# EPD7IN5 commands
PANEL_SETTING                               = 0x00
POWER_SETTING                               = 0x01
POWER_OFF                                   = 0x02
POWER_OFF_SEQUENCE_SETTING                  = 0x03
POWER_ON                                    = 0x04
POWER_ON_MEASURE                            = 0x05
BOOSTER_SOFT_START                          = 0x06
DEEP_SLEEP                                  = 0x07
DATA_START_TRANSMISSION_1                   = 0x10
DATA_STOP                                   = 0x11
DISPLAY_REFRESH                             = 0x12
IMAGE_PROCESS                               = 0x13
LUT_FOR_VCOM                                = 0x20
LUT_BLUE                                    = 0x21
LUT_WHITE                                   = 0x22
LUT_GRAY_1                                  = 0x23
LUT_GRAY_2                                  = 0x24
LUT_RED_0                                   = 0x25
LUT_RED_1                                   = 0x26
LUT_RED_2                                   = 0x27
LUT_RED_3                                   = 0x28
LUT_XON                                     = 0x29
PLL_CONTROL                                 = 0x30
TEMPERATURE_SENSOR_COMMAND                  = 0x40
TEMPERATURE_CALIBRATION                     = 0x41
TEMPERATURE_SENSOR_WRITE                    = 0x42
TEMPERATURE_SENSOR_READ                     = 0x43
VCOM_AND_DATA_INTERVAL_SETTING              = 0x50
LOW_POWER_DETECTION                         = 0x51
TCON_SETTING                                = 0x60
TCON_RESOLUTION                             = 0x61
SPI_FLASH_CONTROL                           = 0x65
REVISION                                    = 0x70
GET_STATUS                                  = 0x71
AUTO_MEASUREMENT_VCOM                       = 0x80
READ_VCOM_VALUE                             = 0x81
VCM_DC_SETTING                              = 0x82

class EPD:
    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
    
    # Hardware reset
    def reset(self):
        epdconfig.digital_write(self.reset_pin, GPIO.HIGH)
        epdconfig.delay_ms(200) 
        epdconfig.digital_write(self.reset_pin, GPIO.LOW)         # module reset
        epdconfig.delay_ms(200)
        epdconfig.digital_write(self.reset_pin, GPIO.HIGH)
        epdconfig.delay_ms(200)   

    def send_command(self, command):
        epdconfig.digital_write(self.dc_pin, GPIO.LOW)
        epdconfig.spi_writebyte([command])

    def send_data(self, data):
        epdconfig.digital_write(self.dc_pin, GPIO.HIGH)
        epdconfig.spi_writebyte([data])
        
    def wait_until_idle(self):
        print("e-Paper busy")
        while(epdconfig.digital_read(self.busy_pin) == 0):      # 0: idle, 1: busy
            epdconfig.delay_ms(100)    
        print("e-Paper busy release")
        
    def init(self):
        if (epdconfig.module_init() != 0):
            return -1
        # EPD hardware init start
        self.reset()
        
        self.send_command(POWER_SETTING)
        self.send_data(0x37)
        self.send_data(0x00)
        self.send_command(PANEL_SETTING)
        self.send_data(0xEF)
        self.send_data(0x08)
        self.send_command(BOOSTER_SOFT_START)
        self.send_data(0xc7)
        self.send_data(0xcc)
        self.send_data(0x28)
        self.send_command(POWER_ON)
        self.wait_until_idle()
        self.send_command(PLL_CONTROL)
        self.send_data(0x19)                                    # 143Hz
        self.send_command(TEMPERATURE_CALIBRATION)
        self.send_data(0x00)
        self.send_command(VCOM_AND_DATA_INTERVAL_SETTING)
        self.send_data(0x77)
        self.send_command(TCON_SETTING)
        self.send_data(0x22)
        self.send_command(SPI_FLASH_CONTROL)
        self.send_data(0x00)
        self.send_command(TCON_RESOLUTION)
        self.send_data(0x02)     #source 600
        self.send_data(0x58)
        self.send_data(0x01)     #gate 448
        self.send_data(0xC0)
        self.send_command(VCM_DC_SETTING)
        self.send_data(0x28)      #decide by LUT file change 1e
        self.send_command(0xe5)
        self.send_data(0x03)
        
        # EPD hardware init end
        return 0

    def getbuffer(self, image):
        start_time = time.time()
        imwidth, imheight = image.size
        pixels = image.load()
        print("imwidth = ", imwidth, "imheight = ", imheight)
        array = [0x33] * 134400                                 # Setting All White
        for y in range(imheight):
            for x in range(imwidth):
                if pixels[x, y] < 64:                           # Black
                    n_pixels = y * self.width + x
                    if n_pixels % 2 == 1:
                        array[n_pixels//2] &= 0xF0
                    else:
                        array[n_pixels//2] &= 0x0F

        print("%s" %(time.time() - start_time))

        return array


    def display(self, array):
        start_time = time.time()
        self.send_command(DATA_START_TRANSMISSION_1)

        for i in range(0, 134400):
            self.send_data(array[i])

        print("%s" % (time.time() - start_time))
        self.send_command(DISPLAY_REFRESH)
        epdconfig.delay_ms(100)
        self.wait_until_idle()

    def Clear(self):
        start_time = time.time()
        self.send_command(DATA_START_TRANSMISSION_1)
        for i in range(0, 134400):
            self.send_data(0x33)
        print("%s" % (time.time() - start_time))
        self.send_command(DISPLAY_REFRESH)
        self.wait_until_idle()


    def sleep(self):
        self.send_command(POWER_OFF)
        self.wait_until_idle()
        self.send_command(DEEP_SLEEP)
        self.send_data(0XA5)
### END OF FILE ###


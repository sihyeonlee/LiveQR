#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd5in83
import time
import qrcode
from PIL import Image,ImageDraw,ImageFont
import traceback
import keypad

font_dir = '/usr/share/fonts/truetype/nanum'

qr_code = qrcode.QRCode(version=3,
                        error_correction=qrcode.constants.ERROR_CORRECT_H,
                        box_size=5,
                        border=0)

try:
    panel = epd5in83.EPD()
    panel.init()
    panel.Clear()
    Image_Palette = Image.new('1', (epd5in83.EPD_WIDTH, epd5in83.EPD_HEIGHT), 255)

    Image_Palette = Image.open('background.bmp')
    Image_Palette = Image_Palette.convert('1')
    panel.display(panel.getbuffer(Image_Palette))

    print("Plz Input Value")
    value = keypad.activation()

    qr_code.add_data(value)
    qr_code.make()

    img_qr = qr_code.make_image()
    img_qr.save("qr.bmp")

    bmp = Image.open('qr.bmp')

    bmp = Image.open('qr.bmp')
    Image_Palette.paste(bmp, (77,147))
    Image_Palette.save("check.bmp")
    panel.display(panel.getbuffer(Image_Palette))

    panel.sleep()


except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()
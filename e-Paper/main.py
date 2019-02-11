#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd5in83
import time
import qrcode
from PIL import Image,ImageDraw,ImageFont
import traceback
import keypad
import web


font_dir = '/usr/share/fonts/truetype/nanum/'
dir = '/home/pi/liveqr/'

qr_code = qrcode.QRCode(version=2,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=5,
                        border=0)

try:
    panel = epd5in83.EPD()
    panel.init()
    panel.Clear()
    Image_Palette = Image.new('1', (epd5in83.EPD_WIDTH, epd5in83.EPD_HEIGHT), 255)
    font48 = ImageFont.truetype(font_dir + 'NanumGothic.ttf', 48)
    Image_Palette = Image.open(dir + 'background.bmp')
    Image_Palette = Image_Palette.convert('1')
    draw = ImageDraw.Draw(Image_Palette)
    draw.text((10,10), u'가격 입력', font=font48, fill=0)
    panel.display(panel.getbuffer(Image_Palette))

    print("Plz Input Value")
    value = keypad.activation()
    out_text = '가격 : ' + str(value) + '원'
    url = web.call_api(int(value))


    qr_code.add_data(url)
    qr_code.make()

    img_qr = qr_code.make_image()
    img_qr.save(dir + "qr.bmp")

    Image_Palette_2 = Image.new('1', (epd5in83.EPD_WIDTH, epd5in83.EPD_HEIGHT), 255)
    Image_Palette_2 = Image.open(dir + 'background.bmp')
    Image_Palette_2 = Image_Palette_2.convert('1')
    bmp = Image.open(dir + 'qr.bmp')
    Image_Palette_2.paste(bmp, (85,132))
    draw = ImageDraw.Draw(Image_Palette_2)
    draw.text((290, 199), out_text, font=font48, fill=0)
    Image_Palette_2.save(dir + "check.bmp")
    panel.display(panel.getbuffer(Image_Palette_2))

    panel.sleep()


except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()
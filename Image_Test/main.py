import qrcode
from PIL import Image,ImageDraw,ImageFont

qr_code = qrcode.QRCode(version=3,
                        error_correction=qrcode.constants.ERROR_CORRECT_M,
                        box_size=5,
                        border=0)

Image_Palette = Image.open('background.bmp')
Image_Palette = Image_Palette.convert('1')
print(Image_Palette.mode)

print("Plz Input Value")
value = int(input())

qr_code.add_data(value)
qr_code.make()

img_qr = qr_code.make_image()
img_qr.save("qr.bmp")

bmp = Image.open('qr.bmp')
print(bmp)

Image_Palette.paste(bmp, (77, 147))
Image_Palette.save("check.bmp")
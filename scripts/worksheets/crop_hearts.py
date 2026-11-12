from PIL import Image

im = Image.open('c:/2026AI_Agent/教學駕駛艙/kristy_image3.png')

# Left heart is around x: 70..160, y: 380..460
im.crop((60, 360, 170, 470)).save('c:/2026AI_Agent/教學駕駛艙/crop_left_heart.png')

# Top-right heart is around x: 530..640, y: 110..210
im.crop((530, 110, 640, 210)).save('c:/2026AI_Agent/教學駕駛艙/crop_tr_heart.png')

# Bottom-right heart is around x: 650..750, y: 410..500
im.crop((650, 410, 750, 500)).save('c:/2026AI_Agent/教學駕駛艙/crop_br_heart.png')

print("Cropped candidate regions")

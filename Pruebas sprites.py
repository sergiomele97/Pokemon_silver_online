from PIL import Image
img = Image.open('sprite1.png', 'r')
img_w, img_h = img.size
background = Image.new('RGBA', (1440, 900), (255, 255, 255, 255))
bg_w, bg_h = background.size
offset = ((bg_w - img_w) // 1, (bg_h - img_h) // 1)
background.paste(img, offset)
background.save('out.png')
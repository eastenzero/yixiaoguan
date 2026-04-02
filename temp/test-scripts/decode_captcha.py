import base64

with open('captcha_base64.txt', 'r') as f:
    img_data = f.read().strip().strip('"')

# Remove data URL prefix if present
if 'base64,' in img_data:
    img_data = img_data.split('base64,')[1]

with open('captcha.jpg', 'wb') as f:
    f.write(base64.b64decode(img_data))

print('Captcha saved to captcha.jpg')

# Try to display info about the image
try:
    from PIL import Image
    img = Image.open('captcha.jpg')
    print(f'Image size: {img.size}')
    print(f'Image mode: {img.mode}')
except ImportError:
    print('PIL not available, image saved but not analyzed')

from PIL import Image
from PIL.ExifTags import TAGS

data = {}
photo = Image.open(r"D:\Images\shutterstock\LNP_Snow_Penyfan_RME_014.JPG")
info = photo.getexif()
for tag, value in info.items():
    decoded = TAGS.get(tag, tag)
    data[decoded] = value

print(data)

ImageDescription = data['ImageDescription']
Make = data['Make']

print(ImageDescription)
print()




# TODO started testing Markdown in HTM /.....blog_detail
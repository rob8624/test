import pyexiv2

img = pyexiv2.Image(r"D:\Images\FOR LNP\RM_121219_SwanseaBus_005.jpg")
data = img.read_exif()
print(data)
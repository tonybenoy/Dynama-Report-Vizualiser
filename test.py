import cv2
import pytesseract
import PIL as pl

image = pl.Image.open("/home/tony/Desktop/Dynama-Report-Vizualiser/8/0_8.pdf.jpg")

data = pytesseract.image_to_string(image=image, lang="eng", config="--psm 6")
print(data)

# cv2.imshow("thresh", image)
# cv2.waitKey()

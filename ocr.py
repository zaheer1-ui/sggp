import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = Image.open('some_image_with_text.png')
text = pytesseract.image_to_string(image)
print(text)

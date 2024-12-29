from pytesseract import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# Set the path to the Tesseract executable
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(filepath):
    if filepath.endswith('.pdf'):
        # Convert PDF to images
        images = convert_from_path(filepath)
        # Extract text from each image
        text = ''.join(pytesseract.image_to_string(img) for img in images)
    else:
        # Extract text directly from image files
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)
    
    return text

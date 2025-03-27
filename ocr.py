import pytesseract

class OCRProcessor:
    def __init__(self, tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def extract_text(self, image):
        return pytesseract.image_to_string(image)

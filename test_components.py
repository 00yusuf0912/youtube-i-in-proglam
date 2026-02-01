import pytesseract
from deep_translator import GoogleTranslator
from PIL import Image, ImageOps, ImageEnhance

# Test tesseract
print("Tesseract version:", pytesseract.get_tesseract_version())

# Test translator
translator = GoogleTranslator(source='en', target='tr')
test_text = "Hello world"
translated = translator.translate(test_text)
print(f"Translation test: '{test_text}' -> '{translated}'")

# Test image processing (dummy)
img = Image.new('L', (100, 100), 255)  # White image
processed = ImageOps.invert(ImageOps.grayscale(img))
processed = ImageEnhance.Contrast(processed).enhance(2.5)
ocr_result = pytesseract.image_to_string(processed, lang='eng').strip()
print(f"OCR test on empty image: '{ocr_result}'")

print("All tests passed!")
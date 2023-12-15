from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    # Open the image using Pillow
    image = Image.open(image_path)

    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(image)

    return text

# Replace 'your_image.jpg' with the path to your image file
image_path = 'sample.jpg'
result_text = extract_text_from_image(image_path)

print("Extracted Text:")
print(result_text)

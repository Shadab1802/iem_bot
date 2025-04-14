import easyocr
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

def extract_text_from_image(uploaded_file):
    # Read the uploaded file using PIL
    image = Image.open(uploaded_file).convert('RGB')

    # Convert PIL image to numpy array (OpenCV format)
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Initialize EasyOCR Reader
    reader = easyocr.Reader(['en'], gpu=False)

    # EasyOCR can accept numpy array directly
    lines = reader.readtext(image_bgr, detail=0)
    lines = [line.upper() for line in lines]

    return lines
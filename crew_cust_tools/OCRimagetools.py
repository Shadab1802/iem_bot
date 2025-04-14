from crewai.tools import BaseTool
from typing import Type
import easyocr
import cv2
import numpy as np

from pydantic import BaseModel

class ImageFileInput(BaseModel):
    file: bytes  # file.read() from Streamlit uploader

class OCRImageTool(BaseTool):
    name: str = "extract_text_from_uploaded_image"
    description: str = "Extracts text lines from an uploaded image file using OCR"
    args_schema: Type[ImageFileInput] = ImageFileInput  # ✅ proper annotation


    def _run(self, **kwargs):
        file_bytes = self.context.get("file")
        if file_bytes is None:
            return "No file provided"

        np_array = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        reader = easyocr.Reader(['en'], gpu=False)
        lines = reader.readtext(image_rgb, detail=0)
        lines = [line.upper() for line in lines]

        return lines

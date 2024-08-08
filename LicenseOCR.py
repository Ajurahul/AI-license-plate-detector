import re
import requests
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image


class LicenseOCR:
    def __int__(self):
        print("Initialized")
        self.processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed')
        self.model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed')

    def ocr_image(self, src_img):
        pixel_values = self.processor(images=src_img, return_tensors="pt").pixel_values
        generated_ids = self.model.generate(pixel_values)
        return re.sub(r'[^a-zA-Z0-9]*', '', self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0])


def get_image(path: str):
    img = Image.open(path).convert('RGB')
    return img


def show_image(url):
    img = Image.open(requests.get(url, stream=True).raw).convert('RGB')
    return img

import pytesseract
from PIL import Image
import base64
import re

class ImageService:

    image_path = "images/phone_{}.png"
    pagination_file_path = "files/pagination.txt"

    def save_image(self, base64_image, page):
        with open(self.image_path.format(page), "wb") as fh:
            fh.write(base64.b64decode(base64_image))
            fh.close()

    def get_text_image(self, page):
        image = Image.open(self.image_path.format(page))
        phone = pytesseract.image_to_string(image)
        phone = re.findall("\d+", phone)

        return "".join(phone)

    def save_pagination(self, content):
        with open(self.pagination_file_path, "w") as fh:
            fh.write(content)
            fh.close()

    def read_pagination(self):
        file = open(self.pagination_file_path)
        text = file.read()
        file.close()

        result = []
        if text:
            result = text.split(",")

        return result


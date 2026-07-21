import easyocr


class OCRService:

    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def extract_text(self, image_path):

        result = self.reader.readtext(image_path)

        lines = []

        for item in result:
            lines.append(item[1])

        return {
            "text": "\n".join(lines),
            "lines": lines
        }
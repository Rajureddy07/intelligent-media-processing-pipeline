import cv2
import easyocr


class OCRService:

    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def read(self, image):
        """
        Run OCR on an image and return only the detected text.
        """
        result = self.reader.readtext(image, detail=1)

        lines = []

        for item in result:
            text = item[1].strip()

            if len(text) > 0:
                lines.append(text)

        return lines

    def preprocess(self, image):
        """
        Improve OCR quality.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        gray = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

        return gray

    def extract_text(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            return {
                "text": "",
                "lines": []
            }

        h, w = image.shape[:2]

        all_lines = []

        # ---------------------------------------------------
        # 1. OCR on full image
        # ---------------------------------------------------
        full = self.preprocess(image)

        full_lines = self.read(full)

        # ---------------------------------------------------
        # 2. OCR on bottom-right crop
        # ---------------------------------------------------
        crop1 = image[
            int(h * 0.55):h,
            int(w * 0.50):w
        ]

        crop1 = self.preprocess(crop1)

        crop1_lines = self.read(crop1)

        # ---------------------------------------------------
        # 3. OCR on bottom-center crop
        # ---------------------------------------------------
        crop2 = image[
            int(h * 0.60):h,
            int(w * 0.25):int(w * 0.75)
        ]

        crop2 = self.preprocess(crop2)

        crop2_lines = self.read(crop2)

        # ---------------------------------------------------
        # 4. Dedicated Number Plate Crop
        # ---------------------------------------------------
        plate = image[
            int(h * 0.72):int(h * 0.95),
            int(w * 0.72):int(w * 0.98)
        ]

        # Upscale for tiny text
        plate = cv2.resize(
            plate,
            None,
            fx=4,
            fy=4,
            interpolation=cv2.INTER_CUBIC
        )

        plate = self.preprocess(plate)

        plate_lines = self.read(plate)

        # ---------------------------------------------------
        # Merge all OCR outputs
        # ---------------------------------------------------
        for line in full_lines + crop1_lines + crop2_lines + plate_lines:

            line = line.strip()

            if line and line not in all_lines:
                all_lines.append(line)

        return {
            "text": "\n".join(all_lines),
            "lines": all_lines
        }
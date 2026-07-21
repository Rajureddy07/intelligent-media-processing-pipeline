import re


class VehicleNumberDetector:

    @staticmethod
    def detect(ocr_text):
        """
        Extract a possible Indian vehicle registration number
        from OCR text.
        """

        if not ocr_text:
            return None

        # Normalize text
        text = ocr_text.upper().replace(" ", "")

        pattern = r"[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}"

        match = re.search(pattern, text)

        if match:
            return match.group()

        return None
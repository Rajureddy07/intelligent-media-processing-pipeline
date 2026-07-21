from PIL import Image, ImageChops
import os
import tempfile


class TamperDetector:

    @staticmethod
    def detect(image_path):
        try:
            original = Image.open(image_path).convert("RGB")

            # Save as JPEG with lower quality
            temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            temp_path = temp_file.name
            temp_file.close()

            original.save(temp_path, "JPEG", quality=90)

            compressed = Image.open(temp_path)

            ela = ImageChops.difference(original, compressed)

            bbox = ela.getbbox()

            os.remove(temp_path)

            return {
                "tampered": bbox is not None
            }

        except Exception:
            return {
                "tampered": False
            }
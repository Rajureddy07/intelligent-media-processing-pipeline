from PIL import Image


class MetadataAnalyzer:

    @staticmethod
    def analyze(image_path):

        try:
            image = Image.open(image_path)

            exif = image.getexif()

            if exif:
                return {
                    "metadata_available": True,
                    "metadata_count": len(exif)
                }

            return {
                "metadata_available": False,
                "metadata_count": 0
            }

        except Exception:
            return {
                "metadata_available": False,
                "metadata_count": 0
            }
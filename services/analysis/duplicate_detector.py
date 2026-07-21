from PIL import Image
import imagehash

from database.models import Advertisement


class DuplicateDetector:

    @staticmethod
    def calculate_hash(image_path):
        image = Image.open(image_path)
        return str(imagehash.phash(image))

    @staticmethod
    def check_duplicate(image_path):

        current_hash = DuplicateDetector.calculate_hash(image_path)

        advertisements = Advertisement.query.all()

        for advertisement in advertisements:

            # Skip if this record doesn't have a hash yet
            if not advertisement.image_hash:
                continue

            if advertisement.image_hash == current_hash:
                return {
                    "is_duplicate": True,
                    "matched_processing_id": advertisement.processing_id,
                    "image_hash": current_hash
                }

        return {
            "is_duplicate": False,
            "matched_processing_id": None,
            "image_hash": current_hash
        }
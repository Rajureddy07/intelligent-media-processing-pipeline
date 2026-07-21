import cv2


class ScreenshotDetector:

    @staticmethod
    def detect(image_path):

        image = cv2.imread(image_path)

        if image is None:
            return {
                "is_screenshot": False,
                "reason": "Image not found"
            }

        height, width = image.shape[:2]

        # Common screenshot aspect ratios
        aspect_ratio = round(width / height, 2)

        common_ratios = [
            0.46,  # Portrait phones
            0.56,
            1.78,  # 16:9
            2.17,
            2.22
        ]

        is_screenshot = any(
            abs(aspect_ratio - r) < 0.05
            for r in common_ratios
        )

        return {
            "is_screenshot": is_screenshot,
            "aspect_ratio": aspect_ratio
        }
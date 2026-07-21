import cv2


class ImageQualityAnalyzer:

    @staticmethod
    def analyze(image_path):

        image = cv2.imread(image_path)

        if image is None:
            raise Exception("Unable to read image.")

        height, width = image.shape[:2]

        # Resolution
        resolution = f"{width} x {height}"

        # Brightness
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = float(gray.mean())

        # Blur Detection
        blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())

        if blur_score < 100:
            blur_status = "Blurry"
        else:
            blur_status = "Sharp"

        # Resolution Quality
        if width >= 1280 and height >= 720:
            resolution_status = "High"
        elif width >= 640 and height >= 480:
            resolution_status = "Medium"
        else:
            resolution_status = "Low"

        # Brightness Quality
        if brightness < 50:
            brightness_status = "Too Dark"
        elif brightness > 200:
            brightness_status = "Too Bright"
        else:
            brightness_status = "Good"

        return {
            "resolution": resolution,
            "width": width,
            "height": height,
            "resolution_status": resolution_status,
            "brightness": round(brightness, 2),
            "brightness_status": brightness_status,
            "blur_score": round(blur_score, 2),
            "blur_status": blur_status
        }
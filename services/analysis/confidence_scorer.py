class ConfidenceScorer:

    @staticmethod
    def calculate(
        image_quality,
        ocr_result,
        vehicle_number,
        duplicate,
        screenshot,
        metadata,
        tamper
    ):

        scores = {}

        # OCR
        text = ocr_result.get("text", "").strip()
        scores["ocr"] = 95 if text else 20

        # Vehicle Number
        scores["vehicle_number"] = 98 if vehicle_number else 25

        # Image Quality
        blur = image_quality.get("blur_score", 0)
        brightness = image_quality.get("brightness", 0)

        quality = 100

        if blur < 100:
            quality -= 30

        if brightness < 40 or brightness > 220:
            quality -= 20

        scores["image_quality"] = max(0, quality)

        # Duplicate
        if isinstance(duplicate, dict):
            is_duplicate = duplicate.get("is_duplicate", False)
        else:
            is_duplicate = bool(duplicate)

        scores["duplicate"] = 90 if not is_duplicate else 60

        # Screenshot
        if isinstance(screenshot, dict):
            is_screenshot = screenshot.get("is_screenshot", False)
        else:
            is_screenshot = bool(screenshot)

        scores["screenshot"] = 90 if not is_screenshot else 70

        # Metadata
        scores["metadata"] = 100 if bool(metadata) else 70

        # Tamper
        if isinstance(tamper, dict):
            is_tampered = tamper.get("tampered", False)
        else:
            is_tampered = bool(tamper)

        scores["tamper"] = 100 if not is_tampered else 50

        overall = round(sum(scores.values()) / len(scores))

        scores["overall"] = overall

        return scores
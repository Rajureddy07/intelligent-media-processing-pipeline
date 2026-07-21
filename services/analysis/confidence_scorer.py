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

        # OCR Confidence
        text = ocr_result.get("text", "").strip()
        scores["ocr"] = 95 if text else 20

        # Vehicle Number Confidence
        scores["vehicle_number"] = (
            98 if vehicle_number else 25
        )

        # Image Quality Confidence
        blur = image_quality.get("blur_score", 0)
        brightness = image_quality.get("brightness", 0)

        quality = 100

        if blur < 100:
            quality -= 30

        if brightness < 40 or brightness > 220:
            quality -= 20

        scores["image_quality"] = max(0, quality)

        # Duplicate Confidence
        scores["duplicate"] = (
            100 if duplicate.get("is_duplicate") else 90
        )

        # Screenshot Confidence
        scores["screenshot"] = (
            100 if not screenshot.get("is_screenshot") else 60
        )

        # Metadata Confidence
        scores["metadata"] = (
            100 if metadata.get("metadata_available") else 70
        )

        # Tamper Confidence
        scores["tamper"] = (
            100 if not tamper.get("tampered") else 50
        )

        overall = round(
            sum(scores.values()) / len(scores)
        )

        scores["overall"] = overall

        return scores
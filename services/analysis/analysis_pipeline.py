from services.analysis.image_quality import ImageQualityAnalyzer
from services.analysis.vehicle_number_detector import VehicleNumberDetector
from services.analysis.vehicle_number_validator import VehicleNumberValidator
from services.analysis.duplicate_detector import DuplicateDetector
from services.analysis.screenshot_detector import ScreenshotDetector
from services.analysis.metadata_analyzer import MetadataAnalyzer
from services.analysis.tamper_detector import TamperDetector
from services.analysis.confidence_scorer import ConfidenceScorer
from services.ocr.ocr_service import OCRService


class AnalysisPipeline:

    @staticmethod
    def run(image_path):

        # Image Quality
        image_quality = ImageQualityAnalyzer.analyze(image_path)

        # OCR
        ocr = OCRService()
        ocr_result = ocr.extract_text(image_path)

        extracted_text = ocr_result.get("text", "")

        # Vehicle Number
        vehicle_number = VehicleNumberDetector.detect(extracted_text)


        # Validate only if a number was detected
        if vehicle_number:
            is_valid = VehicleNumberValidator.validate(vehicle_number)

            # If validation fails, discard the result
            if not is_valid:
                vehicle_number = None
        else:
            vehicle_number = None
            is_valid = False

        # Duplicate
        duplicate = DuplicateDetector.check_duplicate(image_path)

        # Screenshot
        screenshot = ScreenshotDetector.detect(image_path)

        # Metadata
        metadata = MetadataAnalyzer.analyze(image_path)

        # Tamper
        tamper = TamperDetector.detect(image_path)

        # Confidence
        confidence = ConfidenceScorer.calculate(
            image_quality,
            ocr_result,
            vehicle_number,
            duplicate,
            screenshot,
            metadata,
            tamper
        )

        return {
            "image_quality": image_quality,

            "ocr": ocr_result,

            "vehicle_number": {
                "number": vehicle_number,
                "valid": is_valid
            },

            "duplicate": duplicate,

            "screenshot": screenshot,

            "metadata": metadata,

            "tamper": tamper,

            "confidence": confidence
        }
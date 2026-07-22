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

        print("=" * 80)
        print("🚀 Analysis Pipeline Started")
        print(f"Image Path: {image_path}")
        print("=" * 80)

        # ---------------------------------------------------
        # Image Quality
        # ---------------------------------------------------
        print("1️⃣ Running Image Quality Analysis...")
        image_quality = ImageQualityAnalyzer.analyze(image_path)
        print("✅ Image Quality Analysis Completed")

        # ---------------------------------------------------
        # OCR
        # ---------------------------------------------------
        print("2️⃣ Running OCR...")
        ocr = OCRService()
        ocr_result = ocr.extract_text(image_path)
        print("✅ OCR Completed")

        extracted_text = ocr_result.get("text", "")

        # ---------------------------------------------------
        # Vehicle Number Detection
        # ---------------------------------------------------
        print("3️⃣ Detecting Vehicle Number...")
        vehicle_number = VehicleNumberDetector.detect(extracted_text)
        print(f"Detected Vehicle Number: {vehicle_number}")

        # ---------------------------------------------------
        # Vehicle Number Validation
        # ---------------------------------------------------
        print("4️⃣ Validating Vehicle Number...")

        if vehicle_number:
            is_valid = VehicleNumberValidator.validate(vehicle_number)

            if not is_valid:
                vehicle_number = None
        else:
            vehicle_number = None
            is_valid = False

        print(f"Vehicle Number Valid: {is_valid}")

        # ---------------------------------------------------
        # Duplicate Detection
        # ---------------------------------------------------
        print("5️⃣ Checking Duplicate Image...")
        duplicate = DuplicateDetector.check_duplicate(image_path)
        print("✅ Duplicate Detection Completed")

        # ---------------------------------------------------
        # Screenshot Detection
        # ---------------------------------------------------
        print("6️⃣ Detecting Screenshot...")
        screenshot = ScreenshotDetector.detect(image_path)
        print("✅ Screenshot Detection Completed")

        # ---------------------------------------------------
        # Metadata Analysis
        # ---------------------------------------------------
        print("7️⃣ Analyzing Metadata...")
        metadata = MetadataAnalyzer.analyze(image_path)
        print("✅ Metadata Analysis Completed")

        # ---------------------------------------------------
        # Tamper Detection
        # ---------------------------------------------------
        print("8️⃣ Detecting Tampering...")
        tamper = TamperDetector.detect(image_path)
        print("✅ Tamper Detection Completed")

        # ---------------------------------------------------
        # Confidence Score
        # ---------------------------------------------------
        print("9️⃣ Calculating Confidence Score...")
        confidence = ConfidenceScorer.calculate(
            image_quality,
            ocr_result,
            vehicle_number,
            duplicate,
            screenshot,
            metadata,
            tamper
        )
        print("✅ Confidence Score Calculated")

        print("=" * 80)
        print("🎉 Analysis Pipeline Completed Successfully")
        print("=" * 80)

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
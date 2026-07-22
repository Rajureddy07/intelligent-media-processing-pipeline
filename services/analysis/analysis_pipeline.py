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
        # 1. Image Quality
        # ---------------------------------------------------
        print("1️⃣ Running Image Quality Analysis...")
        image_quality = ImageQualityAnalyzer.analyze(image_path)
        print("✅ Image Quality Completed")

        blur_score = image_quality.get("blur_score", 0)

        # FIX: ImageQualityAnalyzer returns "brightness"
        brightness_score = image_quality.get("brightness", 0)

        resolution = image_quality.get("resolution", "Unknown")

        # ---------------------------------------------------
        # 2. OCR
        # ---------------------------------------------------
        print("2️⃣ Running OCR...")
        ocr = OCRService()
        ocr_result = ocr.extract_text(image_path)
        print("✅ OCR Completed")

        extracted_text = ocr_result.get("text", "")

        # ---------------------------------------------------
        # 3. Vehicle Detection
        # ---------------------------------------------------
        print("3️⃣ Detecting Vehicle Number...")

        vehicle_number = VehicleNumberDetector.detect(extracted_text)

        print(f"Vehicle Number: {vehicle_number}")

        # ---------------------------------------------------
        # 4. Validation
        # ---------------------------------------------------
        print("4️⃣ Validating Vehicle Number...")

        if vehicle_number:
            vehicle_valid = VehicleNumberValidator.validate(vehicle_number)
        else:
            vehicle_valid = False
            vehicle_number = ""

        print(f"Vehicle Valid: {vehicle_valid}")

        # ---------------------------------------------------
        # 5. Duplicate
        # ---------------------------------------------------
        print("5️⃣ Checking Duplicate...")

        duplicate = DuplicateDetector.check_duplicate(image_path)

        print(f"Duplicate: {duplicate}")

        # ---------------------------------------------------
        # 6. Screenshot
        # ---------------------------------------------------
        print("6️⃣ Detecting Screenshot...")

        screenshot = ScreenshotDetector.detect(image_path)

        print(f"Screenshot: {screenshot}")

        # ---------------------------------------------------
        # 7. Metadata
        # ---------------------------------------------------
        print("7️⃣ Reading Metadata...")

        metadata = MetadataAnalyzer.analyze(image_path)

        metadata_available = bool(metadata)

        print(f"Metadata Available: {metadata_available}")

        # ---------------------------------------------------
        # 8. Tamper
        # ---------------------------------------------------
        print("8️⃣ Detecting Tampering...")

        tamper = TamperDetector.detect(image_path)

        print(f"Tampered: {tamper}")

        # ---------------------------------------------------
        # 9. Confidence
        # ---------------------------------------------------
        print("9️⃣ Calculating Confidence...")

        confidence = ConfidenceScorer.calculate(
            image_quality,
            ocr_result,
            vehicle_number,
            duplicate,
            screenshot,
            metadata,
            tamper
        )

        # FIX: ConfidenceScorer returns "overall"
        if isinstance(confidence, dict):
            confidence_score = confidence.get("overall", 0)
        else:
            confidence_score = confidence

        print(f"Confidence Score: {confidence_score}")

        print("=" * 80)
        print("🎉 Analysis Completed Successfully")
        print("=" * 80)

        # ---------------------------------------------------
        # Final Report
        # ---------------------------------------------------

        report = {

            "ocr_text": extracted_text,

            "vehicle_number": vehicle_number,

            "vehicle_number_valid": vehicle_valid,

            "blur_score": blur_score,

            "brightness_score": brightness_score,

            "resolution": resolution,

            # Store simple values for the dashboard
            "duplicate_image": duplicate.get("is_duplicate", False),

            "screenshot_detected": screenshot.get("is_screenshot", False),

            "metadata_available": metadata_available,

            "tampered": tamper.get("tampered", False),

            "confidence_score": confidence_score,

            # Store detailed detector outputs for report_json
            "duplicate": duplicate,
            "screenshot": screenshot,
            "metadata": metadata,
            "tamper": tamper,
            "image_quality": image_quality,
            "ocr": ocr_result,
            "confidence": confidence

        }

        return report
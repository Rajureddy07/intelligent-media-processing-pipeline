import os
import threading
import logging
import traceback

from database.db import db
from database.models import Advertisement, AnalysisReport
from services.analysis.analysis_pipeline import AnalysisPipeline
from workers.task_queue import task_queue

# Maximum retry attempts
MAX_RETRIES = 2

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure Logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_image(app):

    print("✅ Background worker started.")

    while True:

        task = task_queue.get()

        print(f"📩 Worker received task: {task}")

        if task is None:
            print("🛑 Worker stopped.")
            break

        processing_id = task["processing_id"]

        print("=" * 80)
        print(f"🚀 Processing Started : {processing_id}")
        print("=" * 80)

        with app.app_context():

            advertisement = Advertisement.query.filter_by(
                processing_id=processing_id
            ).first()

            if advertisement is None:

                logging.warning(
                    f"Advertisement not found : {processing_id}"
                )

                print("❌ Advertisement not found.")

                task_queue.task_done()
                continue

            advertisement.status = "Processing"
            db.session.commit()

            success = False

            while advertisement.retry_count < MAX_RETRIES and not success:

                try:

                    logging.info(
                        f"Attempt {advertisement.retry_count + 1}"
                    )

                    print("🔍 Running Analysis Pipeline...")

                    result = AnalysisPipeline.run(
                        advertisement.image_path
                    )

                    print("✅ Analysis Completed")

                    print("=" * 80)
                    print("PIPELINE RESULT")
                    print(result)
                    print("=" * 80)

                    # Save image hash
                    advertisement.image_hash = None

                    duplicate_info = result.get("duplicate")

                    if isinstance(duplicate_info, dict):
                        advertisement.image_hash = duplicate_info.get(
                            "image_hash"
                        )

                    report = AnalysisReport(

                        advertisement_id=advertisement.id,

                        extracted_text=result.get(
                            "ocr_text", ""
                        ),

                        vehicle_number=result.get(
                            "vehicle_number", ""
                        ),

                        vehicle_number_valid=bool(
                            result.get("vehicle_number_valid", False)
                        ),

                        blur_score=float(
                            result.get("blur_score", 0)
                        ),

                        brightness_score=float(
                            result.get("brightness_score", 0)
                        ),

                        resolution=result.get(
                            "resolution", ""
                        ),

                        duplicate_image=bool(
                            result.get("duplicate_image", False)
                        ),

                        screenshot_detected=bool(
                            result.get("screenshot_detected", False)
                        ),

                        metadata_available=bool(
                            result.get("metadata_available", False)
                        ),

                        tampered=bool(
                            result.get("tampered", False)
                        ),

                        report_json=result

                    )

                    db.session.add(report)

                    advertisement.status = "Completed"

                    db.session.commit()

                    success = True

                    print("🎉 Processing Completed Successfully")

                    logging.info(
                        f"Completed : {processing_id}"
                    )

                except Exception as e:

                    db.session.rollback()

                    print("=" * 80)
                    print("❌ PROCESSING FAILED")
                    traceback.print_exc()
                    print("=" * 80)

                    logging.exception(str(e))

                    advertisement.retry_count += 1
                    db.session.commit()

                    if advertisement.retry_count >= MAX_RETRIES:

                        advertisement.status = "Failed"
                        advertisement.failure_reason = str(e)

                        db.session.commit()

                        print("❌ Maximum Retry Limit Reached")

                        logging.error(
                            f"Failed : {processing_id}"
                        )

        task_queue.task_done()


def start_worker(app):

    worker = threading.Thread(
        target=process_image,
        args=(app,),
        daemon=True
    )

    worker.start()

    print("✅ Worker thread initialized.")
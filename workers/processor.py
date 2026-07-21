import threading
import logging

from database.db import db
from database.models import Advertisement, AnalysisReport
from services.analysis.analysis_pipeline import AnalysisPipeline
from workers.task_queue import task_queue
import os


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

    while True:

        task = task_queue.get()

        if task is None:
            break

        processing_id = task["processing_id"]

        with app.app_context():

            advertisement = Advertisement.query.filter_by(
                processing_id=processing_id
            ).first()

            if not advertisement:
                logging.warning(
                    f"Advertisement not found for Processing ID: {processing_id}"
                )
                task_queue.task_done()
                continue

            advertisement.status = "Processing"
            db.session.commit()

            success = False

            while advertisement.retry_count < MAX_RETRIES and not success:

                try:

                    logging.info(
                        f"Processing {processing_id} | Attempt {advertisement.retry_count + 1}"
                    )

                    result = AnalysisPipeline.run(
                        advertisement.image_path
                    )

                    # Save image hash
                    advertisement.image_hash = result["duplicate"]["image_hash"]

                    report = AnalysisReport(

                        advertisement_id=advertisement.id,

                        extracted_text=result["ocr"]["text"],

                        vehicle_number=result["vehicle_number"]["number"],

                        vehicle_number_valid=result["vehicle_number"]["valid"],

                        blur_score=result["image_quality"]["blur_score"],

                        brightness_score=result["image_quality"]["brightness"],

                        resolution=result["image_quality"]["resolution"],

                        duplicate_image=result["duplicate"]["is_duplicate"],

                        screenshot_detected=result["screenshot"]["is_screenshot"],

                        metadata_available=result["metadata"]["metadata_available"],

                        tampered=result["tamper"]["tampered"],

                        report_json=result

                    )

                    db.session.add(report)

                    advertisement.status = "Completed"

                    db.session.commit()

                    success = True

                    logging.info(
                        f"Processing Completed Successfully: {processing_id}"
                    )

                except Exception as e:

                    advertisement.retry_count += 1

                    db.session.commit()

                    logging.exception(
                        f"Attempt {advertisement.retry_count} failed for {processing_id}"
                    )

                    if advertisement.retry_count >= MAX_RETRIES:

                        advertisement.status = "Failed"
                        advertisement.failure_reason = str(e)

                        db.session.commit()

                        logging.exception(
                            f"Processing Failed after {MAX_RETRIES} attempts: {processing_id}"
                        )

        task_queue.task_done()


def start_worker(app):

    worker = threading.Thread(
        target=process_image,
        args=(app,),
        daemon=True
    )

    worker.start()
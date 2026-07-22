import os

from workers.task_queue import task_queue

from database.db import db
from database.models import Advertisement

from utils.file_utils import (
    create_directory,
    generate_filename,
    generate_processing_id
)


class UploadService:

    @staticmethod
    def save_image(image):

        upload_folder = "uploads"

        create_directory(upload_folder)

        filename = generate_filename(image.filename)
        image_path = os.path.join(upload_folder, filename)

        try:
            # Save uploaded image
            image.save(image_path)

            processing_id = generate_processing_id()

            advertisement = Advertisement(
                processing_id=processing_id,
                filename=filename,
                image_path=image_path,
                status="Pending"
            )

            db.session.add(advertisement)
            db.session.commit()

            print("=" * 80)
            print(f"Queue size before put: {task_queue.qsize()}")

            # Send task to background worker
            task_queue.put({
                "processing_id": processing_id
            })

            print(f"Queue size after put: {task_queue.qsize()}")
            print(f"Task queued successfully: {processing_id}")
            print("=" * 80)

            return {
                "processing_id": processing_id,
                "filename": filename,
                "image_path": image_path
            }

        except Exception as e:
            db.session.rollback()

            # Remove partially saved image if it exists
            if os.path.exists(image_path):
                os.remove(image_path)

            raise Exception(f"Upload failed: {str(e)}")
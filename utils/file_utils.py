import os
import uuid
from PIL import Image

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_processing_id():
    return str(uuid.uuid4())


def generate_filename(filename):
    extension = filename.rsplit(".", 1)[1].lower()
    return f"{uuid.uuid4()}.{extension}"


def create_directory(path):
    os.makedirs(path, exist_ok=True)


def validate_image(image):

    # Empty filename
    if image.filename == "":
        return False, "No file selected"

    # Extension
    if not allowed_file(image.filename):
        return False, "Invalid file type"

    # File size
    image.seek(0, os.SEEK_END)
    size = image.tell()

    if size > MAX_FILE_SIZE:
        image.seek(0)
        return False, "Image exceeds 10 MB limit"

    image.seek(0)

    # Corrupted image check
    try:
        img = Image.open(image)
        img.verify()
        image.seek(0)
    except Exception:
        return False, "Invalid or corrupted image"

    return True, None
import os
import uuid

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


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
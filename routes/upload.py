from flask import Blueprint, jsonify, request

from services.upload_service import UploadService
from utils.file_utils import validate_image

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload():

    # Check if image is present in request
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "Image is required"
        }), 400

    image = request.files["image"]

    # Validate uploaded image
    valid, error = validate_image(image)

    if not valid:
        return jsonify({
            "success": False,
            "error": error
        }), 400

    try:
        response = UploadService.save_image(image)

        return jsonify({
            "success": True,
            "processing_id": response["processing_id"],
            "status": "Pending"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
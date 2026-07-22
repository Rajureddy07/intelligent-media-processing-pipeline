from flask import Blueprint, jsonify, request

from services.upload_service import UploadService
from utils.file_utils import validate_image

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload():
    """
    Upload an advertisement image for analysis.
    """

    # Check if image field exists
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "No image file provided."
        }), 400

    image = request.files["image"]

    # Check filename
    if image.filename == "":
        return jsonify({
            "success": False,
            "error": "No image selected."
        }), 400

    # Validate image
    valid, error = validate_image(image)

    if not valid:
        return jsonify({
            "success": False,
            "error": error
        }), 400

    try:
        # Save image and queue processing
        response = UploadService.save_image(image)

        return jsonify({
            "success": True,
            "message": "Image uploaded successfully.",
            "processing_id": response["processing_id"],
            "status": "Pending",
            "status_url": f"/api/status/{response['processing_id']}",
            "results_url": f"/api/results/{response['processing_id']}"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
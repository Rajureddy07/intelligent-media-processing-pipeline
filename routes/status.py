from flask import Blueprint, jsonify

from database.models import Advertisement

status_bp = Blueprint("status", __name__)


@status_bp.route("/status/<processing_id>", methods=["GET"])
def get_status(processing_id):
    """
    Returns the current processing status of an uploaded advertisement.
    """

    advertisement = Advertisement.query.filter_by(
        processing_id=processing_id
    ).first()

    if advertisement is None:
        return jsonify({
            "success": False,
            "error": "Processing ID not found"
        }), 404

    response = {
        "success": True,
        "processing_id": advertisement.processing_id,
        "filename": advertisement.filename,
        "status": advertisement.status
    }

    # If processing failed, include the failure reason
    if advertisement.status == "Failed":
        response["failure_reason"] = advertisement.failure_reason

    # If processing completed, provide the results URL
    if advertisement.status == "Completed":
        response["results_url"] = f"/api/results/{advertisement.processing_id}"

    return jsonify(response), 200
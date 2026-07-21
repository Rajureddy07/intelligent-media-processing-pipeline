from flask import Blueprint, jsonify

from database.models import Advertisement

status_bp = Blueprint("status", __name__)


@status_bp.route("/status/<processing_id>", methods=["GET"])
def get_status(processing_id):

    advertisement = Advertisement.query.filter_by(
        processing_id=processing_id
    ).first()

    if advertisement is None:
        return jsonify({
            "success": False,
            "message": "Processing ID not found"
        }), 404

    response = {
        "success": True,
        "processing_id": advertisement.processing_id,
        "status": advertisement.status
    }

    # Include failure reason only if processing failed
    if advertisement.status == "Failed":
        response["failure_reason"] = advertisement.failure_reason

    return jsonify(response), 200
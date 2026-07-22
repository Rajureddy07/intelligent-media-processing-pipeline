from flask import Blueprint, jsonify
from database.models import Advertisement

results_bp = Blueprint("results", __name__)


@results_bp.route("/results/<processing_id>", methods=["GET"])
def get_results(processing_id):

    advertisement = Advertisement.query.filter_by(
        processing_id=processing_id
    ).first()

    if advertisement is None:
        return jsonify({
            "success": False,
            "error": "Processing ID not found"
        }), 404

    report = advertisement.report

    if report is None:
        return jsonify({
            "success": False,
            "error": "Report not available"
        }), 404

    return jsonify({
        "success": True,
        "processing_id": advertisement.processing_id,
        "status": advertisement.status,
        "filename": advertisement.filename,
        "analysis": report.report_json
    }), 200
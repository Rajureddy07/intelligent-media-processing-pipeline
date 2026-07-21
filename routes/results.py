from flask import Blueprint, jsonify
from database.models import Advertisement

results_bp = Blueprint("results", __name__)

@results_bp.route("/api/results/<processing_id>", methods=["GET"])
def get_results(processing_id):

    advertisement = Advertisement.query.filter_by(
        processing_id=processing_id
    ).first()

    if not advertisement:
        return jsonify({"error": "Processing ID not found"}), 404

    report = advertisement.report

    if report is None:
        return jsonify({"error": "Report not available"}), 404

    return jsonify({
        "processing_id": advertisement.processing_id,
        "status": advertisement.status,
        "filename": advertisement.filename,
        "analysis": report.report_json
    }), 200
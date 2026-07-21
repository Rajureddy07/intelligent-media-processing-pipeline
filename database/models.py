from datetime import datetime

from database.db import db


class Advertisement(db.Model):
    __tablename__ = "advertisements"

    id = db.Column(db.Integer, primary_key=True)

    processing_id = db.Column(db.String(100), unique=True, nullable=False)

    filename = db.Column(db.String(255), nullable=False)

    image_path = db.Column(db.String(500), nullable=False)

    image_hash = db.Column(db.String(64))

    retry_count = db.Column(db.Integer, default=0)
    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    # NEW
    failure_reason = db.Column(db.Text)

    report = db.relationship(
        "AnalysisReport",
        backref="advertisement",
        uselist=False,
        cascade="all, delete"
    )


class AnalysisReport(db.Model):
    __tablename__ = "analysis_reports"

    id = db.Column(db.Integer, primary_key=True)

    advertisement_id = db.Column(
        db.Integer,
        db.ForeignKey("advertisements.id"),
        nullable=False
    )

    # OCR
    extracted_text = db.Column(db.Text)

    # Vehicle Number
    vehicle_number = db.Column(db.String(30))

    vehicle_number_valid = db.Column(db.Boolean)

    # Image Quality
    blur_score = db.Column(db.Float)

    brightness_score = db.Column(db.Float)

    resolution = db.Column(db.String(50))

    # Assignment Checks
    duplicate_image = db.Column(db.Boolean)

    screenshot_detected = db.Column(db.Boolean)

    metadata_available = db.Column(db.Boolean)

    tampered = db.Column(db.Boolean)

    # Final JSON Result
    report_json = db.Column(db.JSON)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
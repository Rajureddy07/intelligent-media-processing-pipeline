from app import app
from services.analysis.duplicate_detector import DuplicateDetector

image = r"C:\Users\Admin\OneDrive\Desktop\carplate.jpg"

with app.app_context():
    result = DuplicateDetector.check_duplicate(image)
    print(result)
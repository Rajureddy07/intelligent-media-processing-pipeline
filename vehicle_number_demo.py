from services.analysis.vehicle_number_detector import VehicleNumberDetector

samples = [
    "KA01AB1234",
    "Vehicle No: MH12DE5678",
    "Welcome to VCET",
    "DL8CAF5032"
]

for text in samples:
    print(text)
    print(VehicleNumberDetector.detect(text))
    print("-" * 40)
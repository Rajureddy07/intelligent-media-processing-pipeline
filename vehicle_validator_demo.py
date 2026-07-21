from services.analysis.vehicle_number_validator import VehicleNumberValidator

samples = [
    "KA01AB1234",
    "MH12DE5678",
    "DL8CAF5032",
    "123456",
    "ABC123",
    "KA999",
    None
]

for sample in samples:
    print(sample, "->", VehicleNumberValidator.validate(sample))
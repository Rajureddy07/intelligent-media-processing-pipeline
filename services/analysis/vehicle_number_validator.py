import re


class VehicleNumberValidator:

    @staticmethod
    def validate(vehicle_number):

        if not vehicle_number:
            return False

        pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$"

        return bool(re.fullmatch(pattern, vehicle_number))
import re


class VehicleNumberDetector:

    VALID_STATE_CODES = {
        "AP", "AR", "AS", "BR", "CG", "CH", "DD", "DL", "DN",
        "GA", "GJ", "HR", "HP", "JH", "JK", "KA", "KL", "LA",
        "LD", "MH", "ML", "MN", "MP", "MZ", "NL", "OD", "PB",
        "PY", "RJ", "SK", "TN", "TR", "TS", "UK", "UP", "WB"
    }

    BLACKLIST = {
        "ROAD",
        "PUNE",
        "CREATIVITY",
        "ARENA",
        "GLOBAL",
        "ALUMNI",
        "TASK",
        "INDIA",
        "AGARWALS",
        "HOSPITAL",
        "CLINIC",
        "PHONE",
        "CONTACT",
        "MOBILE"
    }

    @staticmethod
    def normalize(text):
        """
        Correct common OCR mistakes.
        """

        replacements = {
            "O": "0",
            "Q": "0",
            "D": "0",
            "I": "1",
            "L": "1",
            "Z": "2",
            "S": "5",
            "B": "8"
        }

        result = ""

        for ch in text.upper():
            result += replacements.get(ch, ch)

        return result

    @staticmethod
    def is_blacklisted(text):

        for word in VehicleNumberDetector.BLACKLIST:
            if word in text:
                return True

        return False

    @staticmethod
    def is_valid_pattern(candidate):

        pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$"

        if not re.fullmatch(pattern, candidate):
            return False

        if candidate[:2] not in VehicleNumberDetector.VALID_STATE_CODES:
            return False

        return True

    @staticmethod
    def detect(ocr_text):

        if not ocr_text:
            return None

        lines = []

        for line in ocr_text.split("\n"):

            clean = re.sub(r"[^A-Za-z0-9]", "", line.upper())

            if clean:
                lines.append(clean)

        candidates = []

        # Individual OCR lines
        for line in lines:

            if VehicleNumberDetector.is_blacklisted(line):
                continue

            candidates.append(line)
            candidates.append(
                VehicleNumberDetector.normalize(line)
            )

        # Merge only adjacent short lines
        for i in range(len(lines) - 1):

            a = lines[i]
            b = lines[i + 1]

            if len(a) <= 6 and len(b) <= 6:

                merged = a + b

                if not VehicleNumberDetector.is_blacklisted(merged):
                    candidates.append(merged)
                    candidates.append(
                        VehicleNumberDetector.normalize(merged)
                    )

        for candidate in candidates:

            if VehicleNumberDetector.is_valid_pattern(candidate):
                return candidate

        return None
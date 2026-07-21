import re


class ContactExtractor:

    @staticmethod
    def extract(text):

        # Phone Numbers
        phone_pattern = r"\b(?:\+91[- ]?)?[6-9]\d{9}\b"
        phone_numbers = list(set(re.findall(phone_pattern, text)))

        # Email Addresses
        email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        emails = list(set(re.findall(email_pattern, text)))

        # Website URLs
        website_pattern = (
            r"(?:https?://)?(?:www\.)?[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        )
        websites = list(set(re.findall(website_pattern, text)))

        return {
            "phone_numbers": phone_numbers,
            "emails": emails,
            "websites": websites
        }
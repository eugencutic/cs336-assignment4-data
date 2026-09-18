

from typing import ClassVar
import re

class PIIMasker:
    EMAIL_REGEX: ClassVar[str] = r'[^\s@]+@[^\s@]+\.[^\s@]+'
    PHONE_REGEX: ClassVar[str] = r'\+?\(?\d[\d\s().-]{7,}\d'
    IP_REGEX: ClassVar[str] = r'((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])'

    @staticmethod
    def mask_emails(text):
        masked, count = re.subn(PIIMasker.EMAIL_REGEX, '|||EMAIL_ADDRESS|||', text)
        return masked, count  
        

    @staticmethod
    def mask_ips(text):
        masked, count = re.subn(PIIMasker.IP_REGEX, '|||IP_ADDRESS|||', text)
        return masked, count

    @staticmethod
    def mask_phone_numbers(text):
        masked, count = re.subn(PIIMasker.PHONE_REGEX, '|||PHONE_NUMBER|||', text)
        return masked, count

    @staticmethod
    def mask_all(text):
        text, email_count = PIIMasker.mask_emails(text)
        text, phone_count = PIIMasker.mask_phone_numbers(text)
        text, ip_count = PIIMasker.mask_ips(text)
        return text, email_count + phone_count + ip_count

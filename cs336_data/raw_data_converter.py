from resiliparse.extract.html2text import extract_plain_text
from resiliparse.parse.encoding import detect_encoding

class RawDataConverter:
    @staticmethod
    def extract_text(content_bytes: bytes) -> str:
        detected_encoding = detect_encoding(content_bytes, html5_compatible=False)

        if detected_encoding is None:
            detected_encoding = 'utf-8'

        content_str = content_bytes.decode(detected_encoding)

        extracted_text = extract_plain_text(content_str)

        return extracted_text

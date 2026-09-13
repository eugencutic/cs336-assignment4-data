import logging
from pathlib import Path
from typing import Tuple
import fasttext

LANG_ID_MODEL_PATH = Path(Path(__file__).parent, 'lid.176.bin')

class LanguageIdentifier:
    def __init__(self):
        self.model_path = Path(LANG_ID_MODEL_PATH)
        self.logger = logging.getLogger(__name__)

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not at {self.model_path.resolve()}. Download from https://fasttext.cc/docs/en/language-identification.html")

        self.model = fasttext.load_model(self.model_path.resolve()._str)

    def identify_language(self, input_str: str) -> Tuple[str, float]:
        self.logger.info(f'Identifying language. Doc preview: {input_str[:30]}')

        labels, confidence_arr = self.model.predict(input_str.replace('\n', ' '))

        self.logger.info(f'fasttext output:\nlabels:{labels}\nconfidence_arr:{confidence_arr}')

        label = str(labels[0])
        label = str(label)[9:] if label.startswith('__label__') else label
        confidence = confidence_arr[0]

        self.logger.info(f'Final label: {label}\nConfidence:{confidence}')

        return (label, confidence)

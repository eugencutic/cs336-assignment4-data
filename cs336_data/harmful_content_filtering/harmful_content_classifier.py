from pathlib import Path
import logging
from typing import Tuple
import fasttext

TOXIC_CLASSIFIER_MODEL_PATH = Path(Path(__file__).parent, 'jigsaw_fasttext_bigrams_hatespeech_final.bin') 
NSFW_CLASSIFIER_MODEL_PATH = Path(Path(__file__).parent, 'jigsaw_fasttext_bigrams_nsfw_final.bin')

class HarmfulContentClassifier:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        if not TOXIC_CLASSIFIER_MODEL_PATH.exists():
            raise FileNotFoundError(f"Toxic classifier model not found at {TOXIC_CLASSIFIER_MODEL_PATH}")
        
        if not NSFW_CLASSIFIER_MODEL_PATH.exists():
            raise FileNotFoundError(f"NSFW classifier model not found at {NSFW_CLASSIFIER_MODEL_PATH}")

        self._toxic_classifier = fasttext.load_model(TOXIC_CLASSIFIER_MODEL_PATH.resolve().as_posix())
        self.logger.info(f"Toxic classifier model loaded from {TOXIC_CLASSIFIER_MODEL_PATH.resolve()}")

        self._nsfw_classifier = fasttext.load_model(NSFW_CLASSIFIER_MODEL_PATH.resolve().as_posix())
        self.logger.info(f"NSFW classifier model loaded from {NSFW_CLASSIFIER_MODEL_PATH.resolve()}")

    def classify_toxic(self, text: str) -> Tuple[str, float]:
        self.logger.info('Classifying text for toxicity.')
        
        labels, confidence_arr = self._toxic_classifier.predict(text.replace('\n', ' '))
        label = labels[0]
        confidence = confidence_arr[0]
        self.logger.info(f'fasttext output:\nlabels:{labels}\nconfidence_arr:{confidence_arr}')

        final_label  = label[9:] if label.startswith('__label__') else label
        self.logger.info(f'Final label: {final_label}\nConfidence: {confidence}')

        return final_label, confidence

    def classify_nsfw(self, text: str) -> Tuple[str, float]:
        self.logger.info('Classifying text for NSFW content.')
        labels, confidence_arr = self._nsfw_classifier.predict(text.replace('\n', ' '))
        label = labels[0]
        confidence = confidence_arr[0]

        self.logger.info(f'fasttext output:\nlabels:{labels}\nconfidence_arr:{confidence_arr}')

        final_label  = label[9:] if label.startswith('__label__') else label
        self.logger.info(f'Final label: {final_label}\nConfidence: {confidence}')

        return final_label, confidence

    def classify_harmful(self, text: str) -> Tuple[bool, float]:
        self.logger.info('Classifying text for harmful content.')
        is_toxic, toxic_confidence = self.classify_toxic(text)
        is_nsfw, nsfw_confidence = self.classify_nsfw(text)

        final_label = is_toxic == 'toxic' or is_nsfw == 'nsfw'
        confidence = max(toxic_confidence, nsfw_confidence)
        self.logger.info(f'Final harmful label: {final_label}\nConfidence: {confidence}')

        return final_label, confidence

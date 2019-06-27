import spacy
from constants import DATA_DIR


class SpacyNER:
    def __init__(self):
        self._nlp = spacy.load("de_core_news_sm")

    def runNER(self, line):
        doc = self._nlp(line)
        return [[entity.label_, entity.text] for entity in doc.ents]

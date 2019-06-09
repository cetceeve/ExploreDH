import spacy

_nlp = spacy.load("de_core_news_sm")

def runNER(line):
    doc = _nlp(line)
    return [[entity.label_, entity] for entity in doc.ents]
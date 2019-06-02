import spacy

_nlp = spacy.load("de_core_news_sm")

def runNER(line):
    doc = _nlp(line)
    res = []

    for element in doc.ents:
        res.append([element.label_, element])

    return res
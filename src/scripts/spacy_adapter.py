import spacy

nlp = spacy.load("de_core_news_sm")

def runNER(line):
    doc = nlp(line)
    res = []

    for element in doc.ents:
        res.append([element.label_, element])

    return res
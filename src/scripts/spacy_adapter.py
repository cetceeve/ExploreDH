import spacy
from spacy_iwnlp import spaCyIWNLP
from constants import DATA_DIR

print("loading spacy...")
_nlp = spacy.load("de_core_news_sm")
_iwnlp = spaCyIWNLP(lemmatizer_path=DATA_DIR + "lemma/IWNLP.Lemmatizer_20181001.json")
_nlp.add_pipe(_iwnlp)


def runNER(line):
    doc = _nlp(line)
    return [[entity.label_, entity] for entity in doc.ents]


def findLemma(token):
    doc = _nlp(token)
    for token in doc:
        print("TOKEN: {}\t\tPOS: {}\tIWNLP:{}".format(token, token.pos_, token._.iwnlp_lemmas))

# @InProceedings{liebeck-conrad:2015:ACL-IJCNLP,
#   author    = {Liebeck, Matthias  and  Conrad, Stefan},
#   title     = {{IWNLP: Inverse Wiktionary for Natural Language Processing}},
#   booktitle = {Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 2: Short Papers)},
#   year      = {2015},
#   publisher = {Association for Computational Linguistics},
#   pages     = {414--418},
#   url       = {http://www.aclweb.org/anthology/P15-2068}
# }


def showSimilarity(tokens):
    docs = _nlp(tokens)
    for tOut in docs:
        for tIn in docs:
            print(tOut.text, tIn.text, tOut.similarity(tIn))

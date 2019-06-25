import nltk
import numpy as np

# this could motherfuking work


def getSimilarityMatrix(tokens):
    # return [nltk.edit_distance("annotieren", token) for token in tokens]
    for token in tokens:
        if nltk.edit_distance("historische Sprache", token) < 6:
            print(token)


def createWordMatrix(tokens):
    # TODO: generate letters array from dataset
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
               "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ä", "ö", "ü", " ", "*", "3", "-", "ß", "/", "4", "(", ")", ".", "1", "9", "5"]
    dictLetters = {k: v for v, k in enumerate(letters)}

    vecs = np.zeros((len(tokens), len(letters)), "int")
    for i, token in enumerate(tokens):
        for char in list(token.lower()):
            vecs[i][dictLetters[char]] += 1

    return vecs

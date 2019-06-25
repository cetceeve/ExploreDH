import nltk
import numpy as np

# this could motherfuking work


def getSimilarityMatrix(tokens):
    # return [nltk.edit_distance("annotieren", token) for token in tokens]
    for token in tokens:
        print(nltk.edit_distance("Augmented Reality", token))


def createWordMatrix(tokens):
    # TODO: generate letters array from dataset
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
               "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ä", "ö", "ü", " ", "*", "3", "-", "ß", "/", "4", "(", ")", ".", "1", "9", "5"]
    dictLetters = {k: v for v, k in enumerate(letters)}

    vecs = np.zeros((len(tokens), len(letters)), "int")
    for i, token in enumerate(tokens):
        for char in list(token.lower()):
            vecs[i][dictLetters[char]] += 1

    return vecs/np.linalg.norm(vecs, ord=2, axis=1, keepdims=True)


def computeCosineSimilarity(token, vectors):
    for vec in vectors:
        simi = np.dot(token, vec)
        print(simi)

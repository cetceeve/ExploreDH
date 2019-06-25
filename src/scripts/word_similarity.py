import nltk

# this could motherfuking work


def getSimilarityMatrix(tokens):
    # return [nltk.edit_distance("annotieren", token) for token in tokens]
    for token in tokens:
        if nltk.edit_distance("historische Sprache", token) < 6:
            print(token)

import nltk
import numpy as np
from Cistem import stem


class KeywordSimilarity:
    def __init__(self, dictKeywords):
        self.keywordLookUpTable = {}

        tokenMatrix = self._createTokenMatrix(dictKeywords.values())
        similarityMatrix = self._getCosineSimilarityMatrix(tokenMatrix)
        print(similarityMatrix)

    def _addStemToKeyword(self, keywords):
        for keyword in keywords:
            keyword["_stem"] = stem(keyword["text"])

    def _createTokenMatrix(self, keywords):
        self._addStemToKeyword(keywords)

        tokens = []
        dictLetters = {}
        for i, keyword in enumerate(keywords):
            # fill tokens and idLoopUpTable
            tokens.append(keyword["_stem"])
            self.keywordLookUpTable[i] = keyword["id"]

            # fill dict of letters
            for char in list(keyword["_stem"].lower()):
                if (char not in dictLetters):
                    dictLetters[char] = len(dictLetters)

        # create matrix
        vecs = np.zeros((len(tokens), len(dictLetters)), "int")
        for i, token in enumerate(tokens):
            for char in token:
                vecs[i][dictLetters[char]] += 1

        # normalize matrix
        return vecs/np.linalg.norm(vecs, ord=2, axis=1, keepdims=True)

    def _getCosineSimilarityMatrix(self, tokenMatrix):
        res = np.zeros((len(tokenMatrix), len(tokenMatrix)))
        for i, vecBase in enumerate(tokenMatrix):
            for j, vec in enumerate(tokenMatrix):
                res[i][j] = np.dot(vecBase, vec)
        return res

    def _levenshteinDistance(self, tokens):
        # return [nltk.edit_distance("annotieren", token) for token in tokens]
        for token in tokens:
            print(nltk.edit_distance("Augmented Reality", token))

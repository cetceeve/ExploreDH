import nltk
import numpy as np
from Cistem import stem


class KeywordSimilarity:
    SIMILARITY_THRESHOLD = 0.95
    LEVENSHTEIN_THRESHOLD = 3

    def __init__(self, _dictKeywords):
        self.dictKeywords = _dictKeywords
        self.keywordLookUpTable = {}
        self.similarityMatrix = self._getCosineSimilarityMatrix(self._getTokenMatrix(_dictKeywords.values()))

    def _addStemToKeyword(self, keywords):
        for keyword in keywords:
            keyword["_stem"] = stem(keyword["text"])

    def _getTokenMatrix(self, keywords):
        self._addStemToKeyword(keywords)

        tokens = []
        dictLetters = {}
        for i, keyword in enumerate(keywords):
            # fill tokens and idLoopUpTable
            tokens.append(keyword["_stem"])
            self.keywordLookUpTable[i] = keyword["id"]

            # fill dict of letters
            for char in keyword["_stem"].lower():
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
                if (j >= i):
                    continue
                res[i][j] = np.dot(vecBase, vec)
        return res

    def getSimilarKeywords(self):
        res = []
        for i, row in enumerate(self.similarityMatrix):
            similarTokens = [self.keywordLookUpTable[i]]

            for j, value in enumerate(row):
                if value > self.SIMILARITY_THRESHOLD:
                    if self._getLevenshteinDistance(i, j) < self.LEVENSHTEIN_THRESHOLD:
                        similarTokens.append(self.keywordLookUpTable[j])

            if len(similarTokens) > 1:
                res.append(tuple(similarTokens))
        return res

    def _getLevenshteinDistance(self, tokenID1, tokenID2):
        token1 = self.dictKeywords[self.keywordLookUpTable[tokenID1]]["_stem"]
        token2 = self.dictKeywords[self.keywordLookUpTable[tokenID2]]["_stem"]
        return nltk.edit_distance(token1, token2)

import sys_io_json as io
from itertools import chain


class OrgaNetwork:
    def __init__(self, _dictArticle, _dictPerson, _dictOrga):
        self.dictArticle = _dictArticle
        self.dictPerson = _dictPerson
        self.dictOrga = _dictOrga

    def getConnections(self):
        conns = [self._connsInArticle(article) for article in self.dictArticle.values()]
        flattend = list(chain.from_iterable(conns))
        # remove duplicate connections independent of direction
        connDict = {hash(conn[0]) + hash(conn[1]): conn for conn in flattend}
        return tuple(map(self._replaceOrgaIDTupleWithCoordinates, connDict.values()))

    def _connsInArticle(self, article):
        # go from person to orga and remove duplicates
        involvedOrgas = list(dict.fromkeys(map(self._replacePersonIDWithOrgaID, article["authors"])))
        if len(involvedOrgas) < 2:
            return []

        # connections = one directional dense graph (no self connecting + no backtracking)
        iterator = range(len(involvedOrgas))
        return [(involvedOrgas[i], involvedOrgas[j]) for i in iterator for j in iterator[i + 1:]]

    def _replacePersonIDWithOrgaID(self, personID):
        return self.dictPerson[personID]["orga"]

    def _replaceOrgaIDTupleWithCoordinates(self, orgaIDTuple):
        return tuple({"id": orgaID, "lat": self.dictOrga[orgaID]["lat"], "lon": self.dictOrga[orgaID]["lon"]} for orgaID in orgaIDTuple)

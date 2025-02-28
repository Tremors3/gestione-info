
## Docs
# https://lucene.apache.org/core/3_5_0/api/core/org/apache/lucene/search/DefaultSimilarity.html
# https://lucene.apache.org/core/9_4_1/core/org/apache/lucene/search/similarities/
# https://lucene.apache.org/core/9_4_1/core/org/apache/lucene/search/similarities/ClassicSimilarity.html

## Wikipedia
# https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency%E2%80%93inverse_document_frequency

from org.apache.lucene.search import BooleanClause, BooleanQuery, Explanation, PhraseQuery, TermQuery
from org.apache.lucene.search.similarities import SimilarityBase, ClassicSimilarity
from org.apache.pylucene.search.similarities import PythonClassicSimilarity

from math import sqrt, log2, log10

class TFLN_PIDF(PythonClassicSimilarity):
    """ TF Log Normalization-Probabilistic IDF """

    def lengthNorm(self, numTerms):
        return 1 / sqrt(numTerms)

    def tf(self, freq):
        if freq > 0.0: return 1 + log10(freq)
        return freq
    
    def sloppyFreq(self, distance):
        return sqrt(distance) / (distance + 1)

    def idf(self, docFreq, numDocs):
        return log2((numDocs - docFreq + 1) / docFreq + 1) + 1

    def idfExplain(self, collectionStats, termStats):
        return Explanation.match(self.idf(termStats.docFreq(), collectionStats.docCount()), "IDF", [])

# class VSM_DEFAULT(PythonClassicSimilarity):

#     def lengthNorm(self, numTerms):
#         return 1 / sqrt(numTerms)

#     def tf(self, freq):
#         return sqrt(freq)

#     def sloppyFreq(self, distance):
#         return 1 / (distance + 1)

#     def idf(self, docFreq, numDocs):
#         return log((numDocs+1)/(docFreq+1)) + 1 

#     def idfExplain(self, collectionStats, termStats):
#         return Explanation.match(self.idf(termStats.docFreq(), collectionStats.docCount()), "IDF", [])
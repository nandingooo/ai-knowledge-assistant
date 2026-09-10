from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class RankedDocument:
    document: object
    score: float


class Retriever:
    """Lightweight in-memory retrieval over persisted documents."""

    def rank(self, query: str, documents: list, top_k: int = 3) -> list[RankedDocument]:
        if not documents:
            return []

        corpus = [doc.content for doc in documents]
        vectorizer = TfidfVectorizer(stop_words="english")
        matrix = vectorizer.fit_transform(corpus + [query])

        scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
        ranked_indices = scores.argsort()[::-1][:top_k]

        return [
            RankedDocument(document=documents[i], score=float(scores[i]))
            for i in ranked_indices
            if scores[i] > 0
        ]

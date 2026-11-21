"""
store.py - keeps the uploaded documents in memory and finds the chunks that match a question.

We use TF-IDF vectors (Day 2, Lesson 02) for retrieval: free, fast, offline and easy to understand.
The same class could later use embeddings and a real vector database (Day 2, Lesson 08).

Note: everything is kept in memory, so it is lost when the server restarts. That is fine for a demo.
"""

import re

from sklearn.feature_extraction.text import TfidfVectorizer

STOP_WORDS = {
    "the", "a", "an", "is", "are", "of", "to", "for", "and", "or", "what", "how", "in", "on", "if",
    "i", "my", "do", "does", "can", "it", "much", "many", "who", "when", "which", "why", "with", "be",
}


def simple_stem(word):
    """Very small stemmer: 'fees' -> 'fee', 'books' -> 'book', 'classes' -> 'class'."""
    if len(word) > 4 and word.endswith("es") and word[-3] in "sxz":
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def tokens(text):
    """Split text into lowercase, stemmed words without stop words."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [simple_stem(w) for w in words if w not in STOP_WORDS and len(w) > 1]


def keywords(text):
    """The set of important words in a text."""
    return set(tokens(text))


class DocumentStore:
    def __init__(self):
        self.chunks = []  # list of {"source": filename, "text": chunk}
        self._vectorizer = None
        self._matrix = None

    # ---- adding and removing -------------------------------------------------
    def add(self, filename, chunks):
        self.chunks = [c for c in self.chunks if c["source"] != filename]  # replace an older upload
        self.chunks += [{"source": filename, "text": text} for text in chunks]
        self._rebuild()

    def clear(self):
        self.chunks = []
        self._rebuild()

    def list_documents(self):
        counts = {}
        for c in self.chunks:
            counts[c["source"]] = counts.get(c["source"], 0) + 1
        return [{"filename": name, "chunks": n} for name, n in counts.items()]

    def get_text(self, filename=None):
        selected = [c["text"] for c in self.chunks if filename is None or c["source"] == filename]
        return "\n".join(selected)

    def get_chunks(self, filename=None):
        return [c for c in self.chunks if filename is None or c["source"] == filename]

    # ---- searching -----------------------------------------------------------
    def _rebuild(self):
        if self.chunks:
            self._vectorizer = TfidfVectorizer(tokenizer=tokens, token_pattern=None, lowercase=False)
            self._matrix = self._vectorizer.fit_transform([c["text"] for c in self.chunks])
        else:
            self._vectorizer, self._matrix = None, None

    def search(self, question, top_k=3):
        """Return the top_k chunks most similar to the question, each with a score from 0 to 1."""
        if not self.chunks:
            return []
        question_vector = self._vectorizer.transform([question])
        scores = (self._matrix @ question_vector.T).toarray().ravel()
        best = scores.argsort()[::-1][:top_k]
        return [{**self.chunks[i], "score": round(float(scores[i]), 3)} for i in best if scores[i] > 0]


# One shared store for the whole app
store = DocumentStore()

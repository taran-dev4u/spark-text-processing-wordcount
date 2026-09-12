"""Text processing, MapReduce tokenization, inverted indexing, and TF-IDF modules."""

from __future__ import annotations

import math
import re
import string
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence

DEFAULT_STOPWORDS = frozenset({
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it",
    "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
    "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
    "they're", "they've", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're",
    "we've", "were", "weren't", "what", "what's", "when", "when's", "where",
    "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with",
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
    "your", "yours", "yourself", "yourselves",
})


class TextProcessor:
    """Preprocesses raw text documents into normalized token streams."""

    def __init__(
        self,
        lowercase: bool = True,
        min_length: int = 1,
        stopwords: set[str] | frozenset[str] | None = None,
        strip_punctuation: bool = True,
    ) -> None:
        self.lowercase = lowercase
        self.min_length = min_length
        self.stopwords = stopwords if stopwords is not None else set()
        self.strip_punctuation = strip_punctuation
        self._punct_trans = str.maketrans("", "", string.punctuation)

    def tokenize(self, text: str) -> list[str]:
        """Tokenize input text into normalized string tokens."""
        if not text:
            return []

        if self.lowercase:
            text = text.lower()

        if self.strip_punctuation:
            text = text.translate(self._punct_trans)

        tokens = re.findall(r"\b[a-zA-Z0-9_-]+\b", text)

        filtered = [
            tok
            for tok in tokens
            if len(tok) >= self.min_length and tok not in self.stopwords
        ]
        return filtered

    def generate_ngrams(self, tokens: Sequence[str], n: int = 2) -> list[tuple[str, ...]]:
        """Generate contiguous n-grams from a sequence of tokens."""
        if n < 1:
            raise ValueError("n-gram length must be at least 1")
        if len(tokens) < n:
            return []
        return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


class WordCountAggregator:
    """MapReduce word count and corpus frequency analyzer."""

    def __init__(self, processor: TextProcessor | None = None) -> None:
        self.processor = processor or TextProcessor()

    def count_lines(self, lines: Iterable[str]) -> Counter[str]:
        """Aggregate token counts across an iterable of lines/documents."""
        counter: Counter[str] = Counter()
        for line in lines:
            tokens = self.processor.tokenize(line)
            counter.update(tokens)
        return counter

    def top_k(self, counts: Mapping[str, int] | Counter[str], k: int = 10) -> list[tuple[str, int]]:
        """Return the top-k most frequent terms."""
        if isinstance(counts, Counter):
            return counts.most_common(k)
        counter = Counter(counts)
        return counter.most_common(k)

    def compute_stats(self, counts: Mapping[str, int] | Counter[str]) -> dict[str, int | float]:
        """Compute corpus summary metrics."""
        total_tokens = sum(counts.values())
        unique_vocab = len(counts)
        hapax_legomena = sum(1 for count in counts.values() if count == 1)
        max_freq = max(counts.values()) if counts else 0
        mean_freq = (total_tokens / unique_vocab) if unique_vocab > 0 else 0.0

        return {
            "total_tokens": total_tokens,
            "unique_vocab": unique_vocab,
            "hapax_legomena": hapax_legomena,
            "max_frequency": max_freq,
            "mean_frequency": round(mean_freq, 2),
        }


class InvertedIndex:
    """Inverted index mapping terms to document IDs and token offsets."""

    def __init__(self, processor: TextProcessor | None = None) -> None:
        self.processor = processor or TextProcessor()
        self.index: dict[str, set[str]] = defaultdict(set)
        self.positions: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
        self.doc_count: int = 0

    def add_document(self, doc_id: str, content: str) -> None:
        """Index a single document by its identifier and textual content."""
        tokens = self.processor.tokenize(content)
        for pos, token in enumerate(tokens):
            self.index[token].add(doc_id)
            self.positions[token][doc_id].append(pos)
        self.doc_count += 1

    def search(self, terms: Sequence[str], operator: str = "AND") -> set[str]:
        """Query the index for matching document IDs with boolean logic."""
        if not terms:
            return set()

        norm_terms = [t.lower() if self.processor.lowercase else t for t in terms]
        postings = [self.index.get(term, set()) for term in norm_terms]

        if not postings:
            return set()

        op = operator.upper()
        if op == "AND":
            result = set(postings[0])
            for p in postings[1:]:
                result.intersection_update(p)
            return result
        elif op == "OR":
            result = set()
            for p in postings:
                result.update(p)
            return result
        else:
            raise ValueError(f"Unsupported operator: {operator}. Use 'AND' or 'OR'.")


class TFIDFCalculator:
    """Computes Term Frequency - Inverse Document Frequency matrices."""

    def __init__(self, processor: TextProcessor | None = None) -> None:
        self.processor = processor or TextProcessor()

    def compute_tf(self, tokens: Sequence[str]) -> dict[str, float]:
        """Compute relative term frequency within a document."""
        if not tokens:
            return {}
        counts = Counter(tokens)
        total = len(tokens)
        return {term: count / total for term, count in counts.items()}

    def compute_idf(self, corpus: Sequence[Sequence[str]]) -> dict[str, float]:
        """Compute smoothed inverse document frequency across a tokenized corpus."""
        n_docs = len(corpus)
        if n_docs == 0:
            return {}

        df: Counter[str] = Counter()
        for doc_tokens in corpus:
            unique_terms = set(doc_tokens)
            df.update(unique_terms)

        # Standard smooth IDF formula: ln((1 + N) / (1 + df)) + 1
        return {
            term: math.log((1.0 + n_docs) / (1.0 + freq)) + 1.0
            for term, freq in df.items()
        }

    def compute_tfidf(self, tokens: Sequence[str], idf: Mapping[str, float]) -> dict[str, float]:
        """Compute TF-IDF weights for a document given a precalculated IDF map."""
        tf = self.compute_tf(tokens)
        return {
            term: tf_val * idf.get(term, 1.0)
            for term, tf_val in tf.items()
        }

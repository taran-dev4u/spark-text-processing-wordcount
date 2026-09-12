import pytest

from spark_text.pipeline import (
    TextProcessor,
    WordCountAggregator,
)


def test_text_processor_basic():
    proc = TextProcessor(lowercase=True, strip_punctuation=True)
    text = "Distributed Systems: MapReduce, Spark, and Beyond!"
    tokens = proc.tokenize(text)
    assert "distributed" in tokens
    assert "systems" in tokens
    assert "mapreduce" in tokens
    assert "spark" in tokens
    assert "beyond" in tokens


def test_text_processor_stopwords():
    proc = TextProcessor(lowercase=True, stopwords={"and", "the", "to", "in"})
    text = "The quick brown fox jumps to the lazy dog in and out"
    tokens = proc.tokenize(text)
    assert "the" not in tokens
    assert "and" not in tokens
    assert "to" not in tokens
    assert "in" not in tokens
    assert "quick" in tokens
    assert "fox" in tokens


def test_generate_ngrams():
    proc = TextProcessor()
    tokens = ["data", "intensive", "computing", "systems"]
    bigrams = proc.generate_ngrams(tokens, n=2)
    assert len(bigrams) == 3
    assert bigrams[0] == ("data", "intensive")
    assert bigrams[2] == ("computing", "systems")

    with pytest.raises(ValueError):
        proc.generate_ngrams(tokens, n=0)


def test_word_count_aggregator():
    proc = TextProcessor(lowercase=True)
    agg = WordCountAggregator(proc)
    lines = [
        "Spark processes data in memory",
        "MapReduce processes data on disk",
        "Spark and MapReduce solve big data challenges",
    ]
    counts = agg.count_lines(lines)
    assert counts["data"] == 3
    assert counts["processes"] == 2
    assert counts["spark"] == 2
    assert counts["mapreduce"] == 2

    top3 = agg.top_k(counts, k=3)
    assert len(top3) == 3
    assert top3[0][0] == "data"
    assert top3[0][1] == 3

    stats = agg.compute_stats(counts)
    assert stats["total_tokens"] > 0
    assert stats["unique_vocab"] > 0
    assert stats["hapax_legomena"] > 0

from spark_text.pipeline import TextProcessor, TFIDFCalculator


def test_tfidf_computation():
    calc = TFIDFCalculator(TextProcessor())
    doc1 = ["spark", "fast", "cluster", "computing"]
    doc2 = ["spark", "resilient", "distributed", "dataset"]
    doc3 = ["hadoop", "mapreduce", "disk", "storage"]

    corpus = [doc1, doc2, doc3]
    idf = calc.compute_idf(corpus)

    # "spark" appears in 2 documents, "computing" appears in 1
    assert idf["computing"] > idf["spark"]

    tfidf_doc1 = calc.compute_tfidf(doc1, idf)
    assert tfidf_doc1["computing"] > tfidf_doc1["spark"]
    assert tfidf_doc1["fast"] > 0


def test_tfidf_empty_corpus():
    calc = TFIDFCalculator()
    assert calc.compute_idf([]) == {}
    assert calc.compute_tf([]) == {}

from spark_text.pipeline import InvertedIndex, TextProcessor


def test_inverted_index_indexing_and_search():
    index = InvertedIndex(TextProcessor())
    index.add_document("doc1", "Apache Spark is a unified analytics engine for large-scale data processing.")
    index.add_document("doc2", "MapReduce is a programming model for processing big data sets with a parallel algorithm.")
    index.add_document("doc3", "Hadoop Distributed File System HDFS stores data across commodity hardware.")

    # Single term query
    res = index.search(["analytics"])
    assert res == {"doc1"}

    # Boolean AND query
    res_and = index.search(["processing", "data"], operator="AND")
    assert res_and == {"doc1", "doc2"}

    # Boolean OR query
    res_or = index.search(["spark", "hdfs"], operator="OR")
    assert res_or == {"doc1", "doc3"}

    # Nonexistent term
    assert index.search(["quantum"]) == set()


def test_inverted_index_empty_query():
    index = InvertedIndex()
    assert index.search([]) == set()

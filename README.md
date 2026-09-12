# Distributed Text Processing & MapReduce Analytics

Parallel text tokenization, inverted indexing, TF-IDF calculation, and graph analytics pipelines built with PySpark and streaming MapReduce abstractions.

## Architecture & Modules

The repository provides a Python package (`spark_text`) for text mining, document retrieval, and network graph analysis:

- `spark_text.pipeline.TextProcessor`: Normalizes strings, strips punctuation, handles custom stopword sets, and extracts n-grams.
- `spark_text.pipeline.WordCountAggregator`: Streaming MapReduce word frequency aggregation with corpus metrics (vocabulary size, hapax legomena, frequency distributions).
- `spark_text.pipeline.InvertedIndex`: Positional and term-level inverted indexing supporting boolean `AND` / `OR` document queries.
- `spark_text.pipeline.TFIDFCalculator`: Smoothed term frequency - inverse document frequency computation across document sets.
- `spark_text.graph`: Random weighted network generation, directed adjacency structures, and iterative power-method PageRank.
- `spark_text.cli`: Command-line interface with `count`, `index`, and `pagerank` subcommands.

## Installation

Requires Python 3.9+.

```bash
git clone https://github.com/taran-dev4u/spark-text-processing-wordcount.git
cd spark-text-processing-wordcount
pip install -e .
```

To install test dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Python API

```python
from spark_text.pipeline import TextProcessor, WordCountAggregator, DEFAULT_STOPWORDS

processor = TextProcessor(lowercase=True, stopwords=DEFAULT_STOPWORDS)
aggregator = WordCountAggregator(processor)

lines = [
    "Apache Spark provides in-memory cluster computing.",
    "MapReduce processes datasets across distributed nodes.",
]

counts = aggregator.count_lines(lines)
top_words = aggregator.top_k(counts, k=5)
print(top_words)
```

### Inverted Indexing & Search

```python
from spark_text.pipeline import InvertedIndex, TextProcessor

index = InvertedIndex(TextProcessor())
index.add_document("doc1", "Distributed storage and cluster computing")
index.add_document("doc2", "Fault tolerant distributed systems")

matches = index.search(["distributed", "computing"], operator="AND")
print(matches)  # {'doc1'}
```

### Command-Line Interface

Run word count frequency analysis with stopword filtering on a text file:

```bash
spark-text count --input spark-dic-implementation/book1.txt --top-k 10 --stopwords
```

Output corpus statistics and frequency table as structured JSON:

```bash
spark-text count --input spark-dic-implementation/book1.txt --top-k 5 --stopwords --json
```

Query multiple documents using the inverted index:

```bash
spark-text index --files spark-dic-implementation/book1.txt spark-dic-implementation/book2.txt --query emperor voyage --operator AND
```

Run iterative PageRank simulation:

```bash
spark-text pagerank --nodes 20 --damping 0.85 --top-k 5
```

## Running Spark Notebooks & Jobs

For distributed cluster execution via Apache Spark:

- `spark-dic-implementation/spark_text_processing_dic.ipynb`: PySpark RDD transformations, shuffle metrics, and execution graph evaluation.
- Benchmark corpora are located in `spark-dic-implementation/` (`book1.txt`, `book2.txt`).

Submit a standalone Spark batch job:

```bash
spark-submit \
    --master local[*] \
    --executor-memory 2G \
    spark-dic-implementation/code_2.py
```

## Testing

Run the test suite covering tokenization, indexing, TF-IDF, graph algorithms, and CLI subcommands:

```bash
pytest tests/ -v
```

Linting check:

```bash
ruff check .
```

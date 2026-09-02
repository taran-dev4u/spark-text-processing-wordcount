# Distributed Text Processing & MapReduce with PySpark

Big data processing and text analytics pipelines developed for CSE 587 (Data-Intensive Computing). Implements parallel text tokenization, stopword filtering, inverted index creation, and word frequency analysis using Apache Spark RDDs and Spark SQL.

## Features & Implementation

- **Distributed Word Count:** RDD `flatMap` tokenization, lowercase/punctuation cleaning, and `reduceByKey` aggregations across worker nodes.
- **Stopword Filtering:** Broadcast variables sharing stopword sets to executors to minimize network shuffle overhead.
- **Inverted Indexing:** Mapping terms to document locations and line offsets for search indexing.

## Structure

- `spark-dic-implementation/code_2.py` — PySpark transformation pipeline.
- `spark-dic-implementation/` — Benchmark corpora (`book1.txt`, `book2.txt`).
- `dic_coursework_and_problem_specs/` — Course project specifications (`487 Phase 1 & 2 Description.pdf`) and report (`dmql_taranmam_50604177.pdf`).

## Running the Spark Job

```bash
spark-submit \
    --master local[*] \
    --executor-memory 2G \
    spark-dic-implementation/code_2.py
```

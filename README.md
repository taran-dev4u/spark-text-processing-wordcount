# Distributed Text Processing, Word Frequency & MapReduce Pipeline with PySpark

[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.x-red.svg)](https://spark.apache.org/)
[![Python](https://img.shields.io/badge/PySpark-Python%20API-blue.svg)](https://spark.apache.org/docs/latest/api/python/)
[![Big Data](https://img.shields.io/badge/Big%20Data-Distributed%20Computing-orange.svg)](https://hadoop.apache.org/)
[![University](https://img.shields.io/badge/Institution-University%20at%20Buffalo%20(UB)-red.svg)](https://www.buffalo.edu/)
[![Course](https://img.shields.io/badge/Course-CSE%20587%20Data--Intensive%20Computing-purple.svg)](https://engineering.buffalo.edu/computer-science-engineering.html)

---

## 📌 Executive Summary & Academic Context

This repository contains the distributed big data processing and large-scale text analytics pipeline developed for **CSE 587 (Data-Intensive Computing - DIC)** at the **University at Buffalo (UB)**.

The project addresses the challenges of parallel text tokenization, inverted index generation, stopword filtering, term frequency-inverse document frequency (TF-IDF), and n-gram extraction across massive document corpora using Apache Spark's Resilient Distributed Datasets (RDDs) and Spark SQL DataFrames.

```
  +------------------+     flatMap(tokenize)     +-------------------+
  | Corpus Documents | ------------------------> | Words / Tokens    |
  +------------------+                           +-------------------+
                                                           |
                                                filter(stopword removal)
                                                           v
  +------------------+     reduceByKey(sum)      +-------------------+
  | Top-K Frequency  | <------------------------ | (Word, 1) Pairs   |
  | & Inverted Index |                           +-------------------+
  +------------------+
```

---

## 🚀 Key Modules & Big Data Pipelines

### 1. RDD-Based Distributed Word Frequency Analysis
- **Tokenization & Normalization:** Distributed regex parsing, lowercasing, punctuation stripping, and whitespace handling across clustered worker nodes.
- **Parallel Stopword Elimination:** Broadcast variables distributing global stopword sets to all executors, minimizing network shuffling overhead.
- **Aggregation via `reduceByKey` vs `groupByKey`:** Optimized memory usage and network serialization using associative in-mapper combiner transformations.

### 2. Inverted Indexing & N-Gram Extraction
- **Inverted Index Construction:** Mapping vocabulary terms to document occurrence lists and line offsets for rapid full-text search indexing.
- **Bi-gram and Tri-gram Collocations:** Sliding window transformations capturing co-occurring phrase semantics.

---

## 📂 Repository Structure

```
spark-text-processing-wordcount/
├── spark-dic-implementation/        # PySpark jobs and mapper/reducer logic
│   ├── code_2.py                    # Distributed word count and text transformation pipeline
│   ├── book1.txt                    # Benchmark input corpus volume 1
│   └── book2.txt                    # Benchmark input corpus volume 2
├── dmql-homework-sql/               # Supplementary database query assignments
├── project-files/                   # Assignment report and execution logs
└── README.md                        # Documentation
```

---

## 🛠️ Execution Instructions

```bash
# Submit Spark job locally or to a cluster
spark-submit \
    --master local[*] \
    --executor-memory 2G \
    spark-dic-implementation/code_2.py
```

---

## 👨‍💻 Author & Academic Attribution
- **Author:** Taran Mamidala
- **Program:** Master of Science in Computer Science (MS CS)
- **Institution:** University at Buffalo, The State University of New York (UB)
- **Course:** CSE 587 — Data-Intensive Computing (DIC)

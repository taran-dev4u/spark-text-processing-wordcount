# Spark Text Processing Word Count

Distributed text-processing project using Spark-style transformations for word count, normalization, stopword handling, and frequency analysis.

## Overview

This project keeps the classic distributed word-count exercise but names it clearly around Spark and text processing. It is useful as a compact data-engineering example because it shows loading, tokenizing, mapping, reducing, sorting, and interpreting output.

The scope is intentionally small, but it demonstrates the core pattern behind many larger distributed text pipelines.

## Problem

Raw text frequency output is noisy when case, punctuation, and stop words are not handled. A useful pipeline needs both the distributed processing pattern and the preprocessing decisions that make the result readable.

## Scope

- Basic distributed word count
- Case normalization and punctuation handling
- Stopword filtering
- Sorted frequency output and interpretation

## Approach

- Loaded multiple text files as one corpus
- Tokenized text into countable terms
- Reduced terms into frequency counts
- Compared raw and cleaned outputs

## Existing Work

- Report covering basic and extended word-count implementation
- Analysis notes for frequency output and preprocessing impact

## Contribution

Implemented and analyzed the text-processing workflow with basic and extended preprocessing.

## Skills

- Apache Spark
- RDDs
- Text processing
- Python
- Data engineering

## Next Update

- Add scripts and sample inputs
- Add expected output files
- Document preprocessing changes and their effect on results

The implementation files are stored separately and will be added after the source folders are reviewed and organized.

## Topics

`spark`, `text-processing`, `wordcount`, `data-engineering`, `python`

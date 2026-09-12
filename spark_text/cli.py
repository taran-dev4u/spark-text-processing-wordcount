"""Command-line interface for text processing, MapReduce analytics, and graph tasks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from spark_text.graph import (
    compute_pagerank,
    generate_edge_weights,
)
from spark_text.pipeline import (
    DEFAULT_STOPWORDS,
    InvertedIndex,
    TextProcessor,
    WordCountAggregator,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="spark-text",
        description="Text processing, MapReduce word counting, and graph analytics CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Word count subcommand
    wc_parser = subparsers.add_parser("count", help="Count words and analyze corpus frequency")
    wc_parser.add_argument("--input", "-i", required=True, help="Input text file path")
    wc_parser.add_argument("--top-k", "-k", type=int, default=10, help="Number of top words to display")
    wc_parser.add_argument("--stopwords", action="store_true", help="Filter standard English stopwords")
    wc_parser.add_argument("--min-len", type=int, default=1, help="Minimum token character length")
    wc_parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    # Inverted index subcommand
    idx_parser = subparsers.add_parser("index", help="Build and query an inverted index")
    idx_parser.add_argument("--files", "-f", nargs="+", required=True, help="Document files to index")
    idx_parser.add_argument("--query", "-q", nargs="+", required=True, help="Search terms")
    idx_parser.add_argument("--operator", choices=["AND", "OR"], default="AND", help="Boolean match logic")
    idx_parser.add_argument("--json", action="store_true", help="Output matches in JSON format")

    # Graph PageRank subcommand
    graph_parser = subparsers.add_parser("pagerank", help="Run PageRank simulation on synthetic or edge data")
    graph_parser.add_argument("--nodes", "-n", type=int, default=20, help="Number of synthetic nodes")
    graph_parser.add_argument("--damping", type=float, default=0.85, help="PageRank damping factor")
    graph_parser.add_argument("--top-k", type=int, default=5, help="Top ranked nodes to output")
    graph_parser.add_argument("--json", action="store_true", help="Output ranks in JSON format")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "count":
        in_path = Path(args.input)
        if not in_path.exists():
            sys.stderr.write(f"Error: input file not found: {in_path}\n")
            return 1

        stopwords = DEFAULT_STOPWORDS if args.stopwords else None
        processor = TextProcessor(min_length=args.min_len, stopwords=stopwords)
        aggregator = WordCountAggregator(processor)

        with in_path.open("r", encoding="utf-8", errors="replace") as f:
            counts = aggregator.count_lines(f)

        top_words = aggregator.top_k(counts, k=args.top_k)
        stats = aggregator.compute_stats(counts)

        if args.json:
            out = {
                "file": str(in_path),
                "stats": stats,
                "top_words": [{"word": w, "count": c} for w, c in top_words],
            }
            print(json.dumps(out, indent=2))
        else:
            print(f"=== Corpus Analysis: {in_path.name} ===")
            print(f"Total tokens: {stats['total_tokens']:,} | Vocabulary size: {stats['unique_vocab']:,}")
            print(f"Top {len(top_words)} words:")
            for rank, (word, count) in enumerate(top_words, 1):
                print(f"  {rank:2d}. {word:16s} {count:,}")

    elif args.command == "index":
        processor = TextProcessor(stopwords=DEFAULT_STOPWORDS)
        index = InvertedIndex(processor)

        for filepath in args.files:
            p = Path(filepath)
            if p.exists():
                text = p.read_text(encoding="utf-8", errors="replace")
                index.add_document(p.name, text)

        matches = index.search(args.query, operator=args.operator)

        if args.json:
            print(json.dumps({
                "query": args.query,
                "operator": args.operator,
                "matches": sorted(matches),
            }, indent=2))
        else:
            print(f"Query: {' '.join(args.query)} [{args.operator}]")
            print(f"Matching documents ({len(matches)}):")
            for m in sorted(matches):
                print(f"  - {m}")

    elif args.command == "pagerank":
        edges = generate_edge_weights(args.nodes, seed=42)
        pr = compute_pagerank(edges, damping=args.damping)
        sorted_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)[: args.top_k]

        if args.json:
            print(json.dumps({
                "nodes": args.nodes,
                "damping": args.damping,
                "top_ranked": [{"node": n, "rank": round(r, 6)} for n, r in sorted_pr],
            }, indent=2))
        else:
            print(f"=== PageRank ({args.nodes} nodes, damping={args.damping}) ===")
            for rank, (node, score) in enumerate(sorted_pr, 1):
                print(f"  {rank:2d}. Node {node:3d}: {score:.6f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Graph analytics and network topology algorithms for distributed systems."""

from __future__ import annotations

import random
from collections import defaultdict
from collections.abc import Sequence


def generate_edge_weights(
    num_nodes: int,
    min_weight: int = 1,
    max_weight: int = 10,
    seed: int | None = 42,
) -> list[tuple[int, int, int]]:
    """Generate complete upper-triangular edges with random integer weights."""
    if seed is not None:
        random.seed(seed)

    edges: list[tuple[int, int, int]] = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = random.randint(min_weight, max_weight)
            edges.append((i, j, weight))
    return edges


def generate_directed_adjacencies(
    num_nodes: int,
    max_links: int = 10,
    seed: int | None = 42,
) -> dict[int, list[int]]:
    """Generate random directed adjacency lists for web-graph simulations."""
    if seed is not None:
        random.seed(seed)

    link_data: dict[int, list[int]] = {}
    for node in range(num_nodes):
        num_links = random.randint(1, min(max_links, max(1, num_nodes - 1)))
        candidates = [n for n in range(num_nodes) if n != node]
        links = random.sample(candidates, min(num_links, len(candidates)))
        link_data[node] = links
    return link_data


def compute_pagerank(
    edges: Sequence[tuple[int, int] | tuple[int, int, int]],
    damping: float = 0.85,
    max_iter: int = 100,
    tol: float = 1e-6,
) -> dict[int, float]:
    """Iterative power-method PageRank on a directed graph."""
    # Build outbound adjacency list and extract all nodes
    nodes: set[int] = set()
    out_links: dict[int, list[int]] = defaultdict(list)

    for edge in edges:
        u, v = edge[0], edge[1]
        nodes.add(u)
        nodes.add(v)
        out_links[u].append(v)

    n = len(nodes)
    if n == 0:
        return {}

    # Initialize uniform probability distribution
    pr: dict[int, float] = {node: 1.0 / n for node in nodes}

    for _ in range(max_iter):
        next_pr: dict[int, float] = {node: (1.0 - damping) / n for node in nodes}

        # Dead-end handling: nodes with 0 out-degree distribute rank uniformly
        dangling_sum = sum(pr[node] for node in nodes if len(out_links[node]) == 0)
        dangling_contrib = (damping * dangling_sum) / n

        for node in nodes:
            next_pr[node] += dangling_contrib

        # Standard PageRank link distribution
        for u in nodes:
            links = out_links[u]
            if links:
                share = (damping * pr[u]) / len(links)
                for v in links:
                    next_pr[v] += share

        # Check for convergence (L1 norm)
        diff = sum(abs(next_pr[node] - pr[node]) for node in nodes)
        pr = next_pr
        if diff < tol:
            break

    return pr


def node_degree_centrality(
    edges: Sequence[tuple[int, int] | tuple[int, int, int]],
) -> dict[str, dict[int, int]]:
    """Compute in-degree and out-degree counts for all observed nodes."""
    in_degree: dict[int, int] = defaultdict(int)
    out_degree: dict[int, int] = defaultdict(int)
    nodes: set[int] = set()

    for edge in edges:
        u, v = edge[0], edge[1]
        nodes.add(u)
        nodes.add(v)
        out_degree[u] += 1
        in_degree[v] += 1

    # Ensure all nodes exist in both dicts
    for node in nodes:
        in_degree.setdefault(node, 0)
        out_degree.setdefault(node, 0)

    return {
        "in_degree": dict(in_degree),
        "out_degree": dict(out_degree),
    }

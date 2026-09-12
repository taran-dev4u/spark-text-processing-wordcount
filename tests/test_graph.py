import pytest

from spark_text.graph import (
    compute_pagerank,
    generate_directed_adjacencies,
    generate_edge_weights,
    node_degree_centrality,
)


def test_generate_edge_weights():
    nodes = 10
    edges = generate_edge_weights(nodes, min_weight=1, max_weight=5, seed=42)
    expected_count = nodes * (nodes - 1) // 2
    assert len(edges) == expected_count
    for u, v, w in edges:
        assert u < v
        assert 1 <= w <= 5


def test_generate_directed_adjacencies():
    nodes = 15
    adj = generate_directed_adjacencies(nodes, max_links=5, seed=42)
    assert len(adj) == nodes
    for u, links in adj.items():
        assert u not in links
        assert len(links) <= 5


def test_compute_pagerank():
    # Triangle graph: 0 -> 1, 1 -> 2, 2 -> 0
    edges = [(0, 1), (1, 2), (2, 0)]
    ranks = compute_pagerank(edges, damping=0.85, max_iter=50)
    assert len(ranks) == 3
    # By symmetry, all nodes in a cycle should have equal PageRank
    assert pytest.approx(ranks[0], rel=1e-3) == ranks[1]
    assert pytest.approx(ranks[1], rel=1e-3) == ranks[2]
    # Sum of ranks should equal 1.0
    assert pytest.approx(sum(ranks.values()), rel=1e-3) == 1.0


def test_node_degree_centrality():
    edges = [(0, 1), (0, 2), (1, 2)]
    centrality = node_degree_centrality(edges)
    assert centrality["out_degree"][0] == 2
    assert centrality["in_degree"][2] == 2
    assert centrality["out_degree"][2] == 0

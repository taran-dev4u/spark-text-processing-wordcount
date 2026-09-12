import json

from spark_text.cli import main


def test_cli_count(tmp_path, capsys):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("hello world hello data processing world", encoding="utf-8")

    ret = main(["count", "--input", str(sample_file), "--top-k", "2", "--json"])
    assert ret == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["stats"]["total_tokens"] == 6
    assert data["top_words"][0]["count"] == 2


def test_cli_index(tmp_path, capsys):
    f1 = tmp_path / "doc1.txt"
    f2 = tmp_path / "doc2.txt"
    f1.write_text("distributed cluster computation", encoding="utf-8")
    f2.write_text("single machine computation", encoding="utf-8")

    ret = main(["index", "--files", str(f1), str(f2), "--query", "computation", "--json"])
    assert ret == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert len(data["matches"]) == 2


def test_cli_pagerank(capsys):
    ret = main(["pagerank", "--nodes", "10", "--top-k", "3", "--json"])
    assert ret == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert len(data["top_ranked"]) == 3

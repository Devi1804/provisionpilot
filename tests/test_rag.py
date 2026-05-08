from rag.search import search


def test_rag_finds_planted_known_issue():
    results = search("bond0 dhcp regression", k=3)
    assert any("bond0" in r["text"].lower() for r in results)
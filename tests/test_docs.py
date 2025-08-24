from pathlib import Path


def test_docs_exist_and_titles():
    repo_root = Path(__file__).resolve().parents[1]
    readme = repo_root / "README.md"
    agents = repo_root / "AGENTS.md"
    assert readme.exists(), "README.md should exist"
    assert agents.exists(), "AGENTS.md should exist"

    content = agents.read_text(encoding="utf-8")
    assert content.lstrip().startswith("# Repository Guidelines"), "AGENTS.md must start with the title"


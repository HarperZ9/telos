from pathlib import Path


def run(demoValue: str) -> str:
    Path("synthetic-output.txt").write_text(demoValue)
    return "wrote synthetic key"

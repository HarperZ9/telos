from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


PUBLIC_CHECKS = {
    "hero_or_mark": re.compile(r"(<img\s|!\[.+?\]\(.+?\))", re.I),
    "plain_tagline": re.compile(r"^>\s+\S+", re.M),
    "why_section": re.compile(r"^##\s+Why(\s+it\s+matters)?\b", re.I | re.M),
    "try_section": re.compile(r"^##\s+(Try it|Quickstart|30-second quickstart)\b", re.I | re.M),
    "what_section": re.compile(r"^##\s+What\s+(it\s+does|to\s+test\s+first)\b", re.I | re.M),
}

DEVELOPER_CHECKS = {
    "install_or_setup": re.compile(r"\b(pip install|npm install|cargo install|cmake|make|uv sync|python -m|git clone)\b", re.I),
    "runnable_command": re.compile(r"```(?:bash|sh|powershell|console)?\s+[\s\S]*?\b(python|node|npm|cargo|pytest|go test|cmake|make|pwsh|powershell)\b", re.I),
    "verify_or_test": re.compile(r"\b(test|pytest|unittest|cargo test|go test|verify|doctor|ci)\b", re.I),
    "integration_surface": re.compile(r"\b(CLI|MCP|API|plugin|IDE|TUI|app|browser|library|SDK|command)\b", re.I),
    "status": re.compile(r"^##\s+(Current\s+status|Status|Release)\b", re.I | re.M),
    "license": re.compile(r"\b(license|MIT|Apache|AGPL|fair-source|proprietary)\b", re.I),
}

CRYPTO_PROVENANCE = re.compile(r"\b(receipt|provenance|hash|digest|audit|evidence|verify|verdict)\b", re.I)
CRYPTIC_FIRST_SCREEN = re.compile(r"\b(membrane|substrate|organ|spine|witnessed|bilateral|conferred|efferent|afferent)\b", re.I)


@dataclass
class RepoReport:
    name: str
    path: str
    public_score: int
    developer_score: int
    verdict: str
    missing_public: list[str]
    missing_developer: list[str]
    warnings: list[str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf8", errors="replace")


def repo_name(path: Path) -> str:
    config = path / ".git" / "config"
    if config.exists():
        text = read_text(config)
        match = re.search(r"github\.com[:/]HarperZ9/([^/\s\"']+?)(?:\.git)?(?:\s|$|\"|')", text)
        if match:
            return match.group(1).removesuffix(".git")
    return path.name


def is_repo(path: Path) -> bool:
    return path.is_dir() and (path / ".git").exists()


def repo_dirs(roots: list[Path]) -> list[Path]:
    repos_by_path: dict[Path, Path] = {}
    for root in roots:
        resolved = root.resolve()
        if is_repo(resolved):
            repos_by_path[resolved] = resolved
            continue
        if not resolved.exists():
            continue
        for child in resolved.iterdir():
            if is_repo(child):
                repos_by_path[child.resolve()] = child
    return sorted(repos_by_path.values(), key=lambda p: p.name.lower())


def classify(text: str, repo: Path) -> RepoReport:
    first_screen = "\n".join(text.splitlines()[:35])
    public = {name: bool(rx.search(text)) for name, rx in PUBLIC_CHECKS.items()}
    developer = {name: bool(rx.search(text)) for name, rx in DEVELOPER_CHECKS.items()}
    missing_public = [name for name, ok in public.items() if not ok]
    missing_developer = [name for name, ok in developer.items() if not ok]
    warnings: list[str] = []
    if CRYPTIC_FIRST_SCREEN.search(first_screen):
        warnings.append("cryptic_terms_in_first_screen")
    if not CRYPTO_PROVENANCE.search(text):
        warnings.append("no_receipt_or_provenance_language")
    public_score = len(public) - len(missing_public)
    developer_score = len(developer) - len(missing_developer)
    verdict = "MATCH" if public_score >= 4 and developer_score >= 5 and not warnings else "DRIFT"
    return RepoReport(
        name=repo_name(repo),
        path=str(repo),
        public_score=public_score,
        developer_score=developer_score,
        verdict=verdict,
        missing_public=missing_public,
        missing_developer=missing_developer,
        warnings=warnings,
    )


def inspect_repo(repo: Path) -> RepoReport:
    readme = repo / "README.md"
    if not readme.exists():
        return RepoReport(
            name=repo_name(repo),
            path=str(repo),
            public_score=0,
            developer_score=0,
            verdict="DRIFT",
            missing_public=list(PUBLIC_CHECKS),
            missing_developer=list(DEVELOPER_CHECKS),
            warnings=["missing_readme"],
        )
    return classify(read_text(readme), repo)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit public/developer presentation layers for local repositories.")
    parser.add_argument("--root", action="append", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    roots = args.root or [Path("C:/dev/public")]
    reports = [inspect_repo(repo) for repo in repo_dirs(roots)]
    payload = {
        "schema": "project-telos.repo-presentation-audit/v1",
        "repo_count": len(reports),
        "match_count": sum(1 for report in reports if report.verdict == "MATCH"),
        "drift_count": sum(1 for report in reports if report.verdict == "DRIFT"),
        "reports": [report.__dict__ for report in reports],
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for report in reports:
            print(f"{report.verdict:5} {report.name:28} public={report.public_score}/5 developer={report.developer_score}/6")
    return 0 if payload["drift_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

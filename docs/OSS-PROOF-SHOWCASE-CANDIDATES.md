# OSS Proof Showcase Candidates

Generated: 2026-06-28

This document records live open-source repositories evaluated for Project Telos proof-showcase work. The rule is quality over volume: a candidate should receive a small, maintainable patch only when the issue is current, scoped, testable, and not spammy.

## AvAdiii/rewardspy

- URL: https://github.com/AvAdiii/rewardspy
- Shape: Python package and Textual/Rich dashboard for RL reward-function observability.
- Current live metadata: MIT license, Python, 46 stars, 4 forks, pushed 2026-06-27, issues enabled with 4 open issues, no open PRs at inspection time.
- Best immediate patch: issue #1, ASCII fallback for dashboard charts.
- Why it fits Telos: the concept maps directly to agent workflow objective monitoring. Telos now has `telos.objective.monitor`, which watches proxy-quality divergence, component dominance, ceiling saturation, steps since improvement, and quality variance collapse.
- Status: patched locally in `C:\dev\public\rewardspy`; tests and Ruff pass; ready for branch push and upstream PR.

## ripienaar/free-for-dev

- URL: https://github.com/ripienaar/free-for-dev
- Shape: high-reach curated catalog of free developer SaaS, PaaS, and IaaS tiers.
- Current live metadata: HTML primary language, 125k+ stars, 13k+ forks, pushed 2026-06-28, issues disabled, no open PRs at inspection time.
- Best immediate patch: none chosen yet. This repo needs careful catalog maintenance, not a forced contribution.
- Why it still matters: it is a strong test for Gather and Index as a catalog validation target: link health, duplicate categories, stale copy, formatting consistency, and provenance for service claims.
- Status: hold as a research/catalog-validation candidate until a concrete, non-spam patch is found.

# Spec: Source Checkout Launchers

## Objective
Define the native launcher contract for the Python flagships. Package-native execution remains the `pyproject.toml` console script plus `src/<package>/__main__.py`; raw source checkouts also get an explicit, tested bridge so operators and host surfaces can run the tools without hidden shell environment.

## Requirements
- [x] `python -m gather --version` works from `C:\dev\public\gather` with no `PYTHONPATH`.
- [x] `python -m forum --version` works from `C:\dev\public\forum` with no `PYTHONPATH`.
- [x] `python -m index --version` works from `C:\dev\public\index` with no `PYTHONPATH`, while `python -m index_graph` remains valid.
- [x] Tests remove ambient `PYTHONPATH` before invoking the source-checkout launcher.
- [x] Existing package entry points and MCP source profiles remain compatible.

## Technical Approach
Add tiny root-level source-checkout launcher packages for the `src/` layout repositories:
- `gather/__init__.py` extends the package path to `./src/gather`; `gather/__main__.py` delegates to `gather.cli.main`.
- `forum/__init__.py` extends the package path to `./src/forum`; `forum/__main__.py` delegates to `forum.cli.main`.
- `index/__init__.py` inserts `./src` into `sys.path`; `index/__main__.py` delegates to `index_graph.cli.main`.

These launchers are source-checkout conveniences only. The package scripts in `pyproject.toml` remain the installed interface, and the `src/<package>/__main__.py` modules remain the package module entry points. For `index`, Hatch wheel package selection is explicit so the source-only `index` alias cannot become part of the built distribution.

## Files to Modify
- `C:\dev\public\gather\tests\test_cli.py` - add no-PYTHONPATH source-checkout test.
- `C:\dev\public\gather\gather\__init__.py` - add source-checkout package path bridge.
- `C:\dev\public\gather\gather\__main__.py` - add source-checkout module launcher.
- `C:\dev\public\forum\tests\test_cli.py` - add no-PYTHONPATH source-checkout test.
- `C:\dev\public\forum\forum\__init__.py` - add source-checkout package path bridge.
- `C:\dev\public\forum\forum\__main__.py` - add source-checkout module launcher.
- `C:\dev\public\index\tests\test_cli_subcommands.py` - add no-PYTHONPATH source-checkout test for `python -m index`.
- `C:\dev\public\index\index\__init__.py` - add source-checkout import bridge.
- `C:\dev\public\index\index\__main__.py` - add source-checkout module launcher.
- `C:\dev\public\index\pyproject.toml` - pin Hatch wheel package selection to `src/index_graph`.
- `C:\dev\public\telos\docs\superpowers\specs\2026-06-29-source-checkout-launchers.md` - record status.

## Success Criteria
- [x] Each new test fails before its matching launcher exists.
- [x] `python -m pytest tests\test_cli.py -q` passes in gather.
- [x] `python -m pytest tests\test_cli.py -q` passes in forum.
- [x] `python -m pytest tests\test_cli_subcommands.py -q` passes in index.
- [x] Manual dogfood commands work from checkout roots with no `PYTHONPATH`:
  - `python -m gather --version`
  - `python -m forum --version`
  - `python -m index --version`

## Blockers
None identified.

## Verification Evidence
- RED: each no-PYTHONPATH subprocess test failed with `No module named gather`, `No module named forum`, and `No module named index`.
- GREEN: `python -m pytest tests\test_cli.py -q` in gather reported `7 passed`.
- GREEN: `python -m pytest tests\test_cli.py -q` in forum reported `20 passed`.
- GREEN: `python -m pytest tests\test_cli_subcommands.py -q` in index reported `8 passed`.
- DOGFOOD: `python -m gather --version`, `python -m forum --version`, and `python -m index --version` returned versions from source checkout roots with `PYTHONPATH` removed.

## Status: IMPLEMENTED

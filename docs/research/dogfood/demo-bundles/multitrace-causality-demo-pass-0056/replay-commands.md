# Replay Commands

```powershell
python docs\research\dogfood\tools\build_multitrace_causality_graph.py --spans docs\research\dogfood\fixtures\multitrace-causality-spans-pass-0055.json --source-binding docs\research\dogfood\schemas\source-evidence-binding-pass-0028.json --trace-join docs\research\dogfood\schemas\otel-trace-receipt-join-pass-0054.json --tool-receipts docs\research\dogfood\schemas\tool-receipts-pass-0054.json --out docs\research\dogfood\schemas\multitrace-causality-graph-pass-0055.json
python docs\research\dogfood\tools\compose_buyer_demo_manifest.py --graph C:\dev\public\telos\docs\research\dogfood\schemas\multitrace-causality-graph-pass-0055.json --out C:\dev\public\telos\docs\research\dogfood\demo-bundles\multitrace-causality-demo-pass-0056
python docs\research\dogfood\tools\test_buyer_demo_manifest.py
```

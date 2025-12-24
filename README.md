# CausalGridBench

A novel synthetic benchmark exposing causal reasoning failures in frontier LLMs.

Current models (including Grok 4) excel at correlation but struggle with Pearl's ladder of causation:
- Level 1: Association (pattern matching) ✅
- Level 2: Intervention (do-operator) ❌
- Level 3: Counterfactuals ❌

This benchmark generates controllable gridworlds with defined causal rules (Key protects from Fire, Door blocks Goal, etc.). Questions require explaining reward changes under interventions — forcing true causal understanding, not memorized shortcuts.

## Why This Matters for xAI
Truth-seeking AI must distinguish causation from correlation to accurately understand the universe. CausalGridBench directly measures progress toward that goal.

## Results (Preliminary)
Tested on Grok API — base model fails ~50% of intervention questions due to correlational reasoning.

## Run
```bash
python causalgridbench.py

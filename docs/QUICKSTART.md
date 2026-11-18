# Reproducing the public synthetic demonstration

```bash
python -m venv .venv
# activate your environment
pip install -r requirements.txt
pytest -q tests
python scripts/make_synthetic.py --output examples/synthetic --seed 123
python scripts/run_synthetic_demo.py --data examples/synthetic --epochs 4
```

Artificial samples contain no observed access-point IDs or real indoor topology. They verify array dimensions and code execution, **not the research paper's empirical accuracy**. Full paper reproduction on the original data remains gated on dataset licenses, privacy clearance and archived source adapters. See `docs/EVIDENCE_LEDGER.md` and `docs/DATA_ACCESS_AND_PRIVACY.md`.

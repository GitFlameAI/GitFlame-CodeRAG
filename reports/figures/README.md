# Figures

Figures referenced by `final_report.tex`. Drop generated plots here as PDF/PNG and
the report will include them automatically (via `\IfFileExists`); until then the
report renders a labelled placeholder box.

Expected files (produced by the evaluation code in Sprint 2):

- `recall_at_k.pdf` — Recall@K curves per method (BM25 / Dense / AST / RRF / RRF+Reranker).
- `rrf_vs_reranker.pdf` — per-issue score comparison, RRF only vs RRF + reranker.

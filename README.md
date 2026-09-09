# dsh-research-writing

[![npm version](https://img.shields.io/npm/v/dsh-research-writing)](https://www.npmjs.com/package/dsh-research-writing)
[![npm downloads](https://img.shields.io/npm/dw/dsh-research-writing)](https://www.npmjs.com/package/dsh-research-writing)
[![GitHub stars](https://img.shields.io/github/stars/Flan246/dsh-research-writing)](https://github.com/Flan246/dsh-research-writing)
[![license](https://img.shields.io/npm/l/dsh-research-writing)](./LICENSE)

Research writing bundle for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness): literature search + citations + BibTeX cleanup + LaTeX compile checks, in one install.

## What's inside

| Plugin | Tools |
|---|---|
| [dsh-lit-search](https://github.com/Flan246/dsh-lit-search) | `lit_search` / `lit_cite` / `lit_bib` / `lit_related` — Crossref + OpenAlex literature search, GB/T 7714 / APA / BibTeX citations (incl. arXiv preprints) |
| [dsh-latex-guard](https://github.com/Flan246/dsh-latex-guard) | `latex_check` / `bib_lint` / `bib_fill` / `cite_audit` — latexmk compile checks with engine auto-detection, BibTeX lint/fill, citation audit |

## Install

```bash
dsh plugin --profile web add dsh-research-writing
```

Both plugins are pulled in as dependencies and registered automatically. Do not install this bundle together with the standalone plugins in the same profile (the rows would duplicate).

## Without dsh

Each plugin also ships a standalone CLI and a SKILL.md:

```bash
npx dsh-lit-search search "mixture of experts" -n 5
npx dsh-lit-search cite 10.1038/nature14539 -s gbt7714
npx dsh-latex-guard check ./my-paper main.tex
npx dsh-latex-guard bib-fill refs.bib --write
```

## License

MIT

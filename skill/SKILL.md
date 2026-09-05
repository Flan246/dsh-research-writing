---
name: dsh-research-writing
description: End-to-end academic writing workflow for DeepSeek Harness — literature search, GB/T 7714 / APA / BibTeX citations, BibTeX cleanup, and LaTeX compile checks. Use when the user is writing or reviewing an academic paper, thesis, or LaTeX project.
---

# Research Writing Workflow

**If the host already has the plugin tools registered (lit_search / lit_cite / lit_bib / lit_related / latex_check / bib_lint / bib_fill / cite_audit), you MUST prefer calling those tools directly. The CLIs below are the fallback for hosts without the plugin.**

This bundle combines two plugins into one install. Typical end-to-end loop:

1. **调研**：`lit_search` 找论文 → `lit_related` 顺引用链扩展
2. **引用**：`lit_cite` 生成 GB/T 7714 / APA 条目，或 `lit_bib` 批量产出 BibTeX 写入项目的 `.bib`
3. **清洗**：`bib_lint` 去重与字段检查 → `bib_fill` 从 Crossref 补全缺失字段（只补不覆盖）
4. **对账**：`cite_audit` 比对 tex 引用与 bib（支持 biblatex 的 \autocite/\nocite 等）
5. **验证**：`latex_check` 编译并返回结构化错误（自动识别 xelatex/lualatex/中文正文）

CLI fallback：`npx dsh-lit-search <search|cite|bib|related>` 与 `npx dsh-latex-guard <check|bib-lint|bib-fill|cite-audit>`，均支持 `--json`。

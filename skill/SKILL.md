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

## 文献判断力：选文献、定数量、写综述前必读

当任务涉及**文献综述写作、选择/筛选参考文献、确定引用数量与优先级、整理引用格式与排序、判断期刊是否高质量**时，先阅读本包内的 `skill/citation-guide.md`（论文引用指南），按其中的数量基准、三类文献配方、三轮检索法与雷区清单执行，再调用上述工具落地。指南还覆盖 GB/T 7714 顺序编码制与著者-出版年制的排序规则、脚注/尾注/文后参考文献表的区别。

判断期刊/会议是否"高质量"时，查本包 `data/journal-whitelist.json`（经管+计算机学科子集，每条目含 CSSCI/北大核心/CCF/中科院分区等官方出处与名单版本）；名单内按标注级别采信，名单外不要凭印象断言级别，可建议用户补充核验。该名单按季度核验官方版本，可能滞后于最新换版。

CLI fallback：`npx dsh-lit-search <search|cite|bib|related>` 与 `npx dsh-latex-guard <check|bib-lint|bib-fill|cite-audit>`，均支持 `--json`。

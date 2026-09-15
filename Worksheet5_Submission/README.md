# Worksheet 5 Submission Package — CircleGuard BMad Lab


This folder contains everything the assignment ("Student Laboratory — Specification
Refactoring & Multi-Agent Quality Gates with BMad") asks to be submitted: Worksheets 1–4 for
validation, the completed Worksheet 5, and all prompts / agent perspectives / refactored
contracts / terminal outputs referenced by it.

## Team
* William Joseph Verdesoto
* Deiner Julian Motta
* Juan Camilo Corrales Osvath

## Start here

**`Worksheet_5_Complete.md`** — the single combined Worksheet 5 document (all of §5.1–§5.4 plus
the submission metadata table). This is the primary deliverable. Every claim in it links back
to the fuller evidence file in the numbered subfolders below.


## Folder structure

```
00_Prerequisites/         Assignment_Spec.pdf (the lab handout), unit3_Worksheets1-4.docx
                           (your prior manual "No-AI" audit), CircleGuard.pdf (the original
                           project brief the audit was based on)
01_Phase1_Benchmarking/    Worksheet 5 §5.1: /bmad-prd validate + /bmad-review output,
                           adversarial/edge-case JSON bundles, the human-audit baseline used
                           to benchmark against, and the audited PRD/UX/Architecture exhibits
                           as they stood at Phase 1 (note: these are point-in-time copies,
                           see "Source of truth" below)
02_Phase2_PartyMode/       Worksheet 5 §5.2: the /bmad-party-mode debate record (all four
                           agent positions in full, the Round 6 addendum, the 7-gate closure
                           annex), the convocation briefing, and the raw HTML session keepsake
03_Phase3_Contracts/       Worksheet 5 §5.3: the AD-1 architectural invariant and the
                           6-scenario BDD acceptance suite
04_Phase4_ReadinessGate/   Worksheet 5 §5.4: the /bmad-sprint-planning readiness-gate result
                           (FAIL) and the full findings file it produced
05_Source_Specifications/  The live, canonical prd.md / architecture.md /
                           ux-design-specification.md (from `cg plan/`) — these are the files
                           Phase 4 checked, and the ones the Phase 2/3 diff still needs to be
                           applied to
Worksheet_5_Complete.md    The combined, submission-ready Worksheet 5
README.md                  This file
```

## Source of truth note

`01_Phase1_Benchmarking/*_exhibit.md` and `05_Source_Specifications/*.md` are **two different
copies** of the same three documents (they diverged because the Phase 1 audit ran against
extracted/redacted exhibits while `05_Source_Specifications/` is the live, workflow-tracked
originals). This divergence is itself flagged as Finding 3 in the Phase 4 gate. Use
`05_Source_Specifications/` as canonical going forward.

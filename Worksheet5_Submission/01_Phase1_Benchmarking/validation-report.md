# BMad PRD Validation Report — CircleGuard

**Workflow:** `/bmad-prd validate`  
**Artifact reviewed:** `prd.md` (Exhibit A extracted from `prerequisites/unit3.docx`)  
**Review date:** 2026-09-14  
**Overall verdict:** **NOT DECISION-READY**

## Executive assessment

The PRD has a specific graph-containment thesis, contiguous requirement identifiers, a stated privacy posture, and several quantitative targets. It is not ready to authorize implementation because the Phase 1 boundary conflicts with unqualified Phase 2/3 journeys and requirements, while the safety-critical state, identity, consent, and fence-resolution rules remain under-specified.

The independent rubric review found **21 issues**: **4 critical**, **13 high**, **4 medium**, and **0 low**.

## Dimension scorecard

| Dimension | Result | Principal reason |
|---|---|---|
| Decision-readiness | Broken | The approved Phase 1 target cannot be determined from the journeys and FR inventory. |
| Substance over theater | Thin | Several platform capability blocks have no supporting journey, outcome, or MVP rationale. |
| Strategic coherence | Thin | Success measures use incompatible clocks and can reward over-fencing. |
| Done-ness clarity | Broken | Core contact, status, identity, and release behaviors lack acceptance-ready semantics. |
| Scope honesty | Broken | The three-phase plan is contradicted by the unqualified requirement inventory. |
| Downstream usability | Broken | No glossary, phase tags, acceptance criteria, or strategy-to-requirement traceability. |
| Shape fit | Broken | Compliance and high-impact exceptions are asserted or omitted rather than specified. |

## Critical blockers

1. **MVP scope contradiction.** Phase 1 promises an intelligence core and manual circles, yet the current journeys and FRs also require WiFi/BLE sensing, LMS updates, gate validation, dashboards, questionnaires, certificate storage, dynamic RBAC, biometrics, and web parity. Every requirement needs an explicit phase/applicability tag.
2. **Contact and fence algorithm is indeterminate.** The edge predicate, traversal depth, cycle handling, precedence, idempotency, active-path semantics, release conditions, and re-exposure behavior are not defined.
3. **Identity model contradicts the anonymity claim.** A retained identity mapping and linked biometrics make the model pseudonymous, not non-reversible anonymous. Purpose, consent, custody, access, retention, deletion, and breach boundaries are missing.
4. **Compliance lacks behavioral traceability.** FERPA and deletion claims do not map data classes, purposes, roles, retention, exceptions, audit evidence, or acceptance tests.

## Highest-priority corrective actions

1. Tag every UJ, FR, DR, NFR, and success criterion by phase; publish a Phase 1 acceptance baseline and explicit MVP non-goals.
2. Add a formal state-transition and graph-traversal contract with worked examples for cycles, duplicate/concurrent events, conflicting evidence, negative tests, overrides, and re-exposure.
3. Replace the anonymity claim with accurate data classification and define keyed pseudonymization, key custody/rotation, identity-vault controls, biometric boundaries, and deletion across every store and derivative.
4. Define one end-to-end containment SLI and measurable component SLIs, including timestamps, percentiles, delivery semantics, workload, and failure exclusions.
5. Add a glossary and traceability matrix: phase → outcome/SC → journey → FR/DR/NFR → owner/dependency → acceptance test.
6. Add Open Questions and Assumptions indexes with accountable owners and resolution deadlines.
7. Replace implementation prescriptions in the PRD—such as Kubernetes PersistentVolume, JWT claims, REST, and a shared Expo codebase—with product-level outcomes; retain selected technologies and rationale in Architecture.

## Mechanical and extraction checks

- SC-1–SC-5, UJ-1–UJ-6, DR-1–DR-6, FR-1–FR-38, and NFR-1–NFR-8 are contiguous and unique.
- No explicit cross-references exist, so cross-reference resolution cannot establish coverage.
- No `[ASSUMPTION]` markers or Assumptions Index exist.
- The source Success Criteria table was flattened during extraction; its targets remain readable but are not reliably machine-paired with their measurements.
- Several journeys lack a specific role-based protagonist.
- Missing load-bearing sections: Non-Goals, Open Questions/decision owners, Glossary, acceptance criteria, and traceability.

## Decision gate

**Do not approve Phase 1 implementation from this PRD as written.** Approval should follow resolution of all four critical blockers and the Phase 1 scope/traceability corrections. The full evidence and fixes are recorded in `review-rubric.md`.

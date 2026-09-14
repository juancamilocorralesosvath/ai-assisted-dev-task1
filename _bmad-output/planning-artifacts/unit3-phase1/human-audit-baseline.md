# Human Audit Baseline — Previous Worksheets 1 and 2

**Source:** `prerequisites/unit3.docx` only.  
**Purpose:** blind benchmark reference for the new Phase 1 worksheet. This baseline was not supplied to the independent BMad reviewers.

## Worksheet 1 — PRD reviewer (Joe)

| Finding | Category | Human result |
|---|---|---|
| FR-28 mandates Kubernetes PersistentVolume | Design Leak [D] | Major |
| FR-3 uses undefined “shared closed space” | Vagueness [V] | Major |
| UJ-4 does not say whether one or both users must confirm | Ambiguity [A] | Major |
| FR-30/FR-32 omit stale QR behavior after a status change | Incompleteness [I] | Major |
| NFR-3 leaves “normal load” undefined | Untestability [U] | Major |

## Worksheet 1 — UX reviewer (Joshua)

| Finding | Category | Human result |
|---|---|---|
| “Successful scan in under 200ms” lacks a measurement boundary and conditions | Untestability [U] | Major |
| “Magic Door” and “calm typography” are subjective | Vagueness [V] | Minor |
| QR states are defined by color while the same document forbids color-only status | Contradiction [C] | Critical |
| External registration omits failure, retry, and recovery | Incompleteness [I] | Major |
| UX requires offline QR resiliency while Architecture defers offline support | Cross-document [X] | Critical |
| Spanish dashboard labels appear without an i18n policy | Ambiguity [A] | Minor bonus |

## Worksheet 1 — Architecture reviewer (Juan)

| Finding | Category | Human result |
|---|---|---|
| Existing WiFi AP hardware is not characterized | Incompleteness [I] | Major |
| LMS synchronization lacks protocol and failure behavior | Incompleteness [I] | Major |
| Multi-campus support lacks a mechanism | Incompleteness [I] | Major |
| Spring Data Neo4j annotations plus raw Cypher are premature design detail | Design Leak [D] | Major |
| Caffeine plus Redis is prescribed without invalidation/TTL/coherence requirements | Design Leak [D] | Major |
| JWT feature gating does not distinguish UI hiding from backend authorization | Ambiguity [A] | Major bonus |

## Worksheet 2 — Team cross-document baseline

| Team collision | Assessment for this benchmark |
|---|---|
| UX offline QR promise vs Architecture Phase 2 deferral | Valid, critical cross-document contradiction. |
| PRD certificate storage vs Architecture existing WiFi hardware | Weak/invalid pairing: the two excerpts concern unrelated capabilities. |
| QR color states vs UX accessibility rule | Valid defect, but intra-document rather than cross-document. |

## Baseline totals used in Worksheet 5.1

- Human PRD defects: 5 substantive findings.
- Human UX/UI findings: 6 substantive findings, including one critical accessibility contradiction.
- Human Architecture findings: 6 substantive findings.
- Human cross-document findings: one clearly valid collision, one misclassified intra-document contradiction, and one weak/invalid pairing.
- Human security/privacy coverage: authorization/stale-token risk appears in the Architecture review, but the audit does not provide a systematic FERPA/HIPAA/PII analysis.

# Worksheet 5: Agentic Integration & Quality Gate Report
## CircleGuard — Specification Refactoring & Multi-Agent Quality Gates with BMad

---

## Submission Metadata

| Field | Team Entry |
|---|---|
| Team Name / Triad ID | CircleGuard Triad |
| Product Lead | Joe |
| UX / Design Lead | Joshua |
| Architecture Lead | Juan |
| Submission Date | 2026-09-14 |

> Note: Phases 2–4 were run and logged under the session tag **"Lead Engineer: Julian"** in
> the raw BMad `/bmad-party-mode` and `/bmad-sprint-planning` transcripts (see
> `02_Phase2_PartyMode/` and `04_Phase4_ReadinessGate/`). Confirm before submission whether
> this refers to the Architecture Lead above or a separate team member, and align the name on
> this page with the transcripts if needed.

---

## 5.1 Benchmarking Matrix — Human Audit vs. BMad Automated Review

*(Full detail, evidence, and per-dimension analysis: `01_Phase1_Benchmarking/worksheet-5-phase-1.md`)*

| Audit Dimension | Human Triad Finding (Worksheets 1 & 2) | BMad Automated Review Finding | Evaluation / Winner |
|---|---|---|---|
| **PRD Defects** — Design Leaks [D], Vagueness [V] | 5 focused defects: FR-28 Kubernetes leak, FR-3 "shared closed space" undefined, UJ-4 confirmation ambiguity, stale-QR omission, NFR-3 "normal load" undefined. | `/bmad-prd validate`: not decision-ready, 21 rubric findings (4 critical, 13 high, 4 medium). `/bmad-review`: 22 adversarial + 49 edge-case findings — confirmed all 5 human findings, then exposed a larger scope contradiction, missing fence state machine, idempotency gaps, incompatible clocks, and non-testable metrics. | ☐ Human deeper **☒ BMad deeper** ☐ Full agreement |
| **UX & UI States** — Missing states [I], Untestability [U] | Unbounded 200ms benchmark, subjective copy, color-only QR states, missing registration retry, offline contradiction, unexplained Spanish labels. | Confirmed all human findings, then enumerated ~10 further missing states (proximity consent timeout, gate decision states, fence-review states, biometric refusal, reduced-motion fallback, etc.). | ☐ Human deeper **☒ BMad deeper** ☐ Full agreement |
| **Cross-Document Collisions** — Capability mismatch [X] | Offline QR (UX) vs. Phase 2 deferral (Architecture) — the collision resolved in §5.2 below. | Confirmed the offline conflict, plus 6 further collisions (FR-count mismatch, Phase 1 scope conflict, capture-vs-consent conflict, professor-name/anonymity conflict, "complete deletion" vs. immutable audit records, latency-target conflict). | ☐ Human deeper **☒ BMad deeper** ☐ Full agreement |
| **Security & Privacy Gaps** — FERPA/HIPAA/PII [G] | JWT feature-gating ambiguity (client-hiding vs. server authorization); stale-QR risk. No systematic privacy pass. | Enumeration attack surface on salted hashes, incomplete "deletion" definition, professor-dashboard re-identification, biometric consent/lifecycle gaps, QR replay, JWT revocation absence, certificate upload/access gaps. | ☐ Human deeper **☒ BMad deeper** ☐ Full agreement |

**Key Takeaway (full text in `01_Phase1_Benchmarking/worksheet-5-phase-1.md`):** BMad's automated review was deeper across all four dimensions — it is comprehensive on state-machine, security, and cross-document coverage the human triad could not reach in the time available. The human audit remained valuable for concise prioritization and source-language/localization nuance the automated lenses did not flag.

---

## 5.2 Party Mode Resolution Transcript & Executive Decision

*(Full transcript, all four agent positions in depth, Round 6 addendum, and the 7-gate
traceability annex: `02_Phase2_PartyMode/worksheet-5-phase-2.md`. Raw session keepsake:
`02_Phase2_PartyMode/party-mode-transcript.html`.)*

**Chosen Collision:** ☒ **Option A — The Offline Gate Collision (Probe 2).**
UX Design Specification §2.3/§4.1 vs. Architecture Decision Document (Mobile Architecture),
plus an underlying phase-governance defect in the PRD (Gatekeeper filed Phase 2 while
Architecture already scheduled it as build item 7 of 8).

**Target Document Clauses:**
- *UX Design Spec* (`ux-design-specification.md`): "Offline Resiliency: QR tokens are
  generated and valid even without active cellular data" (§2.3, `ux:174`); "The 'Walking Pace'
  Benchmark: … under 200ms" (`ux:171`); gate-flow diagram with no branch for absent network
  (`ux:251-264`).
- *Architecture Decision Document* (`architecture.md`): "Offline Support: Not required
  (Phase 1) … Deferred" (`architecture.md:186`); "QR Token Service: Embedded in Auth Service"
  (`architecture.md:206`) — which makes on-device token *generation* physically impossible.

**Agent Positions Summary** *(condensed — full arguments in `worksheet-5-phase-2.md` §3)*:

- **John (PM):** Traced the collision to an untagged-phase defect that the implementation
  plan had already resolved by default; forced the fail-posture decision at unstaffed gates.
- **Sally/Freya (UX):** Conceded the missing state before it was raised; designed the missing
  **Amber — Hold for Verification** state; found the second offline actor (the staff scanner).
- **Winston (Architect):** Showed offline verification was already a property of signed
  tokens, not a feature to grant; replaced the credential design once its rotation scheme was
  shown to permit unbounded re-minting; found the revocation-lag framing that broke the
  deadlock.
- **Murat (Test Architect):** Rejected the scope framing — none of the four offline claims
  were falsifiable; required `lastRevocationSyncAt` on the wire to make the gate observable;
  found the session's highest-risk defect (a self-signed "current status" field).

**Final Engineering Resolution:**
> Campus entry validation ships in Phase 1 as an offline-first decision path in which the
> scanner is the sole source of health status, the credential proves identity only and is bound
> to a live presentation, and every gate outcome is a function of two on-device integers —
> scanner revocation-sync age and clock-anchor state — with no network call anywhere on the
> decision path.

Full numeric decision table (cache-age cliffs, fail-open/closed matrix, revocation SLA,
latency budgets, credential design, clock authority, replay control, key rotation, holder
binding) is in `worksheet-5-phase-2.md` §4.1. It is carried forward unchanged into §5.3 below.

---

## 5.3 Production-Grade Refactored Contracts

*(Full text, including the six-scenario BDD suite and the field-by-field mapping back to
§5.2: `03_Phase3_Contracts/worksheet-5-phase-3.md`.)*

### Artifact A — BMad Architectural Invariant

```
### AD-1: Offline-First Campus Entry Decision Path
- Status: ADOPTED
- Binds: Entry Gateway Service; carrier mobile app; staff scanning app (FR-31)
- Prevents: Admission of a Fenced carrier on a pre-issuance token; acceptance of a
  static/replayed capture (spoofed liveness); wall-clock reads on the decision path
- Rule: Zero-network-call on-device decision path. Scanner staleness tiers on
  lastRevocationSyncAt (S): 0-120s -> GREEN/RED permitted; 121-900s -> RED/AMBER only;
  >=901s -> AMBER only. Credential: 96 pre-minted, platform-signed tokens over 28,800s,
  identity/issuance/validity only, no status field. Revocation propagation: p99 <=60s,
  hard max 180s, polled every 20s. Time: serverTime + delta-monotonic only, OS wall clock
  prohibited on the decision path. Clock skew: +/-30s anchored / +/-60s fallback / no
  verdict if never synced; CLOCK_SUSPECT after 5 consecutive out-of-range samples.
  Liveness: Presence Ring read inside the existing 240ms decode burst (zero added latency);
  failure closes the gate at every gate class, the sole exception to fail-open.
- Trade-off: Live video relay (detected post-hoc via FR-40 device fingerprinting) and
  cross-gate offline replay (100% detected within 300s of reconnection) are accepted and
  explicitly not claimed as prevented. Up to 180s of revocation lag is accepted in
  exchange for offline, zero-network-call operation.
```

### Artifact B — BDD Acceptance Specification (excerpt — full 6-scenario suite in Phase 3 file)

```gherkin
Feature: Offline campus entry validation at an unstaffed perimeter gate

  Scenario: One second past the GREEN cliff, the scanner cannot assert the present
    Given the scanner's lastRevocationSyncAt age S is exactly 121 seconds
    And the presented credential is cryptographically valid and unexpired
    When a carrier presents their credential at an unstaffed perimeter gate
    Then the scanner must not render GREEN
    And the scanner renders RED or AMBER only, per the carrier's last known fence status

  Scenario: A detected static-capture liveness failure closes even an unstaffed perimeter
    Given the credential's cryptographic signature and expiry are valid
    And the Presence Ring liveness check fails during the scanner's decode burst
    When the carrier presents their credential at any gate class, including an unstaffed
      perimeter
    Then the scanner renders LIVENESS FAILED
    And the gate denies entry regardless of gate class or staffing
    And no fail-open exception applies
```

*(The other four scenarios — the GREEN N=120 boundary, the RED N=899/901 fail-open cliff at
an unstaffed perimeter, and `CLOCK_SUSPECT` after 5 consecutive skew samples — are in
`03_Phase3_Contracts/worksheet-5-phase-3.md`.)*

---

## 5.4 Implementation Readiness Quality Gate Sign-Off

*(Full findings and reasoning: `04_Phase4_ReadinessGate/worksheet-5-phase-4.md` and
`04_Phase4_ReadinessGate/implementation-readiness.md`.)*

**Command Executed:** `/bmad-sprint-planning` (readiness-only intent)

**Resulting Status:**
☐ PASS
☐ CONCERNS
**☒ FAIL** — Critical cross-document collisions remain; blocking code implementation.

**Remaining Identified Risks:**

1. **(Critical)** No epics or stories exist anywhere in the project — nothing decomposes the
   PRD/UX/Architecture into implementable, independently completable units. *Fix:*
   `bmad-create-epics-and-stories`.
2. **(Critical)** The Phase 2/3 Offline Gate resolution (AD-1) is adopted but not yet applied
   to the live specification files — `prd.md` still files Gatekeeper under Phase 2 and
   `architecture.md` still carries the voided "Offline Support: Not required (Phase 1)" row.
   This is the same gap Phase 2's own traceability annex flagged as "G1: decided, not
   applied." *Fix:* apply the Phase 2 §G7 diff set, or route through `bmad-correct-course`.
3. **(Medium)** Two disagreeing copies of the same specs exist with no canonical designation
   (`05_Source_Specifications/` vs. `01_Phase1_Benchmarking/*_exhibit.md`). *Fix:* designate
   the live copies canonical; label the Phase 1 copies as point-in-time audit exhibits only.

**Architect Sign-Off Signature:** _______________________________________
**Date:** _______________________
*(Declares that specifications are implementation-ready and safe for autonomous agent
execution — to be completed once findings 1–3 above are triaged.)*

---

## Package Contents

See `README.md` in this folder for the full file manifest and what each subfolder contains.

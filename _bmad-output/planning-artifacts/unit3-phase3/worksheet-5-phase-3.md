# Worksheet 5 — §5.3 · Phase 3
## Specification Refactoring into Production Contracts — CircleGuard

**Phase:** Unit 3 — Phase 3
**Lead Engineer:** Julian
**Source of record:** `_bmad-output/planning-artifacts/unit3-phase2/worksheet-5-phase-2.md`
(§4 Final Engineering Resolution, §4.1 Decision table, §G2–G4, and the "Puente a §5.3" bridge
table at the end of that file)
**Method:** Direct synthesis from the Phase 2 consensus — no new `/bmad-party-mode` round was
run; every value below is already adjudicated and numeric in the Phase 2 record, so this phase
formalizes rather than re-decides.
**Scope respected:** `cg plan/prd.md`, `cg plan/architecture.md`, and
`cg plan/ux-design-specification.md` remain unedited. The two artifacts below are new,
freestanding contracts — they are not diffs applied to the source files. Applying the G7 diff
set to the source files is out of scope for this phase (Phase 2's G1 gate already flagged this
as "decided, not applied").

---

## Artifact A — BMad Architectural Invariant

### AD-1: Offline-First Campus Entry Decision Path

- **Status:** ADOPTED
- **Binds:** Entry Gateway Service; carrier mobile app (QR/credential presentation); staff
  scanning app (FR-31, since two devices at one gate can be offline independently)
- **Prevents:** (1) Admission of a carrier whose fence status changed to `Fenced` after their
  credential was pre-issued but before the scanner's revocation list caught up; (2) a verdict
  rendered from a static/replayed image presented to the scanner (spoofed liveness); (3) any
  code path that reads the device or scanner OS wall clock to decide a gate outcome.
- **Rule:** Every gate decision is computed on-device with zero network calls on the decision
  path. The scanner's authority degrades in two numeric steps keyed to
  `lastRevocationSyncAt` age (`S`): `S = 0–120s` → GREEN or RED permitted (fully
  authoritative); `S = 121–900s` → RED or AMBER only (GREEN prohibited, since the scanner can
  no longer assert the present); `S ≥ 901s` → AMBER only (RED prohibited, since a stale list
  may wrongly deny an already-cleared carrier). The credential is a batch of 96 pre-minted,
  platform-signed tokens over a 28,800s (8h) window; the device presents these and cannot
  generate new ones, and the token carries identity, issuance, and validity only — no status
  field. Revocation-list propagation is bounded at **p99 ≤ 60s, hard maximum 180s**, polled
  every 20s, verified against a scenario injecting ≥1 dropped poll in ≥5% of test runs. All
  decision-path time is `serverTime + Δmonotonic` anchored during the last online contact;
  reading the OS wall clock on the decision path is prohibited. Clock-skew tolerance is ±30s
  when server-anchored (±60s on wall-clock fallback, no verdict if never synced), detected via
  5 consecutive out-of-range `scannerNow − iat` samples triggering `CLOCK_SUSPECT` (manual
  routing) — not a median-based detector, which a 300s pre-mint grid renders statistically
  blind (~26s sampling error at n=32, the same order as the skew being detected). Liveness is
  verified via the Presence Ring (phase-locked, server-anchored, read inside the scanner's
  existing 240ms decode burst — zero added latency); a liveness failure is the single exception
  to fail-open and closes the gate at every gate class, including unstaffed perimeters.
- **Trade-off:** Two residual risks are explicitly accepted and bounded, and no document may
  claim either is prevented: (1) real-time video relay between two coordinated people at the
  moment of presentation — not preventable offline, detected post-hoc via FR-40 device
  fingerprinting; (2) cross-gate replay with both scanners offline simultaneously — not
  preventable offline, detected at 100% within 300s of reconnection via `jti` (16-byte,
  330s/360s retention) reconciliation. In exchange for zero-network-call operation, a cleared
  carrier can remain admissible on a stale but cryptographically valid credential for up to
  180s after clearance (revocation lag), and Gate Transit Time is fixed at 900ms p95/1500ms
  p99 with the Presence Ring active — any implementation that disables the ring to hit a
  faster number invalidates this invariant, since the budget was set with the ring's decode-
  burst read included at zero marginal cost.

---

## Artifact B — BDD Acceptance Specification

```gherkin
Feature: Offline campus entry validation at an unstaffed perimeter gate

  Scenario: Scanner revocation-sync staleness gates the verdict, not the network
    Given the scanner's lastRevocationSyncAt age S is exactly 120 seconds
    And the presented credential is cryptographically valid and unexpired
    When a carrier presents their credential at an unstaffed perimeter gate
    Then the scanner renders GREEN
    And the gate.decision.recorded event carries lastRevocationSyncAt = 120

  Scenario: One second past the GREEN cliff, the scanner cannot assert the present
    Given the scanner's lastRevocationSyncAt age S is exactly 121 seconds
    And the presented credential is cryptographically valid and unexpired
    When a carrier presents their credential at an unstaffed perimeter gate
    Then the scanner must not render GREEN
    And the scanner renders RED or AMBER only, per the carrier's last known fence status

  Scenario: A stale scanner must not deny a possibly-cleared carrier past the RED cliff
    Given the scanner's lastRevocationSyncAt age S is exactly 899 seconds
    And the carrier's last known status on this scanner is Fenced
    When the carrier presents their credential at an unstaffed perimeter gate
    Then the scanner renders RED

  Scenario: Past 900 seconds staleness, an unstaffed gate must not deny on stale data
    Given the scanner's lastRevocationSyncAt age S is exactly 901 seconds
    And the carrier's last known status on this scanner is Fenced
    And the gate class is an unstaffed perimeter
    When the carrier presents their credential at the gate
    Then the scanner must not render RED
    And the scanner renders AMBER, routing to manual verification
    And the physical barrier opens per the unstaffed fail-open policy

  Scenario: Clock-suspect detection routes to manual check instead of a silent wrong verdict
    Given the scanner has recorded 5 consecutive scans with (scannerNow - iat) outside the
      ±30 second server-anchored tolerance
    When the 5th consecutive out-of-range sample is recorded
    Then the scanner enters CLOCK_SUSPECT state
    And every subsequent scan is routed to manual verification until re-synced
    And no GREEN or RED verdict is rendered while CLOCK_SUSPECT is active

  Scenario: A detected static-capture liveness failure closes even an unstaffed perimeter
    Given the credential's cryptographic signature and expiry are valid
    And the Presence Ring liveness check fails during the scanner's decode burst
    When the carrier presents their credential at any gate class, including an unstaffed
      perimeter
    Then the scanner renders LIVENESS FAILED
    And the gate denies entry regardless of gate class or staffing
    And no fail-open exception applies
```

---

## §5.3 Field Mapping (per the Phase 2 bridge table)

| §5.3 field | Value |
|---|---|
| `AD-n:` decision name | AD-1: Offline-First Campus Entry Decision Path |
| `Status` | ADOPTED |
| `Binds` | Entry Gateway Service · carrier mobile app · staff scanning app (FR-31) |
| `Prevents` | Admission of a Fenced carrier on a pre-issuance token · acceptance of a static/replayed capture · wall-clock reads on the decision path |
| `Rule` | Zero-network-call decision path; 120s/900s scanner staleness tiers; revocation lag p99 ≤60s/hard max 180s; `serverTime + Δmonotonic` only; ±30s/±60s clock tolerance with `CLOCK_SUSPECT` detection; Presence Ring liveness, fails closed at every gate class |
| `Trade-off` | Residual, explicitly bounded and not claimed as prevented: live video relay (detected via FR-40) and cross-gate offline replay (100% detected within 300s of reconnect); up to 180s revocation lag accepted in exchange for offline operation |
| `Feature/Scenario/Given/When/Then` | See Artifact B above — six scenarios covering the GREEN/RED/AMBER staleness cliffs, `CLOCK_SUSPECT`, and `LIVENESS FAILED` |

**Status:** §5.3 closed. No edits made to `prd.md`, `architecture.md`, or
`ux-design-specification.md`.

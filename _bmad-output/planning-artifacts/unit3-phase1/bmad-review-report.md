# BMad Multi-Lens Review — CircleGuard Phase 1

**Workflow:** `/bmad-review`  
**Required lenses:** Adversarial and Edge-Case Hunter  
**Review method:** each lens ran in a fresh independent context and received no previous human audit results.  
**Primary target:** `prd.md`  
**Supplementary target:** `specification-bundle.md` (PRD + UX + Architecture), used to evaluate the full Worksheet 5.1 dimensions.

## Raw output inventory

| Target | Lens | Findings | Raw result |
|---|---:|---:|---|
| PRD | Adversarial | 22 | `review-adversarial-prd.json` |
| PRD | Edge-Case Hunter | 49 | `review-edge-cases-prd.json` |
| Specification bundle | Adversarial | 20 | `review-adversarial-bundle.json` |
| Specification bundle | Edge-Case Hunter | 57 | `review-edge-cases-bundle.json` |

The counts are raw lens outputs, not unique defect totals: related findings deliberately recur when two independent lenses reach the same concern.

## Convergent high-impact findings

1. **Phase boundary is unusable.** Phase 1 is described as a manual intelligence core, yet unqualified journeys and requirements depend on later sensing, LMS, gate, dashboard, questionnaire, certificate, RBAC, QR, and web-parity capabilities.
2. **Fence state machine is missing.** No canonical precedence, idempotency, causal-path, cycle, depth, concurrency, negative-evidence, or release contract exists.
3. **Privacy claims exceed the design.** Salted SHA-256 over predictable identifiers is not safely non-reversible; biometrics, de-identification, names in the professor dashboard, multi-channel alerts, analytics, and deletion each cross unstated privacy boundaries.
4. **Gate behavior is incomplete.** Green/Red omits Pending, Unknown, Offline, Revoked, Expired, invalid-signature, clock-error, and service-error states. A valid token can be replayed or remain usable after the holder becomes fenced.
5. **Offline promise conflicts with Architecture.** UX promises tokens usable without cellular data while Architecture defers offline support to Phase 2.
6. **Secure upload behavior is absent.** FR-28 leaks a Kubernetes storage choice while omitting type/size validation, malware scanning, quarantine, encryption, least-privilege access, retention, deletion, backup, and capacity-failure behavior.
7. **Runtime RBAC is unsafe as specified.** UI rendering from JWT claims is not backend authorization; revocation, permission versioning, privilege ceilings, separation of duties, last-admin protection, and audit atomicity are missing.
8. **Success measures are not reproducible.** The 1 s, 30 s, 60 s, and 200 ms targets lack common measurement boundaries, and “normal load” lacks a workload definition.

## UX/UI states found by the automated review

- Sporadic contact: confirm, deny, dismiss, timeout, conflicting confirmations, and pending-edge expiry.
- Smart check-in: ambiguous room, overlapping schedule, missed/locked-device prompt, disabled permissions, manual fallback, duplicate join, stale/full capacity.
- Fence resolution: submitted, under review, rejected, accepted/recalculating, released, and still fenced by another cause.
- Campus entry: Active, Fenced, Pending Review, Unknown, Expired, Revoked, Offline-Unverifiable, Service-Unavailable, malformed token, clock error, and accessible non-color feedback.
- Visitor onboarding: verification failure, abandonment, orphan cleanup, resume, no biometric hardware, biometric refusal, shared device, device change, and non-biometric recovery.
- Questionnaires: missing/invalid configuration, configuration changed mid-response, stale version, incomplete response, unsafe sensitive fields, and rollback.
- Certificate upload: oversize, mislabeled, malformed, encrypted, malicious, storage full/unavailable, access outside case scope, and validation inconclusive/revoked.

## Security and privacy gaps found by the automated review

- Enumeration-resistant keyed pseudonymization, secret custody, rotation, collision handling, and migration are unspecified.
- Complete deletion conflicts with Kafka/audit immutability and omits graph, vault, cache, files, responses, analytics, logs, backups, and active-case handling.
- Professor participant names can expose identifiable attendance and health context.
- Push/email/SMS may reveal medical context on lock screens, email subjects, shared devices, recycled phone numbers, and telecom infrastructure.
- Small cohorts and differencing queries can re-identify people in hotspot dashboards.
- Biometric scope, consent, storage boundary, retention, false-match policy, and an alternative path are absent.
- QR tokens lack nonce, audience, replay detection, authenticated scanner, and an explicit offline risk window.
- De-identification, certificate access, overrides, role changes, and questionnaire changes lack purpose-bound, tamper-evident privileged audit controls.

## Benchmark conclusion

The automated review confirms the strongest human findings and has materially broader coverage, especially for state transitions, distributed-system failure modes, authentication, replay, retention/deletion, notification privacy, analytics re-identification, and accessible degraded states. The human audit remains valuable for editorial and context-sensitive observations—especially the subjective “Magic Door” language, unexplained Spanish labels/i18n, and concise source-level diagnoses—but BMad is the overall winner in all four required Worksheet 5.1 dimensions.

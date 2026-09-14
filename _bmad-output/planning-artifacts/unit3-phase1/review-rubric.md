# PRD Quality Review — CircleGuard

## Overall verdict

CircleGuard has a specific containment thesis, a recognizable privacy posture, contiguous requirement IDs, and several useful quantitative targets. It is not yet decision-ready: the document presents a narrow Phase 1 while treating Phase 2/3 capabilities as current requirements, and its safety-critical status, identity, consent, and fence-resolution rules remain too ambiguous for UX, architecture, or story creation to implement consistently.

## Decision-readiness — broken

The PRD names choices such as a “pessimistic model” and separates delivery into three phases, but it does not expose the trade-offs, owners, or unresolved policy decisions behind them. Most importantly, a green-light decision cannot establish what is actually being authorized for Phase 1 because the journeys and Functional Requirements erase the phase boundary established in Product Scope.

### Findings

- **critical** The build target conflicts with the stated phase plan (§ Product Scope; § User Journeys; § Functional Requirements) — Phase 1 is described as the “Intelligence Core” with manual circle creation, while WiFi/BLE detection, LMS integration, gate validation, dashboards, lab integration, and reservation cancellation are assigned to Phase 2 or 3 yet appear as unqualified UJ-3–UJ-5 and FR-1, FR-3, FR-13–FR-17, and FR-21–FR-38. *Fix:* Give every UJ, FR, DR, NFR, and success criterion a phase/applicability label, then move non-MVP requirements into explicitly non-binding future-scope sections.
- **high** The status-policy decisions are stated without their contested consequences (§ UJ-2; FR-6–FR-10) — “promotes their Probable contacts to Suspect” and recursively fences another layer, but the PRD never records the chosen propagation depth, how cycles and repeated exposure are treated, or why this escalation policy is acceptable. *Fix:* Add a decision record and state-transition table covering triggers, traversal depth, precedence, re-exposure, cycles, overrides, and the public-health rationale for the selected policy.
- **high** Material tensions are presented as settled facts (§ Executive Summary; DR-2; DR-4; FR-15–FR-20) — mandatory gate enforcement, voluntary check-in, de-identification, biometrics, deletion, and the claim of anonymity create policy trade-offs, but there are no Open Questions or `[NOTE FOR PM]` callouts. *Fix:* Add a decision/open-question register with alternatives, consequences, accountable owner, and decision deadline for each material policy tension.

## Substance over theater — thin

The core graph-propagation idea is product-specific, and the performance/retention NFRs are more concrete than generic boilerplate. However, a large portion of the requirement inventory is not earned by the vision, journeys, success criteria, or the declared MVP, making the document read partly as a collection of platform features.

### Findings

- **high** Several capability blocks are detached from the product thesis (§ Functional Requirements, FR-24–FR-38) — dynamic questionnaires, certificate uploads to a Kubernetes PersistentVolume, runtime-defined RBAC, and full web/mobile parity appear without a supporting journey, success measure, or Phase 1 rationale. *Fix:* Trace each block to a validated problem and phase outcome, or move it to a future-capabilities appendix until Discovery justifies it.
- **medium** The user list behaves more like coverage furniture than decision-driving personas (§ Executive Summary, “Target Users”) — five audiences are named, but their needs, constraints, incentives, and conflicts are absent; “Faculty & Staff,” “Visitors & Providers,” and “University Administration” do not drive distinct product decisions. *Fix:* Collapse audiences that do not change requirements and define the few load-bearing personas by context, goal, constraint, and the decisions they influence.

## Strategic coherence — thin

The thesis is clear: combine campus infrastructure and validated check-ins with anonymous graph propagation to contain exposure faster than lab-confirmation workflows. The metric system and feature prioritization do not yet test that thesis cleanly, and the PRD does not protect against achieving speed by indiscriminately increasing disruption.

### Findings

- **high** The success metrics describe incompatible or incomplete clocks (§ Success Criteria, SC-1; FR-11; NFR-1) — containment is targeted “within 60 seconds,” alert dispatch within 30 seconds of a status change, and cascade computation within 1 second, without defining start/end events or whether delivery is included. *Fix:* Define one end-to-end containment SLI and its component SLIs, including trigger, completion event, percentile, test population, and delivery semantics.
- **high** The scorecard can reward over-fencing without measuring missed risk or harm (§ Success Criteria, SC-4) — “<15% of fenced individuals report no actual contact” relies on an undefined post-fence survey and is not paired with false-negative exposure, time unnecessarily fenced, academic disruption, or notification-delivery measures. *Fix:* Operationalize the denominator and evidence source, then add counter-metrics for missed contacts, unnecessary fence-hours, appeal/override rate, and delivery failure.
- **medium** The adoption goal is not aligned to the MVP mechanism (§ Success Criteria, SC-3; § Product Scope; UJ-3) — scheduled-class validation above 70% is measured in the first semester, while the smart schedule/WiFi prompt that enables UJ-3 is assigned to Phase 2 and Phase 1 only names manual circle creation. *Fix:* Choose an MVP adoption metric for the actual Phase 1 workflow or move both the journey and metric into the same later phase.

## Done-ness clarity — broken

Some requirements have useful numeric bounds, especially NFR-1, NFR-3, NFR-4, NFR-7, and QR expiry in FR-32. The central containment and privacy behaviors, however, do not have acceptance-ready semantics, and many functional requirements describe capabilities without observable completion conditions or failure behavior.

### Findings

- **critical** The contact and fence algorithm is not specified well enough to produce one correct implementation (§ UJ-1; FR-3; FR-6–FR-10) — “>15 min, <2m or closed space” has ambiguous Boolean logic, FR-6 fences “all graph-connected contacts” without depth or threshold, and release depends on undefined “active suspect paths.” *Fix:* Specify the edge-qualification formula, time-window anchoring, traversal algorithm, state transitions, path activation rules, idempotency, and worked examples for branching, cycles, repeated reports, negative tests, and re-exposure.
- **critical** The identity model contradicts its privacy claim (§ Executive Summary; DR-2; FR-17–FR-20) — IDs are called “non-reversible anonymous,” yet the system retains an identity mapping for de-identification and additionally “link[s] biometrics”; this is pseudonymity, with materially different consent, access, deletion, and breach consequences. *Fix:* Use accurate data classifications and define identifier derivation, salt/key custody, linkability, vault access approval, biometric purpose/consent/retention/deletion, audit events, and breach boundaries.
- **high** Many FRs have no verifiable outcome or defined terms (§ Functional Requirements, especially FR-5, FR-12, FR-21, FR-23, FR-34, FR-37, FR-38) — phrases such as “all persona types,” “conversion rates,” “granular permissions,” and “same functional coverage” allow materially different implementations to pass. *Fix:* Add acceptance criteria per FR with actor, precondition, observable result, error/empty state, permissions, and precise definitions for every reported measure.
- **high** Certificate upload is implementation-prescriptive but operationally incomplete (§ FR-27–FR-29) — requiring storage on “Kubernetes PersistentVolume” does not define allowed formats and limits, malware handling, encryption, retention, deletion, validation evidence, authorization, or audit behavior. *Fix:* Replace the storage-product mandate with product-level durability/security requirements and add testable upload, scanning, access, retention, deletion, and validation criteria.

## Scope honesty — broken

The three-phase outline is useful in intent, but the rest of the document does not honor it. There are no explicit non-goals, assumptions, or open items despite substantial dependence on campus infrastructure, public-health policy, user consent, and sensing accuracy.

### Findings

- **high** Omissions that materially define MVP behavior are left implicit (§ Product Scope, Phase 1) — the document does not say whether Phase 1 excludes automated sensing, gate enforcement, LMS writes, analytics, certificate management, questionnaires, biometrics, or web parity even though these appear later as requirements. *Fix:* Add an MVP Non-Goals section and mark each deferred feature `[NON-GOAL for MVP]` at its first potentially misleading mention.
- **high** The PRD contains numerous unmarked assumptions and no Assumptions Index (§ Success Criteria; UJ-3–UJ-5; NFR-2) — examples include achieving 70% validation, inferring sub-two-meter proximity from WiFi/BLE, availability of gate QR/NFC hardware, schedule/map/LMS access, 50,000 concurrent users, and Health Center capacity for manual actions. *Fix:* Tag each inference `[ASSUMPTION: …]`, index it, and attach a validation method, owner, and date.
- **high** No open-item mechanism exists for external dependencies or consent choices (§ Domain Requirements; FR-13–FR-17; FR-26–FR-29) — institutional authority to deny entry, data-sharing agreements, notification contact-data linkage, accessibility fallbacks, biometrics consent, and certificate provenance are neither decided nor acknowledged as open. *Fix:* Add Open Questions and `[NOTE FOR PM]` callouts, with dependency owner and a “must resolve before” milestone.

## Downstream usability — broken

IDs are contiguous and unique (SC-1–SC-5, UJ-1–UJ-6, DR-1–DR-6, FR-1–FR-38, NFR-1–NFR-8), which is a sound base. But downstream workflows cannot reliably extract MVP scope, domain meanings, or coverage because there is no glossary or traceability, the success table is structurally damaged, and several journeys lack a contextualized protagonist.

### Findings

- **high** Domain nouns drift across sections without a glossary (§ Executive Summary; § User Journeys; § Functional Requirements) — “Circle” variously means an interconnected contact group, a manually created event, a class cohort, and a graph edge; “Active,” “Fenced,” “Probable,” “Suspect,” and “Confirmed” mix access, fence, and health states; “anonymous,” “de-identification,” and identity mapping are used incompatibly. *Fix:* Add a canonical glossary and separate the contact-event/edge model, health status, fence status, and access decision into distinct defined concepts.
- **high** There is no source-extractable traceability from strategy to delivery (§ Success Criteria; § Product Scope; § User Journeys; § Functional Requirements) — no FR identifies its journey, success criterion, phase, or dependency, so UX, architecture, and story creation cannot determine which requirements form the MVP or whether a thesis outcome is covered. *Fix:* Add a compact traceability matrix mapping phase → outcome/SC → UJ → FR/DR/NFR, including explicit exclusions and external dependencies.
- **medium** Several journeys are actor-light or system-centered (§ UJ-2, UJ-4, UJ-5) — “Health Center” names an institution rather than an authorized role, UJ-4 begins with the system, and UJ-5 uses generic “Person,” so context and permissions do not survive extraction. *Fix:* Give every UJ a named role-based protagonist with goal, trigger, relevant context, success end state, and principal exception path.

## Shape fit — broken

CircleGuard is a high-stakes, multi-stakeholder campus health and access product that feeds UX, architecture, and implementation. Its shape is under-formalized where safety, privacy, consent, operational exceptions, and constraint traceability are load-bearing, while becoming prematurely implementation-specific in secondary areas.

### Findings

- **critical** Compliance is asserted rather than traced to product behavior (§ Domain Requirements, DR-1–DR-4; FR-17–FR-20; FR-26–FR-29) — “complies with FERPA” and “Right to be Forgotten” do not establish which data classes and institutional roles are governed, whether other regimes or campus policies apply, or how deletion interacts with medical, audit, and security records. *Fix:* Have the accountable privacy/legal owner define the applicable constraint set, then trace each requirement to data class, purpose, lawful/authorized basis, retention, deletion exception, access role, audit evidence, and acceptance test.
- **high** The journeys cover happy paths but omit foreseeable high-impact exceptions (§ User Journeys) — there is no path for declining sensing or check-in, disputing a Red gate result, losing connectivity or a phone, conflicting/late test results, inaccessible notification delivery, unauthorized de-identification, or Health Center overload. *Fix:* Add exception journeys for refusal/consent, appeal and override, offline/degraded operation, conflicting evidence, accessibility fallback, abuse, and operational surge.
- **medium** Technical implementation choices are fixed before product policies are resolved (§ FR-17, FR-28, FR-35, FR-37) — “backend REST API,” “Kubernetes PersistentVolume,” “JWT permission claims,” and “same Expo codebase” constrain architecture while the identity, consent, authorization, and phase decisions remain open. *Fix:* State product-level interface, durability, authorization, and parity outcomes in the PRD; move selected technologies and their rationale to architecture decisions after the governing product policies are settled.

## Mechanical notes

- SC, UJ, DR, FR, and NFR identifiers are contiguous and unique; there are no explicit cross-references to resolve, but the absence of references is itself the traceability gap noted above.
- The Success Criteria table has been flattened into alternating text lines, separating several targets from their measurements and making SC-1–SC-5 difficult to parse reliably.
- The Executive Summary user list and several journey steps contain broken line wrapping; “all while preserving individual anonymity” is detached from the Vision sentence.
- No inline `[ASSUMPTION]` tags or Assumptions Index exist, so an index roundtrip cannot be performed.
- UJ-1, UJ-3, and UJ-6 use a Student/Suspect role as protagonist; UJ-2, UJ-4, and UJ-5 do not carry an adequately specific protagonist inline.
- Missing load-bearing sections for this product shape are Non-Goals, Open Questions/decision owners, Glossary, per-requirement acceptance criteria, and strategy-to-requirement traceability.

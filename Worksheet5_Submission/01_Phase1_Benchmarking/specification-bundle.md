<!-- SOURCE: prd.md -->

# Product Requirements Document - CircleGuard

Author: [Redacted]

Date: 2026-03-16

## Executive Summary

Vision: A privacy-first contact tracing platform for university campuses that identifies interconnected contact groups (“Circles”), applies health fences when symptoms or confirmed cases arise, and enables rapid containment through recursive status promotion

all while preserving individual anonymity.

Differentiator: Unlike generic contact tracing apps, CircleGuard combines existing university infrastructure (WiFi APs, class schedules) with a human-validated check-in model and anonymous graph-based propagation to deliver containment speed that outpaces lab confirmation timelines.

Target Users: - Students — Primary population tracked and protected. - Faculty & Staff

Included in circle detection and fencing. - Visitors & Providers — Onboarded via temporary anonymous IDs. - Health Center Staff — Sole authority for de-identification and medical overrides. - University Administration — Dashboard consumers for policy decisions.

## Success Criteria

ID Metric Target Measurement

SC-1 Containment Speed Fence cascade triggers within 60

seconds of a symptom report

SC-2 Privacy Compliance Zero real-name exposure outside

Health Center vault

SC-3 Check-in Adoption >70% of scheduled class contacts

validated via check-in within first semester

Automated test of promotion engine

Penetration test on graph database

App analytics

ID Metric Target Measurement

SC-4 False Positive Rate <15% of fenced individuals report no

actual contact with suspect

SC-5 System Uptime 99.5% availability during academic

hours (7AM-10PM)

Post-fence survey

Infrastructure monitoring

## Product Scope

### Phase 1: MVP — The Intelligence Core

Status Promotion Machine (Suspect → Probable → Confirmed cascade).

Temporal graph with 14-day TTL edges.

Anonymous ID generation (salted hashing).

Manual circle creation and symptom self-reporting.

Multi-channel fence notifications (App Push, Email, SMS).

Health Center de-identification console.

### Phase 2: Growth — Spatial Intelligence

WiFi AP triangulation integration with University Map Service.

Bluetooth Low Energy (BLE) peer-to-peer proximity augmentation.

Smart check-in suggestions based on schedule + WiFi overlap.

Campus entry validation (Gatekeeper).

LMS integration for automatic “Remote Attendance” status.

### Phase 3: Vision — Full Ecosystem

Off-campus circle detection via P2P Bluetooth.

Health Dashboard with hotspot visualization and fence effectiveness analytics.

Lab API bridge for automated test result → status promotion.

Cross-campus interoperability for visiting students.

Class reservation auto-cancellation for fully fenced circles.

## User Journeys

### UJ-1: Student Self-Reporting Symptoms

Student opens CircleGuard app.

Student taps “Report Symptoms.”

System generates a Suspect status for the student’s anonymous ID.

System queries graph for all contacts within the last 14 days meeting the fence threshold (>15 min, <2m or closed space).

All identified contacts are fenced as Probable.

Notifications dispatched via App/Email/SMS to Probable contacts.

Student receives link to schedule a test.

### UJ-2: Health Center Confirms a Positive Test

Health Center receives positive test result.

Health Center enters result into CircleGuard linked to the anonymous ID.

System promotes all Probable contacts of this confirmed case to Suspect (testing required).

System recursively fences the contacts of newly promoted Suspects as Probable.

Health Center can de-identify specific anonymous IDs for medical outreach.

### UJ-3: Student Check-in to a Scheduled Class

Student arrives near classroom; WiFi/BLE detects proximity to the scheduled room’s AP.

System sends a smart prompt: “Are you in Room 302 for Calculus?”

Student confirms → Circle is created linking all confirmed attendees.

If student denies or is near multiple rooms → manual selection or dismissal.

### UJ-4: Sporadic Circle Detection

System detects two anonymous IDs in sustained BLE/WiFi proximity (>15 min,

<2m).

Neither has a matching schedule entry for this location.

System prompts both users: “You’ve been near another person for 15+ minutes. Register a sporadic circle?”

If confirmed → anonymous circle edge is created without revealing identities.

### UJ-5: Campus Entry Validation

Person (student, faculty, visitor) arrives at campus entry.

Person scans QR code or NFC tag via CircleGuard app.

System checks anonymous ID status: if Active → Green (Entry allowed); if Fenced → Red (Entry denied, remote alternatives provided).

Visitors without an account are prompted to register a temporary anonymous ID.

### UJ-6: Fence Resolution via Negative Test

Suspect receives a negative test result.

Health Center enters result into CircleGuard.

System dissolves the fence for the Suspect.

System re-evaluates all downstream contacts — if no other Suspect paths remain, their fences dissolve.

Notifications sent confirming fence release.

## Domain Requirements (EdTech / University Health)

### Privacy Compliance

DR-1: System complies with FERPA (Family Educational Rights and Privacy Act) for student data.

DR-2: All contact graph data uses non-reversible anonymous IDs (salted hashing). Real identity mapping stored in a separate, access-controlled vault accessible only to authorized Health Center personnel.

DR-3: Contact data older than 14 days is automatically purged from the graph database.

DR-4: Users can request complete deletion of their data (“Right to be Forgotten”) at any time.

### Accessibility

DR-5: App and web interfaces comply with WCAG 2.1 AA accessibility standards.

DR-6: All notifications are available in at least 2 channels (visual + text-based) for accessibility.

## Functional Requirements

### Contact Detection & Circle Management

FR-1: Users can check in to a scheduled class via an explicit 1-tap confirmation prompt triggered by WiFi/BLE proximity detection.

FR-2: Users can manually create a circle for unscheduled meetings. Professors/Admins must have a “Circle Dashboard” displaying event details, active participant lists, capacity counters, manual addition capabilities, and a scannable QR code.

FR-3: System detects sustained proximity (>15 minutes within <2 meters or shared closed space) and suggests sporadic circle registration without revealing personal data.

FR-4: Circles are stored as edges in a temporal graph with a 14-day TTL.

FR-5: System supports circle creation for all persona types.

### Status Promotion & Fencing

FR-6: When a user self-reports symptoms, the system assigns Suspect status and fences all graph-connected contacts as Probable.

FR-7: When a Suspect is confirmed positive, the system promotes their Probable contacts to Suspect and recursively fences the new Suspects’ contacts as Probable.

FR-8: Fences remain active for the full 14-day window (pessimistic model) unless overridden by a negative test result or medical override.

FR-9: Health Center can dissolve a fence by submitting a verified negative test result.

FR-10: When a fence is dissolved, the system re-evaluates all downstream contacts and releases those with no remaining active suspect paths.

### Notifications & Academic Integration

FR-11: Fence alerts are dispatched within 30 seconds of a status change via App Push, Email, and SMS simultaneously.

FR-12: Fence notifications include: reason, recommended action, and direct links to resources.

FR-13: System flags fenced students for “Remote Attendance” status in the University LMS.

FR-14: If all members of a class circle are fenced, the system triggers automatic cancellation of the class room reservation.

### Campus Entry & Visitor Management

FR-15: Users validate their entry status at campus gates via QR or NFC scan.

FR-16: Entry validation returns a binary Green/Red status without revealing medical details.

FR-17: Visitors and providers can register a temporary anonymous ID via a web-based onboarding flow. The system must provide a public-facing UI and a secure backend REST API endpoint for creating a local database account and linking biometrics.

### Privacy & Identity

FR-18: All contact graph operations use salted-hash anonymous IDs.

FR-19: The mapping between anonymous IDs and real identities is stored in a separate cryptographic vault accessible only to authorized Health Center personnel.

FR-20: De-identification requires explicit Health Center authorization and is audit-logged.

### Reporting & Analytics

FR-21: Health Dashboard displays active circles, fence counts, and conversion rates.

FR-22: Dashboard visualizes symptom hotspots by building and department.

FR-23: All dashboard data uses aggregated anonymous metrics.

### Dynamic Health Questionnaires

FR-24: Users complete a dynamic health questionnaire upon campus entry or when prompted.

FR-25: Questionnaire questions, options, and validation rules are stored in configuration tables and editable at runtime.

FR-26: Questionnaire responses are linked to the user’s anonymous ID.

### Certificate Management

FR-27: Users can upload test certificates (photo or PDF).

FR-28: Uploaded certificates are stored on Kubernetes PersistentVolume and linked to the user’s anonymous ID.

FR-29: Authorized staff can view and validate uploaded certificates.

### QR-Based Entry & Exit

FR-30: Users display a time-limited signed QR code for gate scanning.

FR-31: University staff use the mobile app to scan QR codes for campus entry/exit validation.

FR-32: QR tokens expire within 5 minutes and are cryptographically signed.

### Access Levels & Dynamic RBAC

FR-33: Roles are dynamically defined at runtime and stored in the relational database.

FR-34: Each role maps to a set of granular permissions.

FR-35: UI features are conditionally rendered based on JWT permission claims.

FR-36: An administrative interface allows authorized users to create, modify, and assign roles and permissions.

### Web Interface

FR-37: A web interface (same Expo codebase) supports manual operations including circle creation, symptom reporting, and fence management.

FR-38: The web interface provides the same functional coverage as the mobile app, minus proximity-based features.

## Non-Functional Requirements

NFR-1: The promotion cascade completes within 1 second for a graph of up to 10,000 active nodes as measured by automated load testing.

NFR-2: The system supports up to 50,000 concurrent users during peak academic hours.

NFR-3: API response times are under 200ms for 95th percentile under normal load.

NFR-4: System maintains 99.5% uptime during academic hours (7AM-10PM local time).

NFR-5: Anonymous ID hashing uses a cryptographically secure algorithm.

NFR-6: The identity vault is encrypted at rest and in transit, with access restricted to Health Center roles via RBAC.

NFR-7: All contact graph data older than 14 days is automatically purged within 1 hour.

NFR-8: The system supports horizontal scaling to accommodate enrollment growth of up to 5x without architectural changes.

---

<!-- SOURCE: ux-design-specification.md -->

# UX Design Specification — CircleGuard

Author: [Redacted]

Date: 2026-03-19

## Executive Summary

### Project Vision

A privacy-first contact tracing platform for university campuses that uses anonymous graph-based edge creation (WiFi/BLE/manual) to map contacts and apply proactive health fences instantly.

### Target Users

Students: Primary mobile app users.

Faculty & Staff: Users navigating room access and LMS integration.

Visitors/Providers: Guest users utilizing web-based onboarding, then transitioning to the native mobile app via Local Authentication (FaceID/TouchID).

Health Center & Admin Staff: Desktop users requiring data-dense dashboards.

### Key Design Challenges

Frictionless Checking-In: Students must check into circles with a single tap.

Visitor Mobile Handoff & Local Auth: Seamless funnel from web-registration to mobile app.

Privacy Trust & Anonymity: The UI must visually reinforce anonymity.

Cross-Platform Parity: Non-smartphone users need feature set parity through the web app.

High-Stress Workflows: Reporting symptoms or receiving a fence is stressful; the UX must guide users with clarity.

### Design Opportunities

Geospatial Hotspot Visualizations: Instant heatmaps of symptomatic clusters.

Ambient Intelligence: BLE and WiFi background UX that feels magical, not like surveillance.

## Core User Experience

### Defining Experience

The defining interaction is the Frictionless Status Check-in. The system must validate the user’s anonymous cryptographic identity instantly via QR code or background BLE/WiFi.

### Platform Strategy

Mobile App (iOS/Android): Primary platform. Leverages BLE, WiFi, Local Auth, Push.

Responsive Web App: Mandatory fallback. Full functional parity for manual operations.

### Effortless Interactions

Background Proximity: BLE/WiFi should register sporadic contacts without user intervention.

Biometric Web-to-App Handoff: Visitors upgrading from web to mobile should experience an automatic token transfer.

### Critical Success Moments

The “Green Screen” Entry: Scanning the QR token must yield a visually distinct “Green” state in under 200ms.

The Fence Notification: Alert delivered with clarity, detailing the Why and the exact Next Steps.

### Experience Principles

Privacy Above All Else: Every UI element must reinforce anonymity.

Zero-Friction Compliance: Interactions must take less than 5 seconds.

Calm Authority: Health alerts use calming typography and clear calls to action.

Radical Transparency: The UI must explain exactly when and why it is scanning.

## Desired Emotional Response

### Primary Emotional Goals

Safety & Trust: Users feel their data is secure and anonymous.

Relief & Clarity: Users feel informed rather than panicked.

Effortless Compliance: Campus safety feels automatic.

### Emotional Journey Mapping

Discovery/Onboarding: Skepticism → Trust.

Daily Interaction: Invisible and mundane.

Status Change (Fenced): Shock → Structured clarity.

Resolution: Relief and empowerment.

### Micro-Emotions

Trust vs. Skepticism, Calm vs. Anxiety, Confidence vs. Confusion.

### Design Implications

To build Trust → Use cryptographic-styled avatars. Display “Data expires in X days” badges.

To avoid Anxiety → Never use police or lockdown vernacular. Use “Remote Learning Recommended.”

To foster Efficiency → Massive thumb-friendly tap-targets.

### Emotional Design Principles

Never Alarm Unnecessarily.

Invisible is Better.

Control Over Data. Design System Foundation Design System Choice

### Themeable System: NativeWind (Tailwind CSS) paired with Headless UI primitives.

Rationale

Cross-Platform Consistency.

High Performance & Speed.

Brand Flexibility & Trust.

Accessibility via Headless UI.

### Implementation Approach

Mobile: React Native with NativeWind.

Web: React with Tailwind CSS and Radix UI.

Shared design-token schema as single source of truth.

## Core User Experience

### Defining Experience

The defining interaction of CircleGuard is the Frictionless Status Check-in. Whether a user is entering a high-traffic campus gate or joining a lecture hall circle, the system must validate their anonymous cryptographic identity instantly. This should feel like a “Magic Door.”

### User Mental Model

Users bring a mental model of “Seamless Transactional Access” (like Apple Wallet). They expect: - Zero Friction. - Predictability: “If I’m Green, I’m good.” - Privacy Assurance.

### Success Criteria

The “Walking Pace” Benchmark: Successful scan in under 200ms.

Ambient Awareness: Automatic proximity notification prompts.

Visual Clarity: High-contrast Green/Red feedback.

Offline Resiliency: QR tokens are valid without active cellular data.

### Novel UX Patterns

Proximity-Triggered Prompts: Background BLE/WiFi monitoring.

Anonymous Hash Avatars: Geometric patterns derived from the anonymous hash.

Biometric Web-to-App Handoff: Instant Upgrade flow from web to native via FaceID/TouchID.

### Experience Mechanics

Initiation: User approaches checkpoint. Proximity beacon pings the app.

Interaction: User taps notification. Biometric auth displays QR token.

Feedback: Haptic pulse and “Check” symbol. Phone shows “Success” animation.

Completion: Home screen status pulses to show “Active” in current circle.

## Visual Design Foundation

### Color System — “Stealth Privacy” Theme

Background: Deep Zinc (#18181B / Zinc-900).

Primary Action (Active): Cyan (#0891B2 / Cyan-600).

Accent/Alert (Fenced): Safety Orange (#EA580C / Orange-600).

Neutral/Surface: Steel Gray (#475569).

### Typography System

Headings: Outfit (Variable Sans).

Body: Inter.

Scale: 8pt modular scale.

### Spacing & Layout Foundation

8px Base Grid.

Medium-high density.

Card-Based UI.

### Accessibility Considerations

WCAG 2.1 AA (4.5:1 ratio).

Status never communicated by color alone.

Minimum 48x48px touch targets.

## Design Direction Decision

### Design Directions Explored

We explored 6 visual variations within the “Stealth Privacy” theme.

### Chosen Direction: The Mesh

This approach surfaces the anonymized contact graph as a living, background data layer.

### Design Rationale

Metaphorical Strength.

Ambient Awareness.

Stealth Aesthetic.

Engagement.

### Implementation Approach

Canvas/SVG Rendering for battery efficiency.

Cyan/Orange Integration.

The “Show Entry QR” action as a high-contrast floating button.

## User Journey Flows

### Frictionless Campus Entry

This flow must be executable in under 200ms to avoid gate congestion.

graph TD

A[Arrival at Gate] --> B{App State?} B -->|Active| C[Display Signed QR]

B -->|Fenced| D[Alert: Entry Denied]

C --> E[Scan at Terminal]

E -->|Valid| F[Success: Gate Opens]

E -->|Expired| G[Auto-Regenerate Token] G --> C

D --> H[Link to Remote Class]

### Symptom Self-Reporting

graph LR

A[Dashboard] --> B[Report Symptom]

--> C[Select Symptoms & Onset]

--> D[Review & Submit]

--> E[Status: Suspect]

--> F[Mesh Updates: Fencing Probable Contacts]

--> G[Health Center Notification]

### Smart Proximity Check-in

graph TD

A[Enter Classroom] --> B[WiFi/BLE Proximity Detected]

--> C[Push Prompt: Confirm Arrival?]

-->|Yes| D[Joined Circle: Calculus II]

-->|No| E[Ignore / Manual Selection]

--> F[Mesh Visualization Updates]

### Journey Patterns

Binary Success Feedback.

Progressive Exposure.

Ambient Status.

### Flow Optimization Principles

The 2-Tap Rule.

OLED Efficiency: Pure black (#000000) for large backgrounds.

Haptic Certainty.

### Professor Circle Dashboard

Layout: Dedicated dashboard for active classes.

Header Details: Date, Start/End Time, Circle ID, Room.

Tab Navigation: “COMUNIDAD” and “PARTICIPANTES.”

Metrics Bar: “Ingresados,” “Potenciales,” “Aforo máximo.”

Participant List: Scrollable list showing user names with visual status indicators.

Actions: “NUEVO ASISTENTE” button.

QR Display: Large scannable QR code for students to self-join.

### Sporadic Proximity Alert

Toast notification triggered by >15 min within <2 meters.

Action button to register circle without revealing PII.

### External User Registration

Flow: Public landing page -> Registration Form -> Data collection -> Account Verification -> Local DB Credential Generation.

Integration: Web-to-App Handoff support.

## Component Strategy

### Design System Components

Leverage NativeWind and Headless UI for a performant, accessible foundation.

### Custom Components

The Mesh Background

Purpose: Ambient status awareness.

Anatomy: Dark background with low-opacity SVG paths.

Interaction: Static or ultra-low frequency updates.

Rotating QR Token

Purpose: Secure, time-limited entry validation.

Anatomy: Centered QR code with countdown ring.

States: Valid (Cyan), Warning/Expiring (Orange), Invalid (Gray).

Hash Avatar

Purpose: Visual identity without personal data exposure.

Anatomy: Simple geometric pattern generated from the anonymous hash.

### Component Implementation Strategy

OLED Maximization.

Zero-Wake Backgrounds.

Accessibility: Status pulses with Haptic feedback and ARIA labels.

### Implementation Roadmap

Phase 1: Status Pulse Badge, Rotating QR Token, Primary Button.

Phase 2: Static Mesh BG, Circle Preview Card, Hash Avatar.

Phase 3: Dynamic Symptom Questionnaires, Alert Overlays.

## UX Consistency Patterns

### Button Hierarchy

Primary (Monolithic): Cyan-600 Background, White Text. 48px+ height.

Secondary (Structural): Steel Gray-500 Outline.

Tertiary (Minimal): Ghost/Text-only.

### Feedback Patterns

Success (Cyan Pulse): 400ms glow animation + check icon + Haptic.

Alert (Safety Orange Banner): Top-anchored persistent banner.

Syncing (Zinc Pulse): Subtle mesh node pulse.

### Form Patterns

Single-Column Only.

Micro-Forms (5-7 items per screen).

Progressive Disclosure.

### Navigation Patterns

“Home Anchor”: Persistent “Show QR” button.

Tabbed Navigation: Status (Home), Circles (Graph), Reporting.

Contextual Side-Nav for Admin.

## Responsive Design & Accessibility

### Responsive Strategy

Mobile-First: The primary entry point for 90% of users.

Desktop (Admin): Side-by-side analytics.

Web Fallback: Identical feature set.

### Breakpoint Strategy

Mobile (Default): < 640px.

Tablet (SM/MD): 640px - 1024px.

Desktop (LG): > 1024px.

### Accessibility Strategy (WCAG 2.1 AA)

AA contrast compliance.

Aria-labels for all icons.

48x48px minimum touch targets.

Full keyboard navigation and skip-links.

### Testing Strategy

Automated: Axe-core.

Manual: VoiceOver and TalkBack audits.

Visual: Color-blindness simulations.

### Implementation Guidelines

Relative Units (rem, %).

Semantic Structure.

Haptic Feedback APIs.

---

<!-- SOURCE: architecture.md -->

# Architecture Decision Document — CircleGuard

## Project Context Analysis

### Requirements Overview

Functional Requirements (23 FRs across 6 categories):

Category Count Architectural Impact

Contact Detection & Circle Mgmt

5 Graph DB, real-time proximity pipeline, temporal TTL

Status Promotion & Fencing 5 Recursive graph traversal engine, state machine

Notifications & Academic Integ.

Campus Entry & Visitor Mgmt

4 Event bus, multi-channel dispatcher, LMS batch synchronizer

3 Entry validation API, guest ID provisioning

Privacy & Identity 3 Dual-store architecture, cryptographic vault Reporting & Analytics 3 Aggregated read model, dashboard service

### Non-Functional Requirements (8 NFRs):

| NFR | Constraint | Architectural Driver |
| --- | --- | --- |
| NFR-1 | Cascade <1s for 10K nodes | Graph query optimization, in-memory caching |
| NFR-2 | 50K concurrent users | Horizontal scaling, load balancing |
| NFR-3 | API <200ms p95 | Low-latency service design |
| NFR-4 | 99.5% uptime (academic hours) | Redundancy, health checks |
| NFR-5 | SHA-256 + unique salt | Crypto module, key management |
| NFR-6 | AES-256 at rest, TLS 1.3 | Vault encryption, RBAC |
| NFR-7 | 14-day auto-purge within 1hr | TTL indexes, scheduled jobs |
| NFR-8 | 5x enrollment growth | Stateless services, horizontal DB scaling |

Scale & Complexity: - Primary domain: Full-stack (Mobile App + Backend APIs + Graph DB

+ External Integrations) - Complexity level: High - Estimated architectural components: 8-10 major services/modules

### Technical Constraints & Dependencies

University WiFi Infrastructure: Existing AP hardware.

University LMS: External system requiring synchronization.

Health Lab Systems: External API bridge.

FERPA Compliance: Strict data handling, audit logging.

Multi-Persona Support: Students, Faculty, Visitors, Providers.

### Cross-Cutting Concerns

Privacy/Anonymization — Anonymous IDs must be the only identifier in the contact graph.

Temporal TTL (14-day window) — Affects graph storage, notifications, reporting.

Audit Logging — FERPA requires tracing de-identification events.

Event-Driven Communication — Status changes trigger cascading effects.

Multi-Campus Potential — Architecture should support future multi-tenant deployment.

## Technology Stack

| Layer | Technology | Version |
| --- | --- | --- |
| Backend | Spring Boot | 4.0.3 (Java 21, Jakarta EE) |
| Graph DB | Neo4j + Spring Data | SDN 8.0.3 |
| Relational DB | PostgreSQL | 16.x |
| Mobile App | Expo (React Native) | SDK 55 (RN 0.83) |
| Auth | OpenLDAP | Existing infrastructure |
| Auth (Guests) | Local DB (PostgreSQL) | CompositeAuthenticationProvider |
| Deployment | Kubernetes | Self-hosted (existing) |
| Build | Gradle (Kotlin DSL) | Latest stable |

## Core Architectural Decisions

### Data Architecture

Decision Choice Rationale

Graph Modeling

Hybrid — SDN annotations + raw Cypher

Annotations for CRUD; Cypher for cascades

Relational JPA/Hibernate on PostgreSQL Identity vault, auth, audit logs Caching Two-tier: Caffeine (L1) + Redis (L2) L1 for hot path; L2 for cross-

service cache

Data Migration

Flyway (PostgreSQL) + Neo4j schema scripts

Version-controlled schema evolution

Event Store Apache Kafka Persistent event log for FERPA audit

### Authentication & Security

Decision Choice Rationale

Auth Chain CompositeAuthenticationProvider (LDAP

→ Local DB)

Community via LDAP; guests via JPA

Decision Choice Rationale

Token Format JWT (stateless, signed) Microservices validate independently

Authorization Dynamic RBAC Configurable roles and permissions

Graph Privacy Salted SHA-256 anonymous IDs Non-reversible; graph never

contains real IDs

Vault Encryption

AES-256 at rest, TLS 1.3 in transit Access restricted to Health

Center via RBAC

Audit Kafka audit topic + PostgreSQL audit table Immutable logging

### API & Communication Patterns

Decision Choice Rationale

External API REST + OpenAPI 3.x Mobile ↔ Backend; well-supported

Inter-Service Async

Apache Kafka events Persistent, fire-and-forget

Inter-Service Sync REST (Spring

WebClient)

API Gateway Nginx Ingress Controller

Error Handling RFC 7807 Problem

Details

Direct queries when immediate response needed

Routing, rate limiting, TLS, load balancing Standardized error responses

### Mobile Architecture (Expo/React Native)

Decision Choice Rationale

State Management

Redux Toolkit Complex state; robust DevTools

Navigation Expo Router (file-based) Convention over configuration API Layer RTK Query Auto-caching, optimistic updates,

polling

Push Notifications Self-hosted gateway Privacy-compliant; on-prem content

Platforms Expo Web — unified codebase

Single codebase for iOS, Android, Web

Offline Support Not required (Phase 1) Deferred to Phase 2

### Infrastructure & Deployment

| Decision | Choice | Rationale |
| --- | --- | --- |
| Runtime | Docker → Kubernetes | Existing infrastructure |
| CI/CD | Jenkins | Existing infrastructure |
| Monitoring | Prometheus + Grafana | K8s native metrics and dashboards |

| Decision | Choice | Choice | Rationale | Rationale |
| --- | --- | --- | --- | --- |
| Logging | ELK Stack | ELK Stack | Centralized log aggregation | Centralized log aggregation |
| Tracing | Actuator + Micrometer | Actuator + Micrometer | Distributed tracing across services | Distributed tracing across services |
| Local Dev | Docker Compose | Docker Compose | Neo4j, PostgreSQL, OpenLDAP, Redis, Kafka | Neo4j, PostgreSQL, OpenLDAP, Redis, Kafka |
| New Services |  |  |  |  |
| Service | Service | Technology | Technology | Purpose |
| Form Engine | Form Engine | Spring Boot + PostgreSQL | Spring Boot + PostgreSQL | Dynamic health questionnaires |
| File Storage | File Storage | Spring Boot + K8s PV | Spring Boot + K8s PV | Certificate upload (photo/PDF) |
| QR Token Service | QR Token Service | Embedded in Auth Service | Embedded in Auth Service | Time-limited signed QR tokens |

### Access Level Architecture

Mobile App (Expo):

Access Level Target Users Key Features

Campus User Students, Faculty, Visitors, Providers

Questionnaire, certificate upload, checkin, QR

University Staff

Gate Security, Health Center Scan QR, register symptomatic persons

Feature Gating: Conditional rendering based on JWT permission claims.

### Implementation Sequence

API Gateway (Nginx Ingress)

Auth Service (LDAP + Local DB + JWT)

Identity Vault Service (PostgreSQL)

Promotion Engine (Neo4j + Kafka)

Notification Dispatcher

Mobile App (Expo + Redux)

Entry Gateway Service

Health Dashboard

## Implementation Patterns & Consistency Rules

### Naming Patterns

Database (PostgreSQL): snake_case, plural tables. Database (Neo4j): PascalCase nodes, UPPER_SNAKE_CASE relationships, camelCase properties. API Endpoints: kebab-case, plural, versioned: /api/v1/{resource}. JSON Fields: camelCase. Kafka Topics:

{domain}.{entity}.{action} (e.g., promotion.status.changed, notification.fence.dispatched). Permissions: {domain}:{action} (e.g., circle:checkin, gate:scan). Code (Java): Packages:

com.circleguard.{service}.{layer}. Code (TypeScript): Components: PascalCase files. Utilities: camelCase files.

### Structure Patterns

Java Service Layout:

src/main/java/com/circleguard/{service}/

├── controller/服务

├── service/

├── repository/

├── model/

├── dto/

├── config/

├── event/

└── exception/

### Expo Project Layout:

src/

├── app/

├── components/

├── features/

├── hooks/

├── services/

├── store/

├── utils/

└── tests /

### Format Patterns

API Response Envelope:

{

"data": {},

"meta": { "timestamp": "ISO-8601", "requestId": "uuid" },

"errors": [{ "code": "FENCE_001", "message": "User is fenced" }]

}

### Error Response (RFC 7807):

{

"type": "/errors/fence-active", "title": "Entry Denied", "status": 403,

"detail": "User status is FENCED.", "instance": "/api/v1/entry/validate/abc123"

}

### Communication Patterns

Kafka Event Structure:

{

"eventId": "uuid",

"eventType": "promotion.status.changed", "timestamp": "ISO-8601",

"source": "circleguard-promotion-service", "payload": {},

"metadata": { "correlationId": "uuid", "version": 1 }

}

Authentication Flow: 1. Client sends credentials → Auth Service 2. Auth Service tries LDAP

→ falls back to Local DB 3. Returns JWT with { sub: anonymousId, permissions: [...], roles: [...] } 4. All subsequent requests include Authorization: Bearer {jwt} 5. Each microservice validates JWT signature locally (shared public key)

## Project Structure (Monorepo)

circleguard/

├── README.md

├── docker-compose.dev.yml

├── Jenkinsfile

├── api-specs/

├── k8s/

│ ├── nginx-ingress.yaml

│ ├── namespace.yaml

│ └── helm/

├── libs/

│ ├── circleguard-common/

│ ├── circleguard-security/

│ └── circleguard-events/

├── services/

│ ├── circleguard-auth-service/

│ ├── circleguard-promotion-service/

│ ├── circleguard-identity-service/

│ ├── circleguard-notification-service/

│ ├── circleguard-form-service/

│ ├── circleguard-file-service/

│ ├── circleguard-gateway-service/

│ └── circleguard-dashboard-service/

└── mobile/

└── circleguard-mobile/

### Architectural Boundaries

API Boundaries: Versioned REST endpoints with OpenAPI contracts.

Service Boundaries: Domain-segregated. Cross-domain data via Kafka or REST.

Library Boundaries: Shared code in libs/ as internal artifacts.

Data Boundaries: Each microservice owns its own schema.

## Validation Results

### Architecture Completeness Checklist

☒ Project context analyzed

☒ Technical constraints identified

☒ Critical decisions documented

☒ Directory structure defined

☒ Component boundaries established

Overall Status: READY FOR IMPLEMENTATION

### Confidence Level: HIGH

Gap Analysis

Minor Gap: JSON schema for Form Engine. Deferred to implementation.

Minor Gap: Exact Prometheus metric names. Standard Micrometer @Timed recommended.

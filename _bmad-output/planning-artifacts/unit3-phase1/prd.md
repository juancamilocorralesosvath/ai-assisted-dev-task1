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

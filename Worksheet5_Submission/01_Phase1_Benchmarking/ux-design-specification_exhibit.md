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

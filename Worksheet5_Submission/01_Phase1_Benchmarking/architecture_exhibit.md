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

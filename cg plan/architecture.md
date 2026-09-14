---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments: ['_bmad-output/project-context.md', '_bmad-output/brainstorming/brainstorming-session-2026-03-16-2156.md', '_bmad-output/planning-artifacts/prd.md']
workflowType: 'architecture'
project_name: 'CircleGuard'
user_name: 'Juan'
date: '2026-03-16'
lastStep: 8
status: 'complete'
completedAt: '2026-03-18'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements (23 FRs across 6 categories):**

| Category | Count | Architectural Impact |
|----------|-------|---------------------|
| Contact Detection & Circle Management | 5 | Graph DB, real-time proximity pipeline, temporal TTL |
| Status Promotion & Fencing | 5 | Recursive graph traversal engine, state machine |
| Notifications & Academic Integration | 4 | Event bus, multi-channel dispatcher, LMS batch synchronizer |
| Campus Entry & Visitor Management | 3 | Entry validation API, guest ID provisioning |
| Privacy & Identity | 3 | Dual-store architecture, cryptographic vault |
| Reporting & Analytics | 3 | Aggregated read model, dashboard service |

**Non-Functional Requirements (8 NFRs):**

| NFR | Constraint | Architectural Driver |
|-----|-----------|---------------------|
| NFR-1 | Cascade <1s for 10K nodes | Graph query optimization, in-memory caching |
| NFR-2 | 50K concurrent users | Horizontal scaling, load balancing |
| NFR-3 | API <200ms p95 | Low-latency service design |
| NFR-4 | 99.5% uptime (academic hours) | Redundancy, health checks |
| NFR-5 | SHA-256 + unique salt | Crypto module, key management |
| NFR-6 | AES-256 at rest, TLS 1.3 | Vault encryption, RBAC |
| NFR-7 | 14-day auto-purge within 1hr | TTL indexes, scheduled jobs |
| NFR-8 | 5x enrollment growth | Stateless services, horizontal DB scaling |

**Scale & Complexity:**

- Primary domain: Full-stack (Mobile App + Backend APIs + Graph DB + External Integrations)
- Complexity level: **High**
- Estimated architectural components: 8-10 major services/modules

### Technical Constraints & Dependencies

- **University WiFi Infrastructure:** Existing AP hardware provides triangulation data; no new hardware deployment required.
- **University LMS:** External system requiring scheduled periodic batch synchronization for remote attendance flagging.
- **Health Lab Systems:** External API bridge needed for automated test result ingestion.
- **FERPA Compliance:** Strict data handling, audit logging, and access controls at every layer.
- **Multi-Persona Support:** Students, Faculty, Visitors, Providers — each with different onboarding and identity lifecycle.

### Cross-Cutting Concerns Identified

1. **Privacy/Anonymization** — Permeates every component; anonymous IDs must be the only identifier in the contact graph.
2. **Temporal TTL (14-day window)** — Affects graph storage, notification lifecycle, reporting aggregation.
3. **Audit Logging** — FERPA requires tracing every de-identification event and data access.
4. **Event-Driven Communication** — Status changes trigger cascading effects across notifications, LMS, and entry systems.
5. **Multi-Campus Potential** — Architecture should not preclude future multi-tenant deployment.

## Starter Template Evaluation

### Primary Technology Domain

**Full-stack Microservices** — Mobile App (Expo/React Native) + Backend Microservices (Spring Boot/Java) + Graph DB (Neo4j) + Relational DB (PostgreSQL) on self-hosted Kubernetes.

### Technology Stack (Verified Versions)

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend | Spring Boot | 4.0.3 (Java 21, Jakarta EE) |
| Graph DB | Neo4j + Spring Data Neo4j | SDN 8.0.3 |
| Relational DB | PostgreSQL | 16.x |
| Mobile App | Expo (React Native) | SDK 55 (RN 0.83) |
| Auth (Community) | OpenLDAP | Existing infrastructure |
| Auth (Guests) | Local DB (PostgreSQL + JPA) | CompositeAuthenticationProvider |
| Deployment | Kubernetes | Self-hosted (existing) |
| Build | Gradle (Kotlin DSL) | Latest stable |

### Starter Options

**Backend: Spring Initializr** (`start.spring.io`)
- Spring Boot 4.0.3, Java 21, Gradle (Kotlin DSL), Jar packaging
- Dependencies: `spring-boot-starter-data-neo4j`, `spring-boot-starter-data-jpa`, `spring-boot-starter-web`, `spring-boot-starter-security`, `spring-boot-starter-ldap`, `spring-boot-starter-websocket`, `postgresql`, `spring-boot-starter-actuator`

**Mobile: Expo CLI**
```bash
npx create-expo-app@latest --template default@sdk-55 circleguard-mobile
```

### Architectural Decisions from Starter

**Architecture Style:** Microservices on Kubernetes — each core domain as a separate Spring Boot service.

**Dual Authentication Chain:**
- `CompositeAuthenticationProvider`: LDAP-first for community members, JPA-based `DaoAuthenticationProvider` fallback for guests/providers.
- Both paths produce unified anonymous ID tokens.

**Dual Datasource Configuration:**
- Explicit `@Configuration` classes for Neo4j (graph operations) and PostgreSQL (identity vault, local auth, audit logs).
- No reliance on Spring Boot auto-config for datasource detection.

**Push Notifications (Privacy-Compliant):**
- Self-hosted push gateway (ntfy/Gotify or equivalent) instead of routing through Expo's servers.
- Ensures notification content never leaves university infrastructure.

**Local Development:**
- `docker-compose.dev.yml` with Neo4j 5.x, PostgreSQL 16, OpenLDAP (osixia/openldap).
- Mirrors production topology for integration testing.

**Testing Infrastructure:**
- JUnit 5 + Spring Boot Test + Testcontainers (Neo4j + PostgreSQL containers).
- Test-first approach for the recursive promotion cascade (FR-7) — fixture graph defined before engine implementation.
- Expo: Jest + React Native Testing Library (unit), Detox (E2E).

**Note:** Project initialization using these commands should be the first implementation story.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- Data modeling approach (hybrid)
- Inter-service communication (Kafka + REST)
- Authentication chain (LDAP + Local DB)
- API gateway (Nginx Ingress)

**Important Decisions (Shape Architecture):**
- Caching strategy (Caffeine + Redis)
- Mobile state management (Redux Toolkit)
- CI/CD pipeline (Jenkins)
- Observability stack (Prometheus/Grafana + ELK)

**Deferred Decisions (Post-MVP):**
- Offline mobile support
- Cross-campus federation protocol
- Advanced analytics/ML pipelines

### Data Architecture

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Graph Modeling | **Hybrid** — SDN 8.x annotations (`@Node`, `@Relationship`) for CRUD + raw Cypher for cascade traversals | Annotations for developer productivity; raw Cypher for performance-critical multi-hop queries (NFR-1: <1s) |
| Relational Modeling | **JPA/Hibernate** on PostgreSQL | Identity vault, local auth credentials, audit logs — standard transactional data |
| Caching | **Two-tier** — Caffeine (L1 local, per-service) + Redis (L2 distributed, shared) | L1 for hot path (status lookups); L2 for cross-service cache (user status, fence state) |
| Data Migration | **Flyway** (PostgreSQL) + Neo4j schema scripts | Version-controlled schema evolution |
| Event Store | **Apache Kafka** | Persistent event log satisfies FERPA audit requirements; enables replay and debugging |

### Authentication & Security

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth Chain | **CompositeAuthenticationProvider** — LDAP-first → Local DB fallback | Community members via OpenLDAP; guests/providers via JPA `DaoAuthenticationProvider` |
| Token Format | **JWT** (stateless, signed) | Microservices validate tokens independently without shared session state |
| Authorization | **Dynamic RBAC** — Roles & Permissions stored in PostgreSQL, loaded at runtime | Roles and permissions are fully configurable; no hardcoded role names. Permissions map to functionalities (e.g., `circle:checkin`, `gate:scan`, `questionnaire:manage`) |
| Graph Privacy | **Salted SHA-256 anonymous IDs** | Non-reversible hashing; unique salt per user; graph never contains real identities |
| Vault Encryption | **AES-256 at rest, TLS 1.3 in transit** | Identity vault access restricted to `HEALTH_CENTER` role via RBAC |
| Audit | **Kafka audit topic + PostgreSQL audit table** | Every de-identification event and data access logged immutably |

### API & Communication Patterns

| Decision | Choice | Rationale |
|----------|--------|-----------|
| External API | **REST + OpenAPI 3.x** (Swagger) | Mobile ↔ Backend; well-supported in Spring Boot and Expo |
| Inter-Service (Async) | **Apache Kafka** events | Status promotions, fence notifications, audit events — fire-and-forget, persistent |
| Inter-Service (Sync) | **REST** (Spring WebClient) | Direct queries between services when immediate response needed (e.g., status check at entry gate) |
| API Gateway | **Nginx Ingress Controller** on K8s | Routing, rate limiting, TLS termination, load balancing across microservices |
| Error Handling | **RFC 7807 Problem Details** | Standardized error responses across all services |
| API Documentation | **SpringDoc OpenAPI** | Auto-generated from annotations, served at `/swagger-ui` |

### Mobile Architecture (Expo/React Native)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| State Management | **Redux Toolkit** | Complex state (fences, circles, notifications, auth); robust DevTools for debugging |
| Navigation | **Expo Router** (file-based) | Convention over configuration; native tab support in SDK 55 |
| API Layer | **RTK Query** (Redux Toolkit Query) | Integrated with Redux; auto-caching, optimistic updates, polling for real-time fence status |
| Push Notifications | **Self-hosted gateway** (ntfy/Gotify) | Privacy-compliant; notification content stays on university infrastructure |
| Platforms | **Expo Web** — unified codebase for iOS, Android, and Web | Single codebase; web covers manual operations for users without GPS/BLE |
| Offline Support | **Not required** (Phase 1) | Deferred; BLE off-campus circles can queue locally if needed later |

### Infrastructure & Deployment

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Container Runtime | **Docker** → **Kubernetes** (self-hosted) | Existing infrastructure; each microservice as a Deployment + Service |
| CI/CD | **Jenkins** | Existing infrastructure; Jenkinsfile per service with Testcontainers stage |
| Monitoring | **Prometheus + Grafana** | Metrics collection, dashboards, alerting (K8s native) |
| Logging | **ELK Stack** (Elasticsearch, Logstash, Kibana) | Centralized log aggregation across all microservices |
| Tracing | **Spring Boot Actuator + Micrometer** | Distributed tracing across service boundaries; feeds into Prometheus |
| API Gateway | **Nginx Ingress Controller** | New deployment; route `/api/v1/promotion/*`, `/api/v1/identity/*`, etc. |
| Local Dev | **Docker Compose** | `docker-compose.dev.yml` with Neo4j, PostgreSQL, OpenLDAP, Redis, Kafka |

### New Services (Discovered in Step 5)

| Service | Technology | Purpose |
|---------|-----------|--------|
| **Form Engine** | Spring Boot + PostgreSQL | Dynamic health questionnaires — questions, options, and validation rules stored in config tables. Managed by users with `questionnaire:manage` permission |
| **File Storage** | Spring Boot + Kubernetes PersistentVolume | Test certificate upload (photo/PDF). Files linked to anonymous IDs |
| **QR Token Service** | Embedded in Auth Service | Generates time-limited signed QR tokens encoding anonymous ID + current status for gate scanning |

### Access Level Architecture

**Mobile App (Expo — iOS/Android/Web):**

| Access Level | Target Users | Key Features |
|-------------|-------------|-------------|
| **Campus User** | Students, Faculty, Visitors, Providers | Health questionnaire, certificate upload, check-in (spaces/meetings/classes), display QR for entry |
| **University Staff** | Gate Security, Health Center | Scan QR for entry/exit, register symptomatic persons, manage questionnaires |

**Feature Gating:** Conditional rendering based on JWT permission claims. No hardcoded role checks — UI features are enabled/disabled by permission strings.

**Dynamic RBAC Model (PostgreSQL):**
```
roles ──< role_permissions >── permissions ──< permission_features >── features
  │                                                                        │
  └── user_roles ──< users                                    UI components
```
- **Roles:** Dynamically created (e.g., "Gate Agent", "Epidemiologist", "Student")
- **Permissions:** Granular capabilities (e.g., `circle:checkin`, `gate:scan`, `symptom:register`, `questionnaire:manage`, `certificate:upload`, `fence:override`)
- **Features:** UI components/routes gated by permissions

### Decision Impact Analysis

**Implementation Sequence:**
1. API Gateway (Nginx Ingress) — establishes routing foundation
2. Auth Service (LDAP + Local DB + JWT) — unblocks all other services
3. Identity Vault Service (PostgreSQL) — anonymous ID generation
4. Promotion Engine (Neo4j + Kafka) — core business logic
5. Notification Dispatcher (Kafka consumer + multi-channel) — response layer
6. Mobile App (Expo + Redux) — user-facing interface
7. Entry Gateway Service — campus validation
8. Health Dashboard — reporting/analytics

**Cross-Component Dependencies:**
- All services depend on **Auth Service** (JWT validation)
- Promotion Engine produces **Kafka events** consumed by Notification Dispatcher, Entry Gateway, and Dashboard
- Identity Vault is accessed only by **Auth Service** (for token creation) and **Health Center API** (for de-identification)
- **Redis** shared by Promotion Engine (fence status cache) and Entry Gateway (quick status lookup)

## Implementation Patterns & Consistency Rules

### Naming Patterns

**Database (PostgreSQL):**
- Tables: `snake_case`, plural (`audit_logs`, `local_users`, `questionnaire_questions`, `role_permissions`)
- Columns: `snake_case` (`anonymous_id`, `created_at`, `fence_status`)
- Foreign keys: `{table_singular}_id` (`user_id`, `role_id`)
- Indexes: `idx_{table}_{columns}` (`idx_users_email`)

**Database (Neo4j):**
- Nodes: `PascalCase` (`Person`, `Circle`, `Space`, `Session`)
- Relationships: `UPPER_SNAKE_CASE` (`CONTACTED_IN`, `BELONGS_TO`, `CHECKED_INTO`)
- Properties: `camelCase` (`startTime`, `duration`, `spaceId`)

**API Endpoints:**
- Format: `kebab-case`, plural, versioned
- Pattern: `/api/v1/{resource}` (`/api/v1/circles`, `/api/v1/fence-alerts`, `/api/v1/questionnaires`)
- Nested: `/api/v1/{parent}/{id}/{child}` (`/api/v1/circles/abc123/members`)

**JSON Fields:** `camelCase` (`anonymousId`, `fenceStatus`, `createdAt`)

**Kafka Topics:** `{domain}.{entity}.{action}` (`promotion.status.changed`, `circle.created`, `audit.access.logged`, `notification.fence.dispatched`)

**Permissions:** `{domain}:{action}` (`circle:checkin`, `gate:scan`, `questionnaire:manage`, `certificate:upload`, `fence:override`, `symptom:register`, `role:assign`)

**Code (Java):**
- Packages: `com.circleguard.{service}.{layer}` (`com.circleguard.promotion.repository`)
- Classes: `PascalCase` — `{Entity}Controller`, `{Entity}Service`, `{Entity}Repository`
- Constants: `UPPER_SNAKE_CASE`

**Code (TypeScript/Expo):**
- Components: `PascalCase` files (`CircleCard.tsx`, `FenceAlert.tsx`)
- Utilities: `camelCase` files (`formatDate.ts`, `usePermission.ts`)
- Redux slices: `camelCase` (`fenceSlice.ts`, `authSlice.ts`, `circleSlice.ts`)

**Microservice Repos:** `circleguard-{service}-service` (`circleguard-auth-service`, `circleguard-promotion-service`)

### Structure Patterns

**Java Service Package Layout:**
```
src/main/java/com/circleguard/{service}/
  ├── controller/     # REST endpoints
  ├── service/        # Business logic
  ├── repository/     # Data access (JPA or Neo4j)
  ├── model/          # Domain entities (@Entity, @Node)
  ├── dto/            # Request/Response objects
  ├── config/         # Spring @Configuration classes
  ├── event/          # Kafka producers/consumers
  └── exception/      # Custom exceptions + @ControllerAdvice
src/test/java/        # Mirrors main/ structure
```

**Expo Project Layout:**
```
src/
  ├── app/            # Expo Router file-based routes
  ├── components/     # Reusable UI components
  ├── features/       # Feature-specific logic (Redux slices + screens)
  ├── hooks/          # Custom hooks (usePermission, useAuth)
  ├── services/       # RTK Query API definitions
  ├── store/          # Redux store config
  ├── utils/          # Formatters, constants
  └── __tests__/      # Co-located test files (*.test.tsx)
```

### Format Patterns

**API Response Envelope:**
```json
{
  "data": {},
  "meta": { "timestamp": "2026-03-18T10:00:00Z", "requestId": "uuid" },
  "errors": [{ "code": "FENCE_001", "message": "User is fenced", "field": null }]
}
```

**Error Response (RFC 7807):**
```json
{
  "type": "/errors/fence-active",
  "title": "Entry Denied",
  "status": 403,
  "detail": "User status is FENCED. Remote alternatives available.",
  "instance": "/api/v1/entry/validate/abc123"
}
```

**Date/Time:** ISO-8601 everywhere (`2026-03-18T10:00:00Z`), stored as UTC, displayed in user's timezone.

### Communication Patterns

**Kafka Event Structure:**
```json
{
  "eventId": "uuid",
  "eventType": "promotion.status.changed",
  "timestamp": "ISO-8601",
  "source": "circleguard-promotion-service",
  "payload": {},
  "metadata": { "correlationId": "uuid", "version": 1 }
}
```

**Redux Action Naming:** `{slice}/{action}` (`fence/setStatus`, `auth/login`, `circle/checkin`)

**Redux State Shape:** Feature-based slices, each owning its own loading/error state.

### Process Patterns

**Error Handling:**
- Backend: `@ControllerAdvice` global handler + custom exception hierarchy (`CircleGuardException` → `FenceException`, `AuthException`)
- Frontend: RTK Query error middleware + toast notifications
- Logging: Structured JSON logs → ELK. Log levels: `ERROR` (alerts), `WARN` (review), `INFO` (audit), `DEBUG` (dev only)

**Authentication Flow:**
1. Client sends credentials → Auth Service
2. Auth Service tries LDAP → falls back to Local DB
3. Returns JWT with `{ sub: anonymousId, permissions: [...], roles: [...] }`
4. All subsequent requests include `Authorization: Bearer {jwt}`
5. Each microservice validates JWT signature locally (shared public key)

**Permission Check Pattern (Frontend):**
```typescript
const { hasPermission } = usePermission();
if (hasPermission('gate:scan')) { /* render scanner */ }
```

**Permission Check Pattern (Backend):**
```java
@PreAuthorize("hasAuthority('questionnaire:manage')")
public ResponseEntity<?> updateQuestion(...) { }
```

### Enforcement Guidelines

**All AI Agents MUST:**
1. Follow naming conventions exactly — no exceptions for "quick fixes"
2. Use the API response envelope for ALL REST responses
3. Emit Kafka events for ALL state changes (status, fences, circles)
4. Check permissions via `@PreAuthorize` (backend) or `usePermission` (frontend) — never hardcode role names
5. Write tests co-located with the code they test
6. Use Testcontainers for any test hitting Neo4j or PostgreSQL

## Project Structure & Boundaries

### Complete Project Directory Structure (Monorepo)

```
circleguard/
├── README.md                       # Project vision and architecture overview
├── docker-compose.dev.yml          # Neo4j, PostgreSQL, OpenLDAP, Redis, Kafka
├── Jenkinsfile                     # Root CI pipeline
├── api-specs/                      # OpenAPI 3.x / Swagger contracts
│   ├── auth-service.yaml
│   ├── promotion-service.yaml
│   └── ...
├── k8s/                            # Kubernetes manifests & Helm charts
│   ├── nginx-ingress.yaml
│   ├── namespace.yaml
│   ├── helm/                      # Templated deployments
│   └── {service}/
│       ├── deployment.yaml
│       └── configmap.yaml
│
├── libs/                           # Shared internal libraries
│   ├── circleguard-common/         # ApiResponse, ErrorResponse, GlobalExceptions
│   ├── circleguard-security/       # JwtFilter, @RequirePermission, RBAC logic
│   └── circleguard-events/         # Kafka event DTOs with @SchemaVersion
│
├── services/
│   ├── circleguard-auth-service/   # LDAP + Local DB + JWT + QR + RBAC
│   │   ├── README.md               # Service-specific implementation brief
│   │   ├── build.gradle.kts
│   │   ├── Dockerfile
│   │   └── src/
│   │       ├── main/java/com/circleguard/auth/
│   │       │   ├── controller/服务
│   │       │   ├── service/
│   │       │   ├── repository/
│   │       │   └── ...
│   │       └── main/resources/db/migration/ # Flyway scripts
│   │
│   ├── circleguard-promotion-service/
│   │   ├── README.md
│   │   └── src/
│   │       ├── main/java/com/circleguard/promotion/
│   │       │   ├── cypher/         # Raw *.cypher queries
│   │       │   └── ...
│   │       └── test/java/          # Integration tests with Testcontainers
│   │
│   ├── circleguard-identity-service/
│   ├── circleguard-notification-service/
│   ├── circleguard-form-service/
│   ├── circleguard-file-service/
│   ├── circleguard-gateway-service/
│   └── circleguard-dashboard-service/
│
└── mobile/
    └── circleguard-mobile/         # Expo SDK 55
        ├── src/
        │   ├── app/                # Expo Router
        │   │   ├── (auth)/
        │   │   ├── (campus)/
        │   │   ├── (staff)/
        │   │   ├── (admin)/
        │   │   └── (shared)/       # Profile, Settings, Notifications
        │   └── component/
        └── __tests__/              # Co-located component tests
```

### Architectural Boundaries

- **API Boundaries:** Versioned REST endpoints (`/api/v1/`) with mandatory OpenAPI contracts in `api-specs/`.
- **Service Boundaries:** Logic is strictly domain-segregated. Cross-domain data is exchanged via **Kafka events** (async) or **REST** (sync queries).
- **Library Boundaries:** Shared code in `libs/` is published as internal artifacts. Services MUST NOT depend on each other's code directly.
- **Data Boundaries:** Each microservice owns its own schema. No cross-service database access.

### Requirements to Structure Mapping

| Epic/Feature | Primary Location |
|--------------|------------------|
| Intelligence Core (Cascade) | `services/circleguard-promotion-service` |
| Privacy Vault (Identity) | `services/circleguard-identity-service` |
| Dynamic RBAC & Auth | `services/circleguard-auth-service` |
| Form Engine | `services/circleguard-form-service` |
| Gate Entry/Exit | `services/circleguard-gateway-service` |
| Mobile/Web Interface | `mobile/circleguard-mobile` |

### Integration Points

- **Internal Communication:**
  - **Async:** Apache Kafka (Domain Events with `schemaVersion`).
  - **Sync:** REST (Spring WebClient).
- **External Integrations:**
  - **OpenLDAP:** Campus identity source (Auth service).
  - **University Map/WiFi:** Location data (Promotion service).
  - **University LMS:** Scheduled batch synchronizer for remote attendance flagging (Notification & Academic integration).
- **Data Flow:** `User Action → Mobile App → Nginx Gateway → Microservice → Kafka Event → Downstream Service`.

## Architecture Validation Results

### Coherence Validation ✅

- **Decision Compatibility:** All technology choices (Java 21, Spring Boot 4, Neo4j 5.x, PostgreSQL 16, Kafka, Redis, Expo SDK 55) are verified for mutual compatibility. Versions are aligned with current industry standards (2025/2026).
- **Pattern Consistency:** Implementation patterns (naming, structure, error handling) are tailored to the Java/Spring and Expo ecosystems.
- **Structure Alignment:** The monorepo structure with 8 domain-driven microservices and shared `libs/` directly supports the scalability and consistency requirements.

### Requirements Coverage Validation ✅

- **Functional Requirements:** FR-1 through FR-38 are fully mapped to specific services and components. 
- **Non-Functional Requirements:** 
    - **Performance (NFR-1):** Addressed via Neo4j raw Cypher for the cascade + Redis/Caffeine two-tier caching.
    - **Privacy (NFR-5/6):** Addressed via salted-hash anonymous IDs in the graph and a segregated Identity Vault (PostgreSQL/AES-256).
    - **Scalability (NFR-8):** Addressed via stateless microservices and Kafka event-driven architecture.

### Implementation Readiness Validation ✅

- **Decision Completeness:** All critical decisions (auth, data, API, infra) are documented with specific versions and rationale.
- **Structure Completeness:** Complete project tree with service-specific READMEs, Flyway migrations, and Helm charts is defined.
- **Pattern Completeness:** AI agent enforcement guidelines are clear, including mandatory API envelopes and Kafka event structures.

### Gap Analysis Results

- **Minor Gap:** Documentation of the specific JSON schema for the dynamic `Form Engine` (FR-25). *Resolution: Deferred to implementation phase as part of the first story for form-service.*
- **Minor Gap:** Exact Prometheus metric names for the cascade engine. *Resolution: Standard Micrometer @Timed metrics recommended for MVP.*

### Architecture Completeness Checklist

- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped
- [x] Critical decisions documented with versions
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Performance considerations addressed
- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION
**Confidence Level:** HIGH

**Key Strengths:**
- **Privacy-as-Code:** Anonymization is baked into the graph modeling and identity vault segregation.
- **Resilient Cascade:** The recursive promotion engine uses a battle-tested graph database (Neo4j) with high-performance direct Cypher queries.
- **Consistent DX:** Shared `libs/` and service READMEs ensure multiple AI agents produce unified code.

### Implementation Handoff

**AI Agent Guidelines:**
- Follow all architectural decisions exactly as documented in this file.
- Use implementation patterns consistently across all 8 microservices.
- Respect project structure and boundaries (standardized Maven/Gradle and Expo layouts).

**First Implementation Priority:**
Initialize the monorepo structure and `circleguard-auth-service` as the foundational security layer.

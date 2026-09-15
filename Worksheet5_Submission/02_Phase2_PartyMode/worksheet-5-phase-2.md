# Worksheet 5 — §5.2 · Phase 2
## Multi-Agent Dispute Resolution — CircleGuard

**Fase:** Unit 3 — Fase 2
**Lead Engineer:** Julian
**Sesión:** `/bmad-party-mode --mode subagent` — John (PM), Sally (UX), Winston (Architect), Murat (Test Architect)
**Fecha:** 2026-09-14
**Keepsake de la sesión:** `_bmad-output/party-mode/2026-09-14-the-offline-gate.html`
**Briefing de convocatoria:** `_bmad-output/planning-artifacts/unit3-phase2/party-mode-briefing-offline-gate.md`
**Alcance respetado:** no se editaron `prd.md`, `ux-design-specification.md` ni `architecture.md`. No se generaron artefactos de §5.3.

---

## 1 · Chosen Collision

**Option A — The Offline Gate Collision (Probe 2).**
*UX Design Specification §2.3 / §4.1 vs. Architecture Decision Document, Mobile Architecture.*

**Why this one over Option B.** Option B (FR-18 anonymity vs. the Professor Dashboard) is a **single-axis contradiction**: one document forbids what another displays, and the resolution is a scoping decision — remove the names or authorise the exposure. It is severe, but it is *one* decision.

Option A is a **compound contradiction across three documents that no single reviewer can resolve**, and I chose it for four reasons:

1. **It has a phase-governance defect underneath it.** `prd.md:55` files Gatekeeper as Phase 2, twelve FRs carry no phase tag at all, and `architecture.md:238` has already scheduled the implementing service as build item 7 of 8. The contradiction is therefore *already being built*, which makes it urgent in a way Option B is not.
2. **One side of it is not a disagreement but an impossibility.** `architecture.md:206` places the signing key in the Auth Service; offline QR *generation* was never merely unsupported, it was physically unachievable. That only becomes visible when an architect is forced to answer where the key lives.
3. **It contains a measurement defect the other collision does not.** NFR-3 (`prd.md:194`) is a 200ms **server p95**; the UX spec spends the same 200ms on an end-to-end interaction covering roughly eight times the work. Two documents agree on a number while meaning different things — the most dangerous kind of false agreement.
4. **It has an undefined production state.** The gate flow at `ux:251-264` models only *Valid* and *Expired*. "No network" has no branch — **not even one that denies**. That is not a documentation gap; it is a system with a reachable state and no specified behaviour, which is exactly what a multi-agent review is for.

**Convergencia humano↔IA (Fase 1).** Option A es la única colisión cross-document hallada de forma independiente por el auditor humano y por la revisión automatizada: `human-audit-baseline.md` W1-UX (Cross-document, Critical), `bmad-review-report.md` convergent finding #5, y True Positive #6 en `worksheet-5-phase-1.md`.

---

## 2 · Target Document Clauses

**Document 1 — UX Design Specification** (`cg plan/ux-design-specification.md`)

> **"Offline Resiliency:** QR tokens are generated and valid even without active cellular data."
> — §2.3 Success Criteria, **ux:174**

> **"The 'Walking Pace' Benchmark:** Successful scan and validation in under 200ms."
> — §2.3 Success Criteria, **ux:171**

> "This flow is the primary daily interaction for all users. It must be executable in under 200ms to avoid gate congestion."
> — §4.1 Frictionless Campus Entry, **ux:249**

> Supporting commitments: "…sustained offline QR generation…" (**ux:25**) and "…enable ambient contact tracing and **offline entry tokens**." (**ux:47**)
> Gate flow diagram models exactly two scanner outcomes — `E -->|Valid|` and `E -->|Expired|` — with **no branch for absent network** (**ux:251-264**).

**Document 2 — Architecture Decision Document** (`cg plan/architecture.md`)

> "| Offline Support | **Not required** (Phase 1) | Deferred; BLE off-campus circles can queue locally if needed later |"
> — Mobile Architecture (Expo/React Native), **architecture.md:186**

> "**Deferred Decisions (Post-MVP):** — Offline mobile support"
> — Decision Priority Analysis, **architecture.md:141**

> "| QR Token Service | **Embedded in Auth Service** | Generates time-limited signed QR tokens…"
> — New Services, **architecture.md:206**

**Supporting exhibit — PRD** (`cg plan/prd.md`): Gatekeeper filed under Phase 2 (**prd.md:55**); FR-15/16/17 and FR-30/31/32 untagged (**prd.md:149-151, 174-176**); NFR-3 server budget (**prd.md:194**).

> ⚠️ **Citation note for the record.** The brief circulated to the agents carried shifted line numbers (ux:147/153/241, architecture:175, prd:77/225-229/265-269). Every claim was real; every anchor was wrong. The numbers above are verified against the files as committed.

---

## 3 · Agent Positions Summary
*(from the `/bmad-party-mode` debate)*

**John (PM Perspective — User Value & Scope).**
Ruled that the collision is downstream of a requirements failure: six entry FRs carry no phase tag while `architecture.md:238` has already scheduled the Entry Gateway Service as build item 7 of 8 — *"code doesn't read prd.md:55, it reads the implementation plan."* Tagged FR-15/16/30/31/32 as Phase 1 and FR-17 as Phase 2, then opened the hole in Sally's design that decided the fail-posture: Amber routes to a human, and at an unstaffed turnstile at 22:00 there is no human. Withdrew his own blanket fail-open ruling when shown it omitted a harm, and priced the resolution honestly — FR-13's LMS sync and Phase 2 BLE slip, and the gap goes to the sponsor as a scoped ask rather than absorbed into velocity.

**Sally / Freya (UX Perspective — Screen States & Friction).**
*(Ambos agentes UX están instalados; se convocó a **Sally** — `bmad-agent-ux-designer` — por el ángulo "Screen States & Friction" que pide la plantilla. Freya no fue convocada.)*
Conceded the defect in her own document before it was raised, and identified the actor no document had drawn: FR-31 puts the *staff scanner* on a mobile app too, so two devices can be offline independently at one gate. Designed the missing state — **Amber, Hold for Verification** — on the principle that *"Green is a claim about the present; Amber is what the system says when it can only speak for the past."* Reversed her absolute refusal of fail-open once shown that a jammed lane manufactures the very contact event the system detects, narrowing it to crowd-physics cases only, and then took the latency start-event definition back from both engineers on the grounds that a clock beginning at "first decoded frame" deletes the autofocus hunt the student actually experiences.

**Winston (Architect Perspective — Invariants & Feasibility).**
Reframed the axis and indicted his own document in the same breath: signed expiring tokens were *already* an offline verification primitive, so `architecture.md:186` was a statement about sync queues masquerading as one about verification — and `architecture.md:206` made offline QR generation **physically impossible**, leaving `ux:25`/`ux:47` *"dead on arrival."* Replaced his own credential design when its rotation seed was shown to permit unbounded re-minting, moving to 96 pre-minted tokens over 28,800 seconds that the device presents and cannot generate. Established that the real constraint is revocation lag rather than offline capability, and found the argument that broke the final deadlock: because FR-9/FR-10 dissolve fences, a stale list wrongly *denies* a medically cleared student, not merely admits a fenced one.

**Murat (Test Architect Perspective — Risk & ATDD Testability).**
Rejected the framing outright: the scope argument is secondary because **none of the four offline statements can fail a test** — no percentile, no instrument, no start or stop event, no network condition — and `ux:251-264` leaves a reachable production state with no defined expected result. Quantified the risk against `SC-4` (*"85% of every false-admit is a genuinely exposed person walking into a lecture hall"*), then publicly re-scored his own model when shown that queue congestion manufactures contact events, raising it from 8 to 16. Made the gate observable by requiring `lastRevocationSyncAt` on the wire — *"without that field the gate is unobservable and I can't test anything"* — and, by stress-testing the **fix** rather than the original spec, found the session's most dangerous defect in `prd.md:174`.

### 3.1 · Addendum — Ronda 6 (ronda acotada a los tres gaps de G3)

Convocada tras el anexo de trazabilidad, limitada a autoridad temporal, control de replay y rotación de clave. Produjo además el hallazgo de mayor riesgo de la sesión.

- **Winston.** Colapsó el Gap 1 mostrando que de tres relojes solo dos deciden: el del portador es un reloj de usabilidad, no de seguridad. Cedió su tolerancia de 60 s a **±30 s** (*"mi 60 estaba anclado en defaults de RFC 7519, OIDC y Envoy que existen porque esos sistemas leen un wall clock"*) y su solapamiento de claves de 72 h a **9 h**. Rechazó a propósito el arreglo real del replay y midió el agujero que compraba: *"un nonce de desafío-respuesta previene todo y cuesta un viaje óptico que revienta el p95 de 900 ms."*
- **Murat.** Prohibió leer el wall clock del SO en la ruta de decisión (`serverTime + Δmonotonic`, deriva < 1,5 s en 8 h) y demolió el detector de desfase de Winston con estadística: sobre una grilla de 300 s, el error de muestreo de la mediana a n=32 es **≈26 s** — el piso de ruido del tamaño del desfase a detectar. Lo reemplazó por el borde: **5 muestras consecutivas fuera de rango → `CLOCK_SUSPECT`**. Sobre replay: *"el requisito no es prevención, es detección del 100 % — y cualquiera que diga que lo prevenimos le está mintiendo al Health Center."* Puntuó en **25** el riesgo de captura de pantalla reenviada, por encima de todo lo discutido en cinco rondas.
- **Sally.** Reescribió el estado recuperable de error de reloj (*"«Clock unverified» es una línea de log disfrazada de UI"*) y disolvió la colisión de presupuesto entre los 600 ms de Winston y los ≤80 ms de Murat sin pedirle nada nuevo a nadie: el **Presence Ring** se lee dentro de la ráfaga de decodificación que el escáner ya captura durante los 240 ms de adquisición. **Latencia añadida: cero.** Con camino sin movimiento obligatorio (Reduce-Motion → par de dígitos rotativo, también phase-locked) *"porque si dejo que Reduce-Motion desactive el anillo en silencio, construí un bypass."*
- **John.** Cortó el nudo de presupuesto sacando liveness de Fase 1 con FR-40 (detección por huella de dispositivo) como cobertura — *"no voy a cambiar un problema resuelto por resolver parcialmente uno nuevo"* — razonamiento correcto contra el mecanismo de 600 ms que tenía sobre la mesa, y superado por el de Sally. Su frase de cierre de la sesión: *"cada resolución que tomé fue sobre un sistema que dice la verdad lentamente; esto es un sistema que dice una mentira perfectamente."*

---

## 4 · Final Engineering Resolution
*Lead Engineer verdict — Julian (revisado tras la ronda 6)*

> **Campus entry validation ships in Phase 1 as an offline-first decision path in which the scanner is the sole source of health status, the credential proves identity only and is bound to a live presentation, and every gate outcome is a function of two on-device integers — scanner revocation-sync age and clock-anchor state — with no network call anywhere on the decision path.**

I am adopting the room's engineering substance and overriding it on four points where it did not converge.

**What I adopt.** Offline verification is not a feature to be granted or deferred; it is a property the chosen cryptography already has, and `architecture.md:186` is struck because it answered a question nobody asked. The genuine constraint is revocation lag, and it is bounded at **p99 ≤ 60s with a hard maximum of 180s**, anchored to SC-1 (`prd.md:33`) on the principle that a gate may not be looser than the cascade feeding it. Scanner authority degrades in two steps: **authoritative to 120s**, **GREEN prohibited past 120s**, **RED prohibited past 900s** — the last step because FR-9/FR-10 make a stale list capable of denying a cleared student. Fail-posture is a function of gate class *and* staffing, not a global default. The 200ms figure is separated into the two budgets it was always conflating: NFR-3 stands untouched as a **server p95**, and the client carries its own decode-to-verdict budget of **400ms p95 / 650ms p99** offline. Temporal authority belongs to the Auth Service alone: time on the decision path is `serverTime + Δmonotonic`, and reading the OS wall clock there is prohibited.

**Where I override the room.**

1. **I take Murat's Gate Transit Time as a binding requirement, not a supplementary metric.** Decode-to-verdict is the engineering SLA; the wide clock from terminal arm to painted verdict — **900ms p95 / 1500ms p99** — is the number that governs throughput and the only one that describes what a student experiences. A spec that instruments only the tractable half is how "under 200ms" became unfalsifiable in the first place, and I will not accept that failure mode twice in the same document.
2. **I rule FR-30 (`prd.md:174`) a defect of record with priority above this collision.** Encoding "current status" in a pre-minted, platform-signed token produces a wrong admission that is cryptographically valid, indistinguishable from a correct one, and invisible to reconciliation. Every other control in this resolution catches stale *decisions*; none catches a stale *assertion we signed ourselves*. The credential carries identity, issuance and validity only.
3. **I reject John's NFR-9 as drafted.** It claims three tiers and specifies two, at boundaries (60s/180s) matching neither engineer. It also conflates the scanner's own sync clock with the end-to-end revocation SLA. The binding distinction: **120 is the only number evaluated on-device; 180 is an end-to-end budget evaluated by the test harness and never appears in scanner code.**
4. **I reverse the deferral of liveness to Phase 2.** John deferred it correctly on the information he had: the only mechanism on the table cost 600ms of observation, and his reasoning — *"I'm not trading a solved problem for a partly-solved new one"* — was right against *that* mechanism. Sally's Presence Ring asks for no new frames and no network round-trip: it reads the decode burst the scanner already captures during its 240ms acquisition. **Zero latency cost.** With the reason for deferral gone, what remains is that it is the highest measured risk in the session — **25**, above the staleness false-admit that governed every prior decision — and no other control touches it, because every other control catches *an old decision* and none catches *a valid token in the wrong hands*.

**Three consequences that override 4 drags with it, written so the result stays coherent:**

- **Winston's latency regression is void.** He had raised Gate Transit Time from 900 to 1200ms p95 to pay for *his* 600ms mechanism. With Sally's, that bill does not exist: **GTT stays at 900ms p95 / 1500ms p99**, and the AC-7a budgets stand as they were. All measurement is taken **with the mechanism active**, never disabled.
- **The fail-closed carve-out rises with it.** A liveness failure is **the single exception to fail-open and closes at every gate class, unstaffed perimeter included**. This does not contradict the matrix: the matrix governs *uncertainty*, and a detected static capture is not uncertainty, it is fraud.
- **FR-40 stays, it is not replaced.** John's detection covers exactly the residue the Presence Ring declares it does not catch — real-time video relay, which does present a genuinely animated screen. Prevention and detection are complementary; dropping FR-40 on winning liveness would leave the one surviving vector uncovered.

**What this permanently eliminates.** There is no longer a reachable gate state without a specified outcome; no requirement in the entry path without an integer, a percentile and an instrument; no untagged FR able to enter the implementation sequence; and no document in which 200ms means two different things. Where the resolution costs more than Phase 1 was funded for, that delta goes to the sponsor as a scoped ask — it is not absorbed silently.

**Residual risk accepted, with its bound:** real-time video relay between two people coordinated at the moment of presentation, and cross-gate replay with both scanners dark. Neither is preventable offline; both are detectable post-hoc — the first by device fingerprint in FR-40, the second at 100% within 300s of reconnection. **No document may claim they are prevented.**

### 4.1 · Decision table

| Decision | Value |
|---|---|
| Entry-validation phase | FR-15/16/30/31/32 **Phase 1**; FR-17 **Phase 2** |
| Gate behaviour, no network | On-device signature + `exp` + local list; **zero network calls on the decision path**; four terminal states |
| Max offline cache age | **120s** (GREEN cliff) · **900s** (RED cliff) |
| Fail-open / fail-closed | Perimeter unstaffed: AMBER **opens**, RED **denies**; ≥901s RED→AMBER, opens · Clinical: **closed**, escort · Interior: **closed-soft**, `gate:scan` override · Low-traffic doors: closed-soft / legacy badge · **Liveness failure closes at every class** |
| FR-32 revocation window | **p99 ≤ 60s**, hard max **180s**, poll **20s**, one dropped poll injected ≥5% of runs |
| 200ms — client or server | **Server** NFR-3 **200ms p95** (unchanged) · **Client** decode-to-verdict **400/650** offline, **700/1200** online · **Gate Transit Time 900/1500** |
| Credential | **28,800s**, 96 pre-minted tokens, **device cannot generate**, **no status field** |
| Temporal authority *(R6)* | Auth Service clock only; `serverTime + Δmonotonic`; OS wall clock **prohibited** on the decision path |
| Clock skew tolerance *(R6)* | **±30s** anchored · **±60s** fallback · **no verdict** if never synced |
| Clock-error detection *(R6)* | 5 consecutive out-of-range `scannerNow − iat` samples → `CLOCK_SUSPECT`, manual routing |
| Replay control *(R6)* | `jti` 16 bytes; retention **330s** anchored / **360s** fallback; ≈2.4 KB state; duplicate → **AMBER**; cross-gate offline **not preventable**, 100% detection within **300s** of reconnect |
| Key rotation *(R6)* | Period **720h**, overlap **9h**; `kid` mandatory; unknown `kid` → neither GREEN nor RED; key death via signed delta channel, **device-side expiry prohibited** |
| Holder binding *(R6)* | **Presence Ring**, phase from server-anchored time, read inside the existing decode burst; **zero added latency**; Reduce-Motion → rotating digit pair; failure fails **CLOSED** at every gate class |
| Amber ceiling | **≤5%** of presentations per rolling 15 min; breach auto-converts the lane to fail-open-with-audit |
| Throughput & dwell | ≥20 scans/min/lane nominal, ≥15 degraded; dwell alarm 5 min, fail 10 min |
| Reconciliation | ≤300s from radio-up, or alarm |

---

## 5 · Anexo de trazabilidad — Registro G1-G7

> **Nota de origen.** G1-G7 no está en el enunciado del Worksheet ni en las skills de BMad. Son las **compuertas de cierre que definimos nosotros** en `party-mode-briefing-offline-gate.md` §6.1, y este anexo las verifica contra lo que la sesión efectivamente produjo. Es un añadido propio, no un campo pedido por la plantilla.

**Veredicto de cierre: las siete cumplidas**, con G1 decidida y pendiente de aplicar el diff (fuera del alcance fijado: no editar archivos fuente).

| # | Compuerta | Estado | Cifra / evidencia |
|---|---|---|---|
| **G1** | Fase declarada | ⚠️ **Decidida, no aplicada** | FR-15/16/30/31/32 + liveness → Fase 1; FR-17 → Fase 2 |
| **G2** | Comportamiento offline especificado | ✅ **Cumplida** | 4 estados terminales × matriz clase/dotación |
| **G3** | Números, no adjetivos | ✅ **Cumplida** *(cerrada en ronda 6)* | caché 120/900 s · fail-posture por clase · desfase 30/60/sin-veredicto |
| **G4** | Ventana de riesgo de revocación | ✅ **Cumplida** | p99 ≤ 60 s · máx. duro 180 s |
| **G5** | Presupuesto de latencia desagregado | ✅ **Cumplida** | 3 relojes, todos con percentil |
| **G6** | Ruta de fallo diseñada | ✅ **Cumplida** | Amber + `CLOCK_SUSPECT` + `LIVENESS FAILED` |
| **G7** | Ediciones concretas | ✅ **Cumplida con una colisión resuelta** | texto `archivo:línea` para 12 cláusulas |

---

### G1 — Fase declarada · ⚠️ decidida, no aplicada

**Decisión:** el PRD es el documento único que declara la fase. FR-15, FR-16, FR-30, FR-31, FR-32 → **Fase 1**; FR-17 → **Fase 2**. `architecture.md` deja de declarar fase y pasa a **citarla**, mediante la regla de John: *"nada entra en la secuencia de implementación de `architecture.md:231-239` cuyo FR no lleve etiqueta Fase 1 en `prd.md`"*, con chequeo de CI que bloquea el merge.

**Evidencia — la contradicción se explicó, no solo se resolvió.** John: *"Aun si las hubieras etiquetado todas Fase 2, `architecture.md:238` ya puso Entry Gateway en el puesto 7 de 8. El código no lee `prd.md:55`, lee el plan de implementación."*

**Por qué no está cerrada:** el criterio de verificación de G1 es *"sin contradicción residual"* entre los tres archivos — es un criterio sobre el **estado de los archivos**. Bajo la instrucción de no editar las fuentes, la contradicción sigue literalmente en disco: `prd.md:55` sigue listando Gatekeeper bajo Fase 2. La decisión está completa y el texto de reemplazo existe (ver G7); **la verificación queda pendiente de la aplicación del diff**, que es alcance de otra fase.

### G2 — Comportamiento offline especificado · ✅

Existe comportamiento definido y observable para la puerta sin red, en **todas** las combinaciones. Cuatro estados terminales (GREEN / RED / AMBER / EXPIRED) y disposición por clase de puerta **y por estado de dotación** — la bifurcación que no existía en ningún documento.

**Criterio de verificación cumplido literalmente** — Murat puede escribir un `Then` que falla: *"N=120 → GREEN renderiza · **N=121 → GREEN no debe renderizar** · N=899, ID vallado → RED renderiza · **N=901, perímetro sin dotación → RED no debe renderizar; MANUAL, y la barrera se abre físicamente**."*

Y el requisito que hace la puerta observable: `lastRevocationSyncAt` en el evento `gate.decision.recorded` — *"sin ese campo en el cable la puerta es inobservable y no puedo testear nada; es un requisito, no telemetría."*

**Tiers de obsolescencia del escáner:**

| Antigüedad de sync `S` | Veredictos permitidos | Lectura |
|---|---|---|
| `S = 0 – 120 s` | GREEN · RED | Plenamente autoritativo. Sin banner. |
| `S = 121 – 900 s` | RED · AMBER | No puede afirmar el presente. Todavía puede denegar sobre lo que sabe. |
| `S ≥ 901 s` | AMBER | Demasiado obsoleto para denegar a un estudiante que quizá ya está liberado. |

**Guard de implementación:** 120 es el único número que el escáner lee jamás. 180 es un SLA end-to-end evaluado por el arnés de pruebas y **nunca** aparece en código de escáner — *"cualquier implementador que ponga 180 en código de escáner construyó la cosa equivocada."*

### G3 — Números, no adjetivos · ✅ (cerrada en ronda 6)

| Sub-requisito de G3 | Estado | Cifra acordada |
|---|---|---|
| Edad máxima de caché | ✅ | **120 s** (corte GREEN) · **900 s** (corte RED) |
| Política fail-open/fail-closed por tipo de puerta | ✅ | Perímetro sin dotación: AMBER abre / RED deniega · Clínica: cerrada · Interior: cerrada-blanda con override · **Liveness cierra en toda clase** |
| Tolerancia de desfase horario | ✅ *(cerrada en R6)* | **±30 s** anclado · **±60 s** fallback · **sin veredicto** si nunca sincronizó |

**Cómo estaba antes de la ronda 6 — el hallazgo del anexo.** La sala verificó `exp` en el dispositivo durante cinco rondas sin que nadie preguntara **de quién es el reloj**. El diseño final lo agravaba en lugar de mitigarlo: con un lote pre-acuñado de 96 tokens de `exp` = 300 s validados por un escáner sin red, no había ninguna autoridad temporal común. Un escáner con el reloj adelantado 6 minutos **rechaza todos los tokens válidos**; atrasado, **acepta tokens caducados**. Ambos fallos son silenciosos y se presentan como EXPIRED o GREEN legítimos. El guard de la línea base lo pedía explícitamente y había quedado sin cubrir:

> `authoritative time, allowed clock skew, regeneration behavior, recoverable clock-error state`
> — `review-edge-cases-bundle.json`, "Relojes de dispositivo y escáner desfasados"

**Cómo se cerró (ronda 6):**

| `scannerTimeSource` | Tolerancia | Ventana efectiva |
|---|---|---|
| `SERVER_ANCHORED` | **±30 s** | 360 s |
| `WALL_CLOCK_FALLBACK` | **±60 s** | 420 s |
| `NONE` (nunca sincronizó) | **sin veredicto** | GREEN irrenderizable |

Prevención: registrar `(serverTime, monotonicTick)` en cada contacto online y evaluar tiempo como `serverTime + Δmonotonic`; wall clock del SO **prohibido** en la ruta de decisión; deriva de cristal 10-50 ppm → **< 1,5 s sobre 8 horas a oscuras**. Detección: `CLOCK_SUSPECT` con **5 muestras consecutivas fuera de rango** (~15 s a 20 escaneos/min), tras el rechazo estadístico del detector por mediana — sobre una grilla de pre-acuñado de 300 s el error de muestreo a n=32 es ≈ 300/(2√32) ≈ **26 s**, del mismo tamaño que el desfase a detectar. **Ambas defensas quedan y no son redundantes:** el anclaje monotónico *previene* deriva; el detector de flujo `iat` *atrapa un ancla que ya nació mal*.

**Los dos guards satélite restantes, también cerrados en R6:**

- **Replay** — `jti` de 16 bytes, retención 330 s anclado / 360 s fallback, ≈2,4 KB de estado a 20 escaneos/min/carril (≤32 KB en ráfaga 10×), duplicado en la misma puerta → **AMBER** `REPLAY_SUSPECT`, nunca RED. Cross-gate con ambos escáneres a oscuras: **no prevenible**, detección **100 %** dentro de **300 s** de la reconexión. La caché sobrevive reinicio de app y de dispositivo; evicción solo por retención, nunca por presión de capacidad — *"desalojar una entrada no vencida es un bug de admisión, no una optimización de memoria."*
- **Rotación de claves** — periodo **720 h**, solapamiento **9 h** (= vida de la credencial, 8 h + 1 h de margen, no oscuridad del escáner). `kid` obligatorio; `kid` desconocido → ni GREEN ni RED (*"una clave desconocida es evidencia sobre mi flota, no sobre su salud"*). **Muerte de clave por el canal de delta firmado, jamás por calendario en dispositivo** — el anillo de claves viaja en el mismo delta firmado que la lista de revocación, así que *"«fresco en la lista» y «fresco en claves» son la misma condición por construcción"*.

### G4 — Ventana de riesgo de revocación · ✅

Ventana explícita y numérica: **p99 ≤ 60 s**, máximo duro **180 s** (cualquier muestra individual por encima rompe el build), intervalo de sondeo **20 s**, con un sondeo caído inyectado en ≥5 % de las corridas.

El 60 no es arbitrario — Winston lo ancló: *"`SC-1` en `prd.md:33` ya gasta 60 segundos del reporte de síntoma a la valla; esta institución ya puso precio a un minuto de no-vallado-todavía, y yo igualo ese precio, no lo duplico en silencio."*

**El residuo quedó escrito, no escondido** — Murat: *"un lote de 96 tokens de 28.800 s es funcionalmente idéntico a re-acuñar durante ocho horas; tu estudiante vallada en T0+60 sigue teniendo ~95 tokens sin caducar y criptográficamente perfectos. No eliminaste el residuo, le pusiste techo — que es el intercambio correcto, pero llamémoslo por su nombre."*

### G5 — Presupuesto de latencia desagregado · ✅ (resuelve E9)

Los 200 ms quedaron partidos en los tres presupuestos distintos que estaban fundidos en uno:

| Reloj | Alcance | Valor |
|---|---|---|
| **NFR-3** (`prd.md:194`) | Servidor, sin tocar | **200 ms p95**, APM |
| **Decode-to-Verdict** | Cliente: timestamp de captura del sensor → verdicto pintado | offline **400 / 650** · online **700 / 1200** |
| **Gate Transit Time** | Cliente: armado del terminal → verdicto, **incluye el barrido de enfoque** | **900 / 1500** |

**Ruta degradada declarada:** offline *es* la ruta degradada, y es la más rápida — Winston: *"los 200 ms end-to-end nunca fueron reales **online**; NFR-3 le da 200 ms p95 al servidor solo, y sumando el despertar de radio más el salto por Nginx a Redis estás en 400-600. Offline no es la amenaza a tus 200 ms, Sally. Es la única forma de conseguirlos."* Throughput degradado: **≥15** escaneos/min/carril frente a **≥20** nominal.

**Corrección de hecho registrada:** Winston corrigió su propio 120 ms de decodificación a **240 ms** tras benchmarks (Vision ~96 ms, ML Kit ~98 ms, **ZXing-CPP ~3.804 ms**), lo que convirtió en restricción arquitectónica la prohibición de ZXing en la ruta de escaneo.

**Nota post-ronda 6:** el Presence Ring se lee **dentro** de esos 240 ms de adquisición, de modo que GTT permanece en **900 / 1500** y la subida a 1200 ms que Winston había propuesto queda anulada.

### G6 — Ruta de fallo diseñada · ✅

Estado de UI para validación no concluyente: **Amber — Hold for Verification**, definido como *"Green es una afirmación sobre el presente; Amber es lo que el sistema dice cuando solo puede hablar del pasado."*

- **Copy:** terminal `"VERIFY MANUALLY"` + código de razón; dispositivo `"Status Unconfirmed — Last synced HH:MM"` con reintento manual.
- **Alternativa no cromática:** icono de reloj de arena (nunca check ni X) + etiqueta textual + contador numérico de obsolescencia — tres canales redundantes al color. Formato exigible: **segundos enteros, ≥16 pt, ≥4.5:1**, tras el veto de Murat a *"pintar un reloj de obsolescencia visible"* por inmensurable.
- **Fallback atendido:** carril secundario con dotación, **más** la bifurcación sin dotación que ningún documento tenía.
- **Límite de saturación:** Amber **≤5 %** de presentaciones por ventana móvil de 15 min — *"al 6 % tu único humano en la puerta **es** el torniquete"* — y comportamiento definido al superarlo: el carril se convierte automáticamente a fail-open-con-auditoría.
- **Estado de error de reloj (R6):** **"SCANNER CLOCK OFFSET — VERIFY MANUALLY"**, subtexto **"Measured offset: [N]s. Routing all scans to manual check until resynced."**, ≥16 pt, ≥4.5:1, con **icono distinto** (reloj-con-cuña, no el reloj de arena de obsolescencia) porque *"«mi reloj está mal» y «mi red está vieja» son problemas distintos con arreglos distintos"*. Lado portador: badge no bloqueante, sin rojo, sin "error" — **"Clock check: showing your correct pass despite device time drift. No action needed now."**
- **Estado de fallo de liveness (R6):** `LIVENESS FAILED` cierra en toda clase de puerta; es la única excepción a fail-open, porque *"una captura estática detectada es una señal de fraude, no un problema de conectividad."*

> **Corrección de ancla:** G6 cita `ux:429-437` para WCAG 2.1 AA, pero el archivo tiene **405 líneas**. La cláusula real es **`ux:217`** — *"Status is never communicated by color alone; every 'Active' (Cyan) or 'Fenced' (Orange) state is accompanied by distinctive icons and text labels"* — con AA 4.5:1 en **`ux:216`** y la estrategia en **`ux:389`**. El compromiso existe; el ancla del briefing estaba desplazada, igual que `prd.md:77`→**`:55`** y `architecture.md:175`→**`:186`** en G1.

### G7 — Ediciones concretas · ✅ (con una colisión resuelta)

Texto de reemplazo `archivo:línea` producido para doce cláusulas: `prd.md:55` (Gatekeeper movido de Fase 2 a Fase 1), FR-16 (tres estados), **FR-30** (identidad y validez solamente), FR-39 (nueva, postura de fallo), FR-40 (detección por huella de dispositivo, se mantiene), NFR-9 (nueva, lag de revocación), NFR-10 (nueva, throughput), `ux:171`, `ux:174`, `ux:249`, el mermaid completo de `ux:251-264`, y las cláusulas de ronda 6 (autoridad temporal, replay, rotación de clave, Presence Ring). El strike de `architecture.md:186` y `:141` está especificado.

**Dos defectos en los diffs, no en las decisiones — ambos adjudicados:**

1. **`ux:174` tenía dos textos en competencia.** El de John dice que los tokens son *"derived on-device"* — la palabra exacta que Winston eliminó y Murat vetó. El de Sally es correcto: *"el dispositivo **presenta** credenciales de este lote y **no puede generar** nuevas."* Aplicar el de John reabriría el agujero que cerró todo el rediseño. **Resolución: se usa el de Sally.**
2. **NFR-9 de John es incoherente** — declara tres niveles y especifica dos, en fronteras (60/180) que no son de ninguno de los dos ingenieros, y confunde el reloj de sincronía del escáner con el SLA end-to-end. Ambos ingenieros pidieron descartarlo. **Resolución: rechazado** (override 3 del Bloque 4). La frontera vinculante: **120 es el único número que el escáner lee jamás; 180 es un SLA evaluado por el arnés de pruebas y nunca aparece en código de escáner.**

---

## Puente a §5.3

| Campo de §5.3 | Fuente en este documento |
|---|---|
| `AD-n:` nombre de la decisión | Bloque 4, frase de veredicto |
| `Binds:` | Entry Gateway Service · app móvil del portador · app de escaneo del staff (FR-31) |
| `Prevents:` | Admisión de un portador `Fenced` con token pre-emisión; presentación de una captura estática |
| `Rule:` (sin lenguaje elástico) | Bloque 4 §4.1 — tabla de decisiones |
| `Trade-off:` | Riesgo residual aceptado: relay de video en vivo y replay cross-gate con ambos escáneres a oscuras |
| `Feature/Scenario/Given/When/Then` | G2 (cortes 120/121/899/901) · G3 (`CLOCK_SUSPECT`) · G4 (sondeo caído ≥5 %) |

**Estado:** §5.2 cerrado. Sin tocar `architecture.md`, `prd.md` ni `ux-design-specification.md`. Sin artefactos de §5.3.

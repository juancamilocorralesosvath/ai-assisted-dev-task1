# Briefing de Convocatoria — `bmad-party-mode`
## Colisión Option A: The Offline Gate Collision (UX §4.1 vs. Architecture p.31)

**Fase:** Unit 3 — Fase 2, Multi-Agent Dispute Resolution (Worksheet 5 §5.2)
**Producto:** CircleGuard
**Convocante:** Julian (Lead Engineer)
**Fecha:** 2026-09-14
**Estado:** BORRADOR PARA REVISIÓN HUMANA — no lanzar `/bmad-party-mode` hasta aprobación
**Revisión:** v2 — nombres de agentes verificados contra la instalación; §7 alineado al formato exacto del enunciado

---

## 0. Configuración verificada de esta instalación

Fuente: `_bmad/config.toml`, `_bmad/config.user.toml`, `.agents/skills/bmad-party-mode/{SKILL.md,customize.toml}`. Sin overrides en `_bmad/custom/` (no existe `bmad-party-mode.toml`).

### 0.1 Roster instalado — los nueve agentes del cuarto por defecto

| code | Nombre | Título | Icono | Módulo |
|---|---|---|---|---|
| `bmad-agent-analyst` | Mary | Business Analyst | 📊 | bmm |
| `bmad-agent-pm` | **John** | **Product Manager** | 📋 | bmm |
| `bmad-agent-ux-designer` | **Sally** | **UX Designer** | 🎨 | bmm |
| `bmad-agent-architect` | **Winston** | **System Architect** | 🏗️ | bmm |
| `bmad-agent-dev` | Amelia | Senior Software Engineer | 💻 | bmm |
| `wds-agent-freya-ux` | **Freya** | **WDS Designer** | 🎨 | wds |
| `wds-agent-saga-analyst` | Saga | WDS Analyst | 📚 | wds |
| `wds-agent-mimir-builder` | Mimir | WDS Builder | 🔨 | wds |
| `bmad-tea` | **Murat** | **Master Test Architect and Quality Advisor** | 🧪 | tea |

### 0.2 Sally o Freya: **son dos agentes distintos, y ambos están instalados**

El enunciado escribe "Sally / Freya" porque no sabe si tienes WDS. **Tú lo tienes** (`wds v0.4.3` preservado en Fase 1), así que ambos existen:

- **Sally** (`bmad-agent-ux-designer`, BMM) — *"Balances empathy with edge-case rigor... Speaks like a filmmaker pitching the scene before the code exists."*
- **Freya** (`wds-agent-freya-ux`, WDS) — *"Norse goddess of beauty, magic, and strategy... starts with WHY before HOW — design without strategy is decoration."*

**Decisión: usar Sally.** El cuerpo del enunciado (Fase 2, paso 3) nombra literalmente *"Winston (Architect), **Sally** (UX), John (PM), and Murat (Test Architect)"* — sin Freya. Y el ángulo que pide la plantilla para ese rol es **"Screen States & Friction"**, que es exactamente el registro de Sally (edge-case rigor sobre estados de pantalla), no el de Freya (estrategia y el *por qué* antes del *qué*).

> **Opción descartada:** convocar a las dos. Freya aportaría un choque interno de diseño interesante, pero la plantilla §5.2 tiene **un solo campo** para el rol UX. Dos voces de diseño obligan a fundir posiciones al transcribir, que es justo donde se pierde el argumento. Si aun así la quieres, súmala como voz invitada y transcribe solo la posición de Sally en el worksheet.

### 0.3 Tres condiciones de la instalación que hay que forzar al lanzar

| # | Condición por defecto | Problema | Acción |
|---|---|---|---|
| C1 | `default_party = ""` → el cuarto por defecto son **los 9 agentes instalados** | Mary, Amelia, Saga, Mimir y Freya diluyen la disputa de 4 roles | **Nombrar el cast inline.** SKILL.md §4: *"an inline-named cast IS the roster for the session"*. Nombrar a John, Sally, Winston y Murat en el prompt fija el roster. |
| C2 | `party_mode = "session"` → **una sola mente voces a todos los personajes inline** | Es literalmente el mecanismo del empate fácil que quieres evitar: un contexto compartido converge solo | **Lanzar con `--mode subagent`.** SKILL.md: *"a real agent behind each persona every substantive round so each thinks independently."* |
| C3 | `communication_language = "English"` (`config.user.toml`) | La party correrá **en inglés**, no en español | Está bien: el Worksheet 5 también es en inglés. El prompt de §10 va en inglés a propósito. |

> **Nota menor:** `user_name = "Joshe"` en `config.user.toml`. La party saludará como "Joshe" (respuesta de instalación de tu compañero). Inofensivo, pero no te sorprendas.
>
> **Nota sobre memoria:** `party_memory = true`, pero SKILL.md aclara que *"Ad-hoc inline casts are always ephemeral until saved as a party."* Un cast inline **no** deja memlog. Para esta sesión única es lo correcto. El *keepsake* HTML opcional del cierre se escribe en `_bmad-output/party-mode/`.

---

## 1. Enunciado de la disputa

**Formulación oficial del enunciado (Option A — Probe 2):**

> *"UX Spec §4.1 mandates offline QR validation in < 200ms, but Architecture page 31 defers offline support to Phase 2."*

**Formulación operativa (con anclajes reales del repositorio):**

> La UX declara como criterios de éxito que el escaneo de acceso se completa **en menos de 200 ms** y que los tokens QR son válidos **sin datos celulares activos**. La Arquitectura declara que el soporte offline **no es requerido en Fase 1** y queda **diferido a Fase 2**. Ambos documentos describen el mismo recorrido (entrada por portería) y ninguno reconoce la existencia del otro.

> ⚠️ **Discrepancia de encuadre que debes conocer.** El enunciado funde latencia y offline en una sola cláusula ("offline QR validation in < 200ms"). En el documento real **son dos viñetas separadas** (`ux:147` y `ux:153`) más una tercera afirmación en el diagrama de flujo (`ux:241`). El briefing cita las tres para satisfacer el requisito *verbatim* del worksheet sin inventar una frase que no existe. Menciónalo en tu resolución final: es un punto a tu favor, no un problema.

La party **no se convoca para decidir "quién gana"**, sino para producir el material con el que **tú**, como Lead Engineer, escribes la *Final Engineering Resolution* de §5.2. Ver §6.

---

## 2. Evidencia canónica (citas verificables)

### 2.1 Target Document Clauses — para el campo homónimo de §5.2

**Document 1 Clause — UX Design Specification** (`§ Core User Experience > Success Criteria`, sin etiqueta de fase)

```
ux-design-specification.md:147   The "Walking Pace" Benchmark: Successful scan in under 200ms.
ux-design-specification.md:153   Offline Resiliency: QR tokens are valid without active cellular data.
ux-design-specification.md:241   This flow must be executable in under 200ms to avoid gate congestion.
```

**Document 2 Clause — Architecture Decision Document** (`§ Mobile Architecture (Expo/React Native)`, con etiqueta de fase explícita)

```
architecture.md:175   Offline Support   Not required (Phase 1)   Deferred to Phase 2
```

**Mapeo a la nomenclatura del enunciado:** "UX Spec §4.1" → `ux-design-specification.md:147,153,241` · "Architecture page 31" → `architecture.md:175`. Los `.md` extraídos no tienen numeración de secciones ni paginación; la referencia del enunciado viene del PDF original.

### 2.2 Contexto que reencuadra la disputa (hallazgo propio, no presente en Fase 1)

| # | Fuente | Ancla | Texto literal | Por qué importa |
|---|---|---|---|---|
| E3 | PRD | `prd.md:77` | `Campus entry validation (Gatekeeper).` — bajo `### Phase 2: Growth — Spatial Intelligence` | **El PRD ya ubica toda la portería en Fase 2.** Architecture está alineado con el PRD; la UX es el documento descolgado. |
| E4 | PRD | `prd.md:225,227,229` | `FR-15`, `FR-16`, `FR-17` (validación de entrada por QR/NFC, Green/Red, registro de visitantes) | Viven en la lista plana de FRs **sin etiqueta de fase**, contradiciendo E3. El PRD se contradice a sí mismo. |
| E5 | PRD | `prd.md:265,267,269` | `FR-30`, `FR-31`, `FR-32` (QR firmado, expiración 5 min, **staff escanea con la app móvil**) | FR-31 implica que **el escáner también es un teléfono**. El problema offline existe en *ambos* extremos del escaneo. |
| E6 | Architecture | `architecture.md:212-228` | `Implementation Sequence: ... Entry Gateway Service ...` | La secuencia de implementación **incluye** el Entry Gateway sin etiqueta de fase, mientras E2 difiere offline a Fase 2. Architecture también es internamente ambiguo. |
| E7 | Architecture | `architecture.md:7` | `Functional Requirements (23 FRs across 6 categories)` | El PRD define 38 FRs. Architecture razonó sobre un subconjunto. Desajuste de alcance = causa raíz estructural. |
| E8 | UX | `ux-design-specification.md:243-256` | Diagrama del flujo de portería | **Solo modela `Valid` y `Expired`.** No existe rama para "sin red", ni siquiera para denegar. |
| E9 | Architecture / PRD | `architecture.md:33` · `prd.md:293` | `NFR-3 \| API <200ms p95 \| Low-latency service design` · `NFR-3: API response times are under 200ms for 95th percentile under normal load.` | La Arquitectura promete 200 ms **de API a p95**; la UX promete 200 ms **de flujo completo**. No son la misma magnitud. |

### 2.3 Guard-snippets de la revisión automatizada (línea base a igualar o superar)

**`review-adversarial-bundle.json` — lente Adversarial** · location: `UX > Core User Experience > Success Criteria; Architecture > Mobile Architecture > Offline Support`

- *trigger_condition:* `The UX requires QR tokens to work without cellular data, while the architecture explicitly says offline support is not required in Phase 1.`
- *guard_snippet:* `Choose one Phase 1 contract: either remove offline validity from UX or define offline-signed token issuance, scanner trust material, clock-skew tolerance, revocation limits, replay controls, and synchronization behavior.`
- *potential_consequence:* `Users may be denied entry during network outages or scanners may accept stale or revoked credentials without a defined risk model.`

**`review-adversarial-bundle.json`** · location: `PRD > UJ-5 and FR-30 through FR-32; UX > Frictionless Campus Entry and Rotating QR Token`

- *guard_snippet:* `Define a complete entry state machine with Active, Fenced, Pending Review, Unknown, Expired, Revoked, Offline-Unverifiable, and Service-Unavailable states, including copy, iconography, retry, staffed fallback, and audit behavior for each.`

**`review-adversarial-bundle.json`** · location: `UX > Frictionless Campus Entry; UX > Critical Success Moments; PRD > NFR-3` *(el vínculo latencia↔offline del enunciado)*

- *guard_snippet:* `Split the latency budget into measurable stages and define end-to-end percentile targets from scan acquisition to gate decision under normal, peak, degraded-network, and offline conditions.`

**`review-edge-cases-bundle.json`** — hallazgos satélite que la resolución debe cubrir:

| Trigger | Guard exigido |
|---|---|
| Escáner o app offline | `offline signature validation, trusted key rotation, cached revocation limits, maximum offline age, fail-open vs fail-closed policy` |
| Token fotografiado/replicado dentro de sus 5 min | `nonce, audience, gate/session binding, replay detection with defined offline fallback` |
| Relojes de dispositivo y escáner desfasados | `authoritative time, allowed clock skew, regeneration behavior, recoverable clock-error state` |
| Usuario promovido a `Fenced` tras emitirse el token | `immediate token revocation or online revalidation; offline acceptance must have an explicit bounded risk window` |
| Validación expira / estado desconocido | `Add explicit Pending, Offline, Invalid, Expired, System Error outcomes; do not map unknown states to Green` |

> **Nota de procedencia:** esta evidencia cross-document proviene de los JSON de *bundle*. Los `review-*-prd.json` solo cubren el PRD aislado y **no** contienen esta colisión. Citar los bundle.

---

## 3. Posturas iniciales por rol

> Los encabezados usan **los cuatro lentes exactos de la plantilla §5.2**, para que la transcripción sea directa. Cada postura incluye lo que el agente **concede** y lo que **no concede**. Un agente que no defienda su "no concede" no está haciendo su trabajo.

### 3.1 📋 John — PM Perspective: *User Value & Scope*

**Tesis:** *La UX escribió un criterio de éxito de Fase 1 para una capacidad que el PRD ya asignó a Fase 2. El contrato de fase manda.*

- **Se apoya en:** E3 (`prd.md:77` ubica Gatekeeper en Fase 2) y el `architecture.md:175` (Architecture coincide). Dos de tres documentos concuerdan.
- **Concede:** el PRD es la causa raíz. FR-15/16/17 y FR-30/31/32 (E4, E5) viven sin etiqueta de fase, lo que habilitó que UX y Architecture leyeran cosas distintas. El PM asume la deuda: **etiquetar por fase los 38 FRs** es entregable suyo, no de UX.
- **NO concede:** que "resiliencia offline" entre a Fase 1 por la puerta de atrás como criterio de éxito de UX. Si la portería completa es Fase 2, su comportamiento degradado también lo es.
- **Coste si pierde:** adelantar criptografía offline a Fase 1 desplaza el Status Promotion Machine, el grafo temporal y la consola de de-identificación (`prd.md:57-69`), que *son* el núcleo del MVP.

### 3.2 🎨 Sally — UX Perspective: *Screen States & Friction*

**Tesis:** *La promesa "Magic Door" muere en la puerta. Diferir offline sin rediseñar la portería no resuelve nada: deja un flujo sin estado para el caso más común.*

- **Se apoya en:** E8 — el diagrama de portería (`ux:243-256`) solo modela `Valid` y `Expired`. **No hay rama para "sin red"**, ni siquiera para denegar. Diferir offline a Fase 2 no elimina ese hueco: lo congela.
- **Argumento de fricción física:** las porterías son donde falla la cobertura — torniquetes metálicos, accesos subterráneos, aglomeraciones a las 8:00. El caso "sin datos" no es un borde: es el escenario recurrente de la hora punta, y es exactamente el que produce la congestión que `ux:241` dice evitar.
- **Concede:** `ux:153` está mal redactado. Afirma una garantía criptográfica ("los tokens *son válidos*") cuando la intención de diseño era resiliencia percibida ("el usuario no queda varado"). Acepta reescribirlo.
- **NO concede:** cerrar la disputa borrando `ux:153` sin entregar a cambio un **estado `Offline-Unverifiable` con copy, iconografía, ruta de reintento y fallback atendido por personal**. Eliminar la línea sin diseñar el fallo sustituye una contradicción por una omisión.
- **Coste si pierde:** sin fallback definido, el guardia improvisa — y la improvisación en portería significa o colas, o dejar pasar a gente en `Fenced`.

### 3.3 🏗️ Winston — Architect Perspective: *Invariants & Feasibility*

**Tesis:** *"Offline" no es un interruptor: es un modelo de confianza distinto, FR-31 lo duplica, y el invariante que salga de aquí debe decir qué NO puede ocurrir nunca.*

- **Se apoya en:** E5 — `FR-31` dice que **el personal escanea con la app móvil**. Hay dos dispositivos que pueden estar offline: el del portador y el del escáner. Validar offline exige, en el escáner: material de confianza distribuido, rotación de claves, CRL cacheada, edad máxima de caché, tolerancia de desfase horario y política fail-open/fail-closed. Es un subsistema, no un flag.
- **Segundo apoyo (el invariante candidato):** conflicto irreducible con `FR-32` (token firmado, 5 min) — un escáner offline **no puede saber** que el portador fue promovido a `Fenced` después de la emisión. Offline y revocación inmediata son mutuamente excluyentes; solo se negocia el **tamaño de la ventana de riesgo**.
- **Tercer apoyo:** E9 — la Arquitectura promete 200 ms de **API a p95** (`NFR-3`), la UX promete 200 ms de **flujo completo**. La cláusula del enunciado ("offline validation in < 200ms") funde dos presupuestos que nunca fueron el mismo.
- **Concede:** E6 y E7 son deuda suya. `Entry Gateway Service` aparece en la secuencia sin etiqueta de fase, y el documento razonó sobre 23 FRs cuando el PRD define 38. La decisión de `architecture.md:175` se tomó sobre alcance incompleto y debe re-emitirse explícitamente contra los 38.
- **NO concede:** que se acepte "resiliencia offline" sin **ventana de riesgo numérica y política fail-open/fail-closed por tipo de puerta**. Un "sí" sin esos dos números es una brecha de seguridad con formato de acuerdo.
- **Formato exigido a su propia postura:** debe cerrar enunciando su posición como **regla sin lenguaje elástico**, lista para convertirse en el campo `Rule:` del `AD-n` de §5.3.

### 3.4 🧪 Murat — Test Architect Perspective: *Risk & ATDD Testability*

**Tesis:** *Tal como está escrito hoy, ninguna de las dos posturas puede fallar una prueba. Ese es el defecto real, y "diferir a Fase 2" no lo arregla.*

- **Se apoya en:** `ux:153` no define qué significa "válido sin datos" (¿cuánto tiempo? ¿contra qué material de confianza?). `architecture.md:175` no define qué debe ocurrir en Fase 1 cuando *sí* se cae la red — solo dice que el soporte "no es requerido". **Ningún caso de prueba puede distinguir un sistema conforme de uno no conforme.**
- **Posición procedimental (bloqueante):** "Diferido a Fase 2" **no** es resolución por sí sola. Ausencia de soporte offline sigue siendo comportamiento observable y requiere criterio de aceptación negativo en Fase 1: *dado el escáner sin red, el sistema DEBE `<resultado definido>`*.
- **Exige tres escenarios en Gherkin** (formato de §5.3 Artifact B, no prosa):
  1. `Given` escáner sin conectividad `And` token válido no expirado → `When` se escanea → `Then` `<resultado definido>`.
  2. `Given` token emitido `And` portador promovido a `Fenced` después de la emisión (E5/`FR-32`) `And` escáner offline → `When` se escanea → `Then` `<resultado definido>` `And` se emite registro de auditoría.
  3. `Given` desfase de reloj en el límite exacto de la tolerancia acordada → `When` se escanea → `Then` `<resultado definido>` recuperable.
- **NO concede:** ningún acuerdo que use "debería", "resiliente" o "mejor esfuerzo" sin número asociado. Ninguna métrica de latencia sin decir si es cliente end-to-end o servidor, y a qué percentil (E9).
- **Rol en la sala:** Murat no vota por A o B. Vota por **falsabilidad**, y veta cualquier redacción que no la tenga — incluida la ganadora.

---

## 4. Asimetría deliberada (por qué esto no puede empatar)

| | Respaldo documental | Punto débil propio |
|---|---|---|
| John | 2 de 3 documentos (`prd.md:77` + `architecture.md:175`) | El PRD se autocontradice (E4, E5) — causa raíz suya |
| Winston | Alineado con el PRD; coste técnico real (E5) | Decidió sobre 23 de 38 FRs (E7); secuencia sin fases (E6) |
| Sally | El más débil documentalmente (dos viñetas sin fase) | Pero es la única con un hueco que persiste **gane quien gane** (E8) |
| Murat | Ninguno — no disputa el fondo | Puede bloquear a los tres |

John y Winston entran alineados **sobre la fase** pero divergen sobre el alcance del arreglo: John quiere etiquetar FRs y cerrar; Winston sostiene que su propia decisión debe re-emitirse contra los 38 FRs antes de ser vinculante. Sally pierde el punto de fase y aun así retiene el entregable. Murat puede rechazar el consenso de los tres. **No hay configuración en la que los cuatro salgan satisfechos sin trabajo nuevo.**

---

## 5. Preguntas que la sala debe responder (en orden)

1. ¿La validación de entrada en portería es Fase 1 o Fase 2? *(Vinculante — resuelve E3 vs E4/E5/E6.)*
2. Dada esa fase, ¿cuál es el comportamiento **especificado** de la puerta cuando el dispositivo del portador, el del escáner, o ambos, no tienen red?
3. Si se admite alguna validación offline: ¿cuál es la **edad máxima de caché** en minutos, y la política **fail-open o fail-closed por tipo de puerta**?
4. Dado `FR-32` (5 min): ¿cuál es la **ventana de riesgo aceptada** en la que un token de un usuario recién promovido a `Fenced` puede seguir abriendo la puerta? *(Un número, o "cero" con revalidación online obligatoria.)*
5. Los 200 ms: ¿cliente end-to-end o servidor? ¿A qué percentil? ¿Aplican también en la ruta degradada? *(Resuelve E9 y la cláusula fundida del enunciado.)*
6. ¿Qué estados entran en la máquina de estados de entrada de Fase 1 y cuáles se difieren? *(Base: `Active, Fenced, Pending Review, Unknown, Expired, Revoked, Offline-Unverifiable, Service-Unavailable`.)*
7. ¿Qué documento se edita, en qué línea, con qué texto exacto?

---

## 6. Criterio de cierre

### 6.1 Compuertas obligatorias — las siete deben cumplirse

| # | Compuerta | Se verifica con |
|---|---|---|
| G1 | **Fase declarada.** Un único documento declara la fase de la validación de entrada; los otros dos se alinean o la citan explícitamente. | Sin contradicción residual entre `prd.md:77`, la lista de FRs del PRD y `architecture.md:175`. |
| G2 | **Comportamiento offline especificado, no omitido.** Aun si la respuesta es "sin soporte offline en Fase 1", existe comportamiento definido y observable para la puerta sin red. | Murat puede escribir un `Then` que falle si el sistema hace otra cosa. |
| G3 | **Números, no adjetivos.** Si hay validación offline: edad máxima de caché, tolerancia de desfase horario y política fail-open/fail-closed por tipo de puerta, todos numéricos. | Cero apariciones de "resiliente", "debería" o "mejor esfuerzo" sin cifra adjunta. |
| G4 | **Ventana de riesgo de revocación reconocida.** La tensión `FR-32` × offline se resuelve con ventana explícita o prohibición explícita de aceptación offline. | La cifra (o el cero) queda escrita en el documento, no en el acta. |
| G5 | **Presupuesto de latencia desagregado.** Los 200 ms quedan definidos como cliente o servidor, con percentil, y con valor declarado para la ruta degradada. | Resuelve E9; sin esto la cláusula del enunciado sigue siendo dos promesas distintas. |
| G6 | **Ruta de fallo diseñada.** Existe estado de UI para validación no concluyente, con copy, alternativa no cromática (`ux:429-437`, WCAG 2.1 AA) y fallback atendido. | Entregable de Sally, exigible aunque haya perdido G1. |
| G7 | **Ediciones concretas.** Cada cambio acordado se expresa como `archivo:línea` + texto nuevo. | Diff aplicable, no minuta. |

### 6.2 Qué produce la sala y qué produces tú

La plantilla §5.2 separa dos cosas que no hay que confundir:

- **La sala produce** las cuatro *Agent Positions* y el material técnico (números, estados, reglas). La sala puede **no** llegar a consenso — el enunciado no lo exige.
- **Tú produces** la *Final Engineering Resolution*. Es **tu veredicto como Lead Engineer**, no el acta del consenso. Si la sala se traba, adjudicas tú y lo dices.

**Forma mínima de una resolución aceptable:** un **contrato de fase único** que (a) asigna la validación de entrada a una fase, (b) especifica el comportamiento de la puerta sin red *para la Fase 1 en todo caso*, (c) adjunta cifras a toda tolerancia y al presupuesto de latencia, (d) nombra el estado de UI del fallo, y (e) se entrega como lista de ediciones `archivo:línea`.

**Una resolución es válida aunque un rol pierda por completo en G1.** Lo que no es válido es que un rol pierda en G1 y por eso no entregue nada.

### 6.3 Anti-patrones — rechazar explícitamente

| Anti-patrón | Por qué se rechaza |
|---|---|
| **"Diferido a Fase 2."** — a secas | Viola G2. Deja `ux:153` en pie, o lo borra sin definir el reemplazo. Es la contradicción convertida en omisión. |
| **"Soporte offline best-effort."** | Viola G3 y G4. Sin edad máxima de caché ni ventana de revocación, autoriza a un escáner a admitir a una persona en `Fenced` sin límite. |
| **"UX cede, se eliminan las líneas 147/153."** | Viola G6. Cierra la colisión formal y deja el flujo de portería sin rama de fallo (E8). |
| **"Los 200 ms se mantienen como aspiración."** | Viola G5 y el mandato del enunciado de *"no compromise with vague language"*. |
| **"Ambos tienen razón, se documenta la tensión."** | Viola G1 y G7. Un riesgo registrado no es un contrato de fase. |
| **Acuerdo sin `archivo:línea`.** | Viola G7. Nada que un revisor pueda verificar en el repositorio. |

---

## 7. Estructura de salida — mapeo 1:1 con Worksheet 5 §5.2

> Verificado contra `unit 3 - Student_Assignment_BMad_Spec_Review.pdf`, líneas 247-297 del texto extraído. La sesión debe producir **exactamente estos cinco bloques**, en este orden.

### Bloque 1 — `Chosen Collision`
> ☒ **Option A: Offline Gate Access & Validation (UX §4.1 vs. Architecture page 31)**
> ☐ Option B: Professor Dashboard Anonymity vs. Real Names (PRD FR-18 vs. UX §4.6)

Añadir una línea con la justificación de la elección (convergencia humano↔IA, §9).

### Bloque 2 — `Target Document Clauses`
- **Document 1 Clause:** cita *verbatim* de §2.1, bloque UX, con las tres líneas y sus anclas.
- **Document 2 Clause:** cita *verbatim* de §2.1, bloque Architecture, con su ancla.
- Nota de mapeo "§4.1 / page 31" → anclas reales, y la discrepancia de encuadre de §1.

### Bloque 3 — `Agent Positions Summary (from the /bmad-party-mode debate)`
Cuatro entradas, con las etiquetas **exactas** del worksheet:

| Campo del worksheet | Fuente en este briefing |
|---|---|
| `John (PM Perspective - User Value & Scope)` | §3.1 + lo que efectivamente argumente en sala |
| `Sally / Freya (UX Perspective - Screen States & Friction)` | §3.2 — **transcribir a Sally**; anotar que Freya existe pero no fue convocada |
| `Winston (Architect Perspective - Invariants & Feasibility)` | §3.3, cerrando con su regla sin lenguaje elástico |
| `Murat (Test Architect Perspective - Risk & ATDD Testability)` | §3.4, con los tres escenarios en Gherkin |

Cada entrada: tesis, concesión, y el punto que **no** cedió. Dos a cuatro frases — la plantilla da ~4 renglones por rol.

### Bloque 4 — `Final Engineering Resolution (Your verdict as Lead Engineer)`
Tu veredicto, no el acta. Debe satisfacer G1–G7 y decir en una frase inicial **cuál es la decisión**, antes de cualquier matiz.

### Bloque 5 — Anexo de trazabilidad *(no lo pide el worksheet; lo añades tú)*
Registro G1–G7 con evidencia, y la lista de ediciones `archivo:línea` sobre `prd.md`, `ux-design-specification.md` y `architecture.md`.

### 7.1 Puente a §5.3 — qué debe salir de la sesión para no repetirla

§5.3 exige dos artefactos con formato fijo. La sesión debe dejar el material listo:

| Campo de §5.3 | Alimentado por |
|---|---|
| `AD-n:` nombre de la decisión | Bloque 4 |
| `Binds:` | E5/E6 — Entry Gateway Service, app móvil del portador, **app de escaneo del staff (FR-31)** |
| `Prevents:` | G4 — admisión de un portador `Fenced` con token pre-emisión |
| `Rule:` **sin lenguaje elástico** | G3 + G4 + G5 — los números de Winston |
| `Trade-off:` | La postura perdedora en G1, enunciada como sacrificio explícito |
| `Feature/Scenario/Given/When/Then/And` | Los tres escenarios Gherkin de Murat (§3.4) |

> Si la sesión termina sin los números de G3/G4/G5, §5.3 es inescribible y hay que volver a convocar. Esa es la razón práctica del veto de Murat.

---

## 8. Reglas de la sala

- Cada rol abre con su tesis y su "NO concede" **antes** de cualquier réplica.
- Nadie cita "buenas prácticas" sin anclarlas a `archivo:línea` de los tres exhibits.
- Los guard-snippets de §2.3 son la **línea base**: la resolución debe igualarlos o superarlos; si los rechaza, debe justificarlo por escrito.
- Murat habla en último lugar en cada ronda y puede vetar el consenso.
- La sesión no cierra hasta que G1–G7 estén marcadas.
- Prohibido el lenguaje elástico — mandato literal del enunciado: *"Do not compromise with vague language."*

---

## 9. Trazabilidad a Fase 1

| Artefacto de Fase 1 | Vínculo |
|---|---|
| `human-audit-baseline.md` | W1-UX (Joshua): *"UX requires offline QR resiliency while Architecture defers offline support"* — Cross-document [X], **Critical**. W2: única colisión calificada *"Valid, critical cross-document contradiction"*. |
| `bmad-review-report.md` | Convergent high-impact finding **#5**: *"Offline promise conflicts with Architecture."* |
| `worksheet-5-phase-1.md` | True Positive **#6** — defecto hallado por humano **y** máquina. |
| `review-adversarial-bundle.json` | Colisión exacta con ambos anclajes + tres guard-snippets (§2.3). |
| `review-edge-cases-bundle.json` | Cinco hallazgos satélite que definen el alcance de la resolución (§2.3). |

Option A es la **única** colisión cross-document con convergencia humano↔IA independiente en toda la Fase 1.

---

## 10. Lanzamiento

### 10.1 Comando

```
/bmad-party-mode --mode subagent
```

`--mode subagent` es **obligatorio** por C2 (§0.3): sin él, un solo contexto voces a los cuatro y convergen sin fricción real.

### 10.2 Prompt de apertura

En inglés, porque `communication_language = "English"` (C3). Sigue la plantilla del enunciado (Fase 2, paso 3) con las cláusulas verbatim reales insertadas:

```
We have a critical cross-document collision in CircleGuard.

John (PM), Sally (UX), Winston (Architect), and Murat (Test Architect) — you four
are the room for this session.

THE COLLISION — Option A, The Offline Gate:

  Document 1, UX Design Specification (Core User Experience > Success Criteria):
    "The 'Walking Pace' Benchmark: Successful scan in under 200ms."     [ux:147]
    "Offline Resiliency: QR tokens are valid without active cellular data."  [ux:153]
    "This flow must be executable in under 200ms to avoid gate congestion." [ux:241]

  Document 2, Architecture Decision Document (Mobile Architecture):
    "Offline Support | Not required (Phase 1) | Deferred to Phase 2"     [architecture.md:175]

CONTEXT YOU MUST ACCOUNT FOR:
  - prd.md:77 places "Campus entry validation (Gatekeeper)" in Phase 2.
  - prd.md:225-229 (FR-15..17) and prd.md:265-269 (FR-30..32) carry NO phase tag.
  - FR-31: university staff scan with the MOBILE APP — the scanner can be offline too.
  - FR-32: QR tokens are signed and expire in 5 minutes.
  - NFR-3 promises 200ms for API p95; the UX promises 200ms end-to-end. Not the same budget.
  - The UX gate flow diagram (ux:243-256) models ONLY "Valid" and "Expired" —
    there is no branch for "no network", not even to deny.

Debate the technical, user experience, and risk trade-offs of this contradiction.
Do not compromise with vague language. Propose an authoritative engineering
resolution that eliminates the collision.

Ground rules:
  - Open with your thesis AND the one thing you will NOT concede, before any rebuttal.
  - Cite file:line from the three exhibits. No "best practice" without an anchor.
  - Winston: close with your position stated as a rule containing ZERO elastic
    language — it becomes an AD-n Rule field.
  - Murat: express your acceptance criteria as Given/When/Then, not prose. You may
    veto any wording that cannot fail a test — including the winning proposal.
  - Do not close until these are settled with NUMBERS: entry-validation phase;
    specified gate behavior with no network; max offline cache age; fail-open vs
    fail-closed by gate type; the revocation risk window for FR-32; whether 200ms
    is client end-to-end or server, and at what percentile.
```

### 10.3 Checklist previo

- [ ] Contexto fresco (el enunciado lo exige: *"In a fresh context window"*).
- [ ] Confirmar que el cast inline quedó fijado en los cuatro y no aparecieron Mary, Amelia, Saga, Mimir o Freya (C1).
- [ ] Confirmar que corre en `subagent`, no en `session` (C2).
- [ ] Guardar el transcript — §5.2 pide *"Party Mode Resolution Transcript & Executive Decision"*.

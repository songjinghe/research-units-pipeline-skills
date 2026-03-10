# research-units-pipeline-skills

> Languages: [English](README.md) | [简体中文](README.zh-CN.md) | **Español** | [Português (Brasil)](README.pt-BR.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

> **En una frase**: Crea pipelines que pueden “guiar a humanos / guiar a modelos” durante la investigación: no solo scripts, sino un conjunto de **skills semánticas** donde cada skill sabe qué hacer, cómo hacerlo, cuándo se considera terminado y qué NO debe hacer.

Índice de skills: [`SKILL_INDEX.md`](SKILL_INDEX.md).  
Estándar de skills/pipelines: [`SKILLS_STANDARD.md`](SKILLS_STANDARD.md).

## Diseño central: Skills primero + unidades reanudables + evidencia primero

Los flujos de investigación suelen caer en uno de estos extremos:
- **solo scripts**: se ejecutan, pero son una caja negra difícil de depurar o mejorar;
- **solo documentación**: se ven bien, pero la ejecución sigue dependiendo de criterio ad hoc y se desvía con facilidad.

Este repositorio convierte “escribir un survey” en **pasos pequeños, auditables y reanudables**, y deja artefactos intermedios en disco en cada etapa.

1) **Skill = manual ejecutable**
- Cada skill define `inputs / outputs / acceptance / guardrails`.
- Por ejemplo, C2–C4 son etapas de **NO PROSE**.

2) **Unit = paso reanudable**
- Cada unit es una fila en `UNITS.csv` con dependencias, entradas, salidas y criterios de DONE.
- Si una unit queda `BLOCKED`, se corrige el artefacto referido y se continúa desde ahí, sin reiniciar todo.

3) **Evidencia primero**
- C1 recupera papers.
- C2 construye la estructura y el pool de papers por subsección.
- C3/C4 convierten eso en evidencia y referencias listas para escribir.
- C5 redacta y produce el draft final o el PDF.

Resumen rápido:

| Si necesitas... | Mira | Acción típica |
|---|---|---|
| ampliar cobertura / conseguir más papers | `queries.md` + `papers/retrieval_report.md` | añadir buckets de keywords, subir `max_results`, importar colecciones offline, hacer snowballing |
| corregir la estructura o subsecciones débiles | `outline/outline.yml` + `outline/mapping.tsv` | fusionar/reordenar secciones, subir `per_subsection`, volver a mapear |
| reforzar escritura con poca evidencia | `papers/paper_notes.jsonl` + `outline/evidence_drafts.jsonl` | mejorar notes/packs antes de redactar |
| reducir tono plantillado o redundancia | `output/WRITER_SELFLOOP_TODO.md` + `output/PARAGRAPH_CURATION_REPORT.md` + `sections/*` | reescritura localizada + best-of-N + fusión de párrafos |
| aumentar citas únicas globales | `output/CITATION_BUDGET_REPORT.md` + `citations/ref.bib` | inyección in-scope de citas (NO NEW FACTS) |

## Configuración de referencia para Codex

```toml

[sandbox_workspace_write]
network_access = true

[features]
unified_exec = true
shell_snapshot = true
steer = true
```

## Inicio rápido de 30 segundos (de 0 a PDF)

1) Inicia Codex en este repositorio:

```bash
codex --sandbox workspace-write --ask-for-approval never
```

2) Escribe una sola frase en el chat, por ejemplo:

> Write a survey about LLM agents and output a PDF (show me the outline first)

3) Qué ocurre después:
- Crea una carpeta con timestamp dentro de `workspaces/` y guarda ahí todos los artefactos.
- Prepara primero el outline y una lista de lectura por sección, y luego se detiene para pedir tu confirmación.
- Responde “Looks good. Continue.” para comenzar la redacción y generar el PDF.

4) Los tres archivos que más abrirás:
- Draft en Markdown: `workspaces/<...>/output/DRAFT.md`
- PDF: `workspaces/<...>/latex/main.pdf`
- Reporte de QA: `workspaces/<...>/output/AUDIT_REPORT.md`

5) Si se detiene inesperadamente:
- `workspaces/<...>/output/QUALITY_GATE.md`: por qué se detuvo y qué corregir a continuación
- `workspaces/<...>/output/RUN_ERRORS.md`: errores de ejecución o scripts

Opcional:
- Fija el pipeline explícitamente: `pipelines/arxiv-survey-latex.pipeline.md`
- Si quieres un flujo completamente automático sin pausa en el outline, dilo en el prompt inicial.

Glosario mínimo:
- workspace: carpeta de salida de una ejecución (`workspaces/<name>/`)
- C2: checkpoint de aprobación del outline; sin esa aprobación no se escribe prose
- strict: activa quality gates; si falla algo, el proceso se detiene con reporte

## Recorrido detallado: de 0 a PDF

En el chat normalmente escribirás algo como:

> Write a LaTeX survey about LLM agents (strict; show me the outline first)

El pipeline avanza por etapas y, por defecto, se detiene en C2.

### [C0] Inicializar una ejecución (sin prose)

- Crea una carpeta con timestamp en `workspaces/`.
- Escribe el contrato básico de ejecución: `UNITS.csv`, `DECISIONS.md` y `queries.md`.

### [C1] Buscar papers (primero construir un pool sólido)

- Objetivo: recuperar un conjunto candidato grande (`max_results=1800` por bucket; meta de deduplicación `>=1200`) y luego seleccionar un core set (por defecto `300`).
- Enfoque: dividir el tema en varios buckets (sinónimos, acrónimos, subtemas), recuperar por separado y luego fusionar + deduplicar.
- Si la cobertura es baja, añade buckets o sube `max_results`.
- Si el ruido es alto, refina keywords y exclusiones.
- Salidas principales: `papers/core_set.csv` y `papers/retrieval_report.md`.

### [C2] Revisar el outline (sin prose; pausa por defecto)

Revisa sobre todo:
- `outline/outline.yml`
- `outline/mapping.tsv`
- opcionalmente `outline/coverage_report.md`

Dos comprobaciones rápidas suelen bastar:
1) ¿La estructura tiene pocas secciones pero suficientemente sustanciosas?
2) ¿Cada subsección tiene suficientes papers mapeados para redactar con respaldo?

### [C3–C4] Convertir papers en material listo para escribir (sin prose)

- `papers/paper_notes.jsonl`: qué hizo cada paper, resultados y limitaciones
- `citations/ref.bib`: bibliografía y claves de cita utilizables
- `outline/writer_context_packs.jsonl`: packs de escritura por subsección
- `outline/tables_index.md`: tabla índice interna
- `outline/tables_appendix.md`: tablas legibles para el apéndice

### [C5] Redacción y salida (todas las iteraciones ocurren aquí)

1) Escribir archivos por sección en `sections/*.md`
- Primero el cuerpo, luego reescribir aperturas y transiciones.
- Normalmente incluye front matter, chapter leads y subsecciones.

2) Pasar por cuatro gates de convergencia:
- `output/WRITER_SELFLOOP_TODO.md`
- `output/SECTION_LOGIC_REPORT.md`
- `output/ARGUMENT_SELFLOOP_TODO.md`
- `output/PARAGRAPH_CURATION_REPORT.md`

3) Desplantillar el texto:
- `style-harmonizer`
- `opener-variator`

4) Fusionar al draft final `output/DRAFT.md`
- Si faltan citas: `output/CITATION_BUDGET_REPORT.md` → `output/CITATION_INJECTION_REPORT.md`
- Auditoría final: `output/AUDIT_REPORT.md`
- En el pipeline LaTeX también se compila `latex/main.pdf`

Meta recomendada:
- citas únicas globales `>=165`

Si el pipeline se bloquea:
- revisa `output/QUALITY_GATE.md`
- o `output/RUN_ERRORS.md`

Para reanudar:
- corrige el archivo indicado y di “continue”

**Principio clave**: C2–C4 aplican **NO PROSE**; primero se construye la base de evidencia y solo en C5 se redacta prose.

## Artefactos de ejemplo (v0.1: una ejecución completa de referencia)

Este directorio de ejemplo recorre todo el flujo: recuperar papers → outline → evidencia + referencias → escribir por sección → fusionar → compilar PDF.

- Ruta de ejemplo: `example/e2e-agent-survey-latex-verify-<TIMESTAMP>/`
- El pipeline se detiene en **C2** antes de redactar prose
- Configuración por defecto: 300 papers núcleo, 28 papers mapeados por subsección y evidencia a nivel abstract
- Perfil recomendado: `draft_profile: survey`; si quieres más rigor, usa `draft_profile: deep`

Puntos de entrada sugeridos:
- `example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/output/AUDIT_REPORT.md`
- `example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/latex/main.pdf`
- `example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/output/DRAFT.md`

Si quieres entender cómo converge la escritura:
- El prose por subsección está en `sections/`
- Los reportes de iteración están en `output/`

Vista rápida del directorio:

```text
example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/
  STATUS.md           # progreso y registro de ejecución
  UNITS.csv           # contrato de ejecución
  DECISIONS.md        # checkpoints humanos
  CHECKPOINTS.md      # reglas de checkpoint
  PIPELINE.lock.md    # pipeline seleccionado
  GOAL.md             # objetivo y alcance
  queries.md          # configuración de recuperación y redacción
  papers/             # resultados de búsqueda + base de evidencia
  outline/            # estructura + materiales para redactar
  citations/          # BibTeX + verificación
  sections/           # drafts por sección
  output/             # draft fusionado + reportes QA
  latex/              # scaffold LaTeX + PDF compilado
```

Nota: `outline/tables_index.md` es una tabla interna; `outline/tables_appendix.md` es una tabla orientada al lector.

Vista del pipeline:

```mermaid
flowchart LR
  WS["workspaces/{run}/"]
  WS --> RAW["papers/papers_raw.jsonl"]
  RAW --> DEDUP["papers/papers_dedup.jsonl"]
  DEDUP --> CORE["papers/core_set.csv"]
  CORE --> STRUCT["outline/outline.yml + outline/mapping.tsv"]
  STRUCT -->|Approve C2| EVID["C3-C4: paper_notes + evidence packs"]
  EVID --> PACKS["C4: writer_context_packs.jsonl + citations/ref.bib"]
  PACKS --> SECS["sections/ (per-section drafts)"]
  SECS --> G["C5 gates (writer/logic/argument/style)"]
  G --> DRAFT["output/DRAFT.md"]
  DRAFT --> AUDIT["output/AUDIT_REPORT.md"]
  AUDIT --> PDF["latex/main.pdf (optional)"]

  G -.->|"FAIL → back to sections/"| SECS
  AUDIT -.->|"FAIL → back to sections/"| SECS
```

Para revisar entregables, céntrate en el directorio de ejemplo con el timestamp más reciente.

## Puedes abrir issues (para seguir mejorando el flujo de escritura)

## Roadmap (WIP)
1. Añadir colaboración multi-CLI y diseño multiagente.
2. Seguir puliendo las skills de escritura para subir el nivel mínimo y máximo.
3. Completar los pipelines restantes y añadir más ejemplos bajo `example/`.
4. Reducir contenido intermedio redundante siguiendo la navaja de Occam.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WILLOSCAR/research-units-pipeline-skills&type=Date)](https://star-history.com/#WILLOSCAR/research-units-pipeline-skills&Date)

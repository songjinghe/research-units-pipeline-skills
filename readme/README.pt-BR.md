# research-units-pipeline-skills

> Languages: [English](README.md) | [简体中文](README.zh-CN.md) | [Español](README.es.md) | **Português (Brasil)** | [日本語](README.ja.md) | [한국어](README.ko.md)

> **Em uma frase**: Crie pipelines que conseguem “guiar humanos / guiar modelos” ao longo da pesquisa — não apenas um conjunto de scripts, mas um conjunto de **skills semânticas** em que cada skill sabe o que fazer, como fazer, quando está concluída e o que NÃO deve fazer.

Índice de skills: [`SKILL_INDEX.md`](SKILL_INDEX.md).  
Padrão de skills/pipelines: [`SKILLS_STANDARD.md`](SKILLS_STANDARD.md).

## Design central: Skills-first + unidades retomáveis + evidence first

Fluxos de pesquisa costumam cair em dois extremos:
- **apenas scripts**: roda, mas vira uma caixa-preta difícil de depurar ou melhorar;
- **apenas documentação**: parece organizado, mas a execução continua dependendo de julgamento ad hoc e se desvia com facilidade.

Este repositório transforma “escrever um survey” em **passos pequenos, auditáveis e retomáveis**, salvando artefatos intermediários em disco em cada etapa.

1) **Skill = playbook executável**
- Cada skill define `inputs / outputs / acceptance / guardrails`.
- Por exemplo, C2–C4 são etapas de **NO PROSE**.

2) **Unit = passo retomável**
- Cada unit é uma linha em `UNITS.csv` com dependências, entradas, saídas e critérios de DONE.
- Se uma unit fica `BLOCKED`, você corrige o artefato apontado e retoma dali, sem reiniciar tudo.

3) **Evidence first**
- C1 recupera papers.
- C2 monta a estrutura e os pools de papers por subseção.
- C3/C4 transformam isso em evidências e referências prontas para escrita.
- C5 escreve o texto e produz o draft final ou o PDF.

Resumo rápido:

| Se você precisa... | Veja | Ação típica |
|---|---|---|
| ampliar cobertura / encontrar mais papers | `queries.md` + `papers/retrieval_report.md` | adicionar buckets de keywords, aumentar `max_results`, importar coleções offline, fazer snowballing |
| corrigir o outline ou subseções fracas | `outline/outline.yml` + `outline/mapping.tsv` | mesclar/reordenar seções, aumentar `per_subsection`, refazer o mapping |
| fortalecer escrita com pouca evidência | `papers/paper_notes.jsonl` + `outline/evidence_drafts.jsonl` | melhorar notes/packs antes de redigir |
| reduzir tom de template ou redundância | `output/WRITER_SELFLOOP_TODO.md` + `output/PARAGRAPH_CURATION_REPORT.md` + `sections/*` | reescrita localizada + best-of-N + fusão de parágrafos |
| aumentar citações únicas globais | `output/CITATION_BUDGET_REPORT.md` + `citations/ref.bib` | injeção in-scope de citações (NO NEW FACTS) |

## Configuração de referência do Codex

```toml

[sandbox_workspace_write]
network_access = true

[features]
unified_exec = true
shell_snapshot = true
steer = true
```

## Guia rápido de 30 segundos (do zero ao PDF)

1) Inicie o Codex neste repositório:

```bash
codex --sandbox workspace-write --ask-for-approval never
```

2) Digite uma única frase no chat, por exemplo:

> Write a survey about LLM agents and output a PDF (show me the outline first)

3) O que acontece em seguida:
- Ele cria uma pasta com timestamp dentro de `workspaces/`.
- Primeiro prepara o outline e a lista de leitura por seção, depois pausa para sua aprovação.
- Responda “Looks good. Continue.” para começar a escrever e gerar o PDF.

4) Os três arquivos que você mais vai abrir:
- Draft em Markdown: `workspaces/<...>/output/DRAFT.md`
- PDF: `workspaces/<...>/latex/main.pdf`
- Relatório de QA: `workspaces/<...>/output/AUDIT_REPORT.md`

5) Se parar de forma inesperada:
- `workspaces/<...>/output/QUALITY_GATE.md`
- `workspaces/<...>/output/RUN_ERRORS.md`

Opcional:
- Fixe o pipeline explicitamente: `pipelines/arxiv-survey-latex.pipeline.md`
- Se quiser rodar de ponta a ponta sem parar no outline, diga isso no prompt inicial.

Glossário mínimo:
- workspace: pasta de saída de uma execução (`workspaces/<name>/`)
- C2: checkpoint de aprovação do outline; sem isso não há prose
- strict: ativa quality gates; falhas interrompem a execução com relatório

## Passo a passo detalhado: do zero ao PDF

No chat, normalmente você dirá algo como:

> Write a LaTeX survey about LLM agents (strict; show me the outline first)

O pipeline avança por estágios e, por padrão, pausa em C2.

### [C0] Inicializar uma execução (sem prose)

- Cria uma pasta com timestamp em `workspaces/`.
- Escreve o contrato básico da execução: `UNITS.csv`, `DECISIONS.md` e `queries.md`.

### [C1] Buscar papers (primeiro montar um pool forte)

- Objetivo: recuperar um conjunto candidato grande (`max_results=1800` por bucket; meta de deduplicação `>=1200`) e depois selecionar um core set (por padrão `300`).
- Abordagem: dividir o tema em vários buckets (sinônimos, acrônimos, subtópicos), recuperar separadamente e depois mesclar + deduplicar.
- Se a cobertura estiver baixa, adicione buckets ou aumente `max_results`.
- Se houver muito ruído, refine keywords e exclusões.
- Saídas principais: `papers/core_set.csv` e `papers/retrieval_report.md`.

### [C2] Revisar o outline (sem prose; pausa por padrão)

Revise principalmente:
- `outline/outline.yml`
- `outline/mapping.tsv`
- opcionalmente `outline/coverage_report.md`

Duas checagens rápidas costumam bastar:
1) A estrutura está enxuta, mas substanciosa?
2) Cada subseção tem papers suficientes mapeados para sustentar a escrita?

### [C3–C4] Transformar papers em material pronto para escrever (sem prose)

- `papers/paper_notes.jsonl`: o que cada paper fez, resultados e limitações
- `citations/ref.bib`: bibliografia e chaves de citação válidas
- `outline/writer_context_packs.jsonl`: pacotes de escrita por subseção
- `outline/tables_index.md`: tabela índice interna
- `outline/tables_appendix.md`: tabelas voltadas ao leitor

### [C5] Escrita e saída (todas as iterações ficam aqui)

1) Escrever arquivos por seção em `sections/*.md`
- Escreva primeiro o corpo; depois reescreva aberturas e transições.
- Em geral inclui front matter, chapter leads e subseções.

2) Passar por quatro gates de convergência:
- `output/WRITER_SELFLOOP_TODO.md`
- `output/SECTION_LOGIC_REPORT.md`
- `output/ARGUMENT_SELFLOOP_TODO.md`
- `output/PARAGRAPH_CURATION_REPORT.md`

3) Tirar o “tom de template”:
- `style-harmonizer`
- `opener-variator`

4) Mesclar no draft final `output/DRAFT.md`
- Se faltarem citações: `output/CITATION_BUDGET_REPORT.md` → `output/CITATION_INJECTION_REPORT.md`
- Auditoria final: `output/AUDIT_REPORT.md`
- No pipeline LaTeX também é compilado `latex/main.pdf`

Meta recomendada:
- citações únicas globais `>=165`

Se o pipeline bloquear:
- veja `output/QUALITY_GATE.md`
- ou `output/RUN_ERRORS.md`

Para retomar:
- corrija o arquivo apontado e diga “continue”

**Princípio-chave**: C2–C4 aplicam **NO PROSE**; primeiro constrói-se a base de evidências, e só em C5 o texto é escrito.

## Artefatos de exemplo (v0.1: uma execução completa de referência)

Este diretório de exemplo percorre todo o fluxo: recuperar papers → outline → evidência + referências → escrever por seção → mesclar → compilar PDF.

- Caminho de exemplo: `example/e2e-agent-survey-latex-verify-<TIMESTAMP>/`
- O pipeline pausa em **C2** antes de escrever prose
- Configuração padrão: 300 papers centrais, 28 papers mapeados por subseção e evidência em nível de abstract
- Perfil recomendado: `draft_profile: survey`; para maior rigor, use `draft_profile: deep`

Pontos de entrada sugeridos:
- `example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/output/AUDIT_REPORT.md`
- `example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/latex/main.pdf`
- `example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/output/DRAFT.md`

Se quiser ver como a escrita converge:
- O texto bruto por subseção fica em `sections/`
- Os relatórios de iteração ficam em `output/`

Visão rápida do diretório:

```text
example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/
  STATUS.md           # progresso e log de execução
  UNITS.csv           # contrato de execução
  DECISIONS.md        # checkpoints humanos
  CHECKPOINTS.md      # regras de checkpoint
  PIPELINE.lock.md    # pipeline selecionado
  GOAL.md             # objetivo e escopo
  queries.md          # configuração de busca e escrita
  papers/             # resultados de busca + base de evidências
  outline/            # estrutura + materiais de escrita
  citations/          # BibTeX + verificação
  sections/           # drafts por seção
  output/             # draft mesclado + relatórios de QA
  latex/              # scaffold LaTeX + PDF compilado
```

Observação: `outline/tables_index.md` é uma tabela interna; `outline/tables_appendix.md` é uma tabela para o leitor.

Visão do pipeline:

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

Para revisar entregáveis, concentre-se no diretório de exemplo com o timestamp mais recente.

## Sinta-se à vontade para abrir issues

## Roadmap (WIP)
1. Adicionar colaboração multi-CLI e design multiagente.
2. Continuar refinando as skills de escrita para elevar a qualidade.
3. Completar os pipelines restantes e adicionar mais exemplos em `example/`.
4. Remover conteúdo intermediário redundante seguindo a navalha de Occam.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WILLOSCAR/research-units-pipeline-skills&type=Date)](https://star-history.com/#WILLOSCAR/research-units-pipeline-skills&Date)

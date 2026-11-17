# Design doc layout

Follow the repository's existing docs convention when it has one. Otherwise create:

```
docs/design/<system-slug>/
├── DESIGN.md                    spine: statements, status, decisions, traceability, build order
├── 1-context.md                 level 1 diagram and notes
├── 2-containers.md              level 2 diagram and notes
├── 3-components/<container>.md  one per container designed at level 3
├── 4-code/<component>.md        one per component designed at level 4
└── flows.md                     end-to-end sequence diagrams
```

Create each file when its level starts. `DESIGN.md` links to every other file and is the place a new reader starts.

## DESIGN.md

```markdown
# <System name> design

Status: <framing | level N in progress | ready for planning> · Updated: <date>

## Problem statement
<What hurts today, for whom, and what it costs.>

## Proposed solution
<The approach and named technologies, as the hypothesis this design tests.>

## Goals
- G1: <observable outcome>

## Non-goals
- <explicitly out of scope>

## Constraints
- <platform, budget, team, compliance, deadline>

## Current state
<What already exists that this design touches, with paths. Omit for a greenfield system.>

## Design map
| Level | Doc | Status |
| --- | --- | --- |
| 1 Context | [1-context.md](1-context.md) | approved <date> |
| 2 Containers | [2-containers.md](2-containers.md) | in review |
| 3 Components | [management-api](3-components/management-api.md) | not started |

## Glossary
| Term | Meaning |
| --- | --- |

## Decisions
| # | Level | Decision | Alternatives considered | Reason |
| --- | --- | --- | --- | --- |

## Open questions
| # | Question | Blocks | Owner |
| --- | --- | --- | --- |

## Traceability
| Goal | Delivered by |
| --- | --- |

## Build order
<Filled at hand-off: slices in dependency order, with the risks to prove first.>
```

Record a decision in the table when it is made. When the repository keeps ADRs, write decisions that are hard to reverse and the result of a real trade-off as ADRs in its format, and link them from the table.

## Level docs

```markdown
# Level <N>: <Context | Containers | Components of X | Code of Y>

Zooms into: <link to the parent element's doc> · Status: <in review | approved date>

## Diagram
<Mermaid block, title and legend.>

## Elements
| Element | Type | Technology | Responsibility |
| --- | --- | --- | --- |

## Relationships
| From | To | Purpose | Protocol | Failure behaviour |
| --- | --- | --- | --- | --- |

## Assumptions
- <stated without a user answer; confirm or replace during review>

## Deferred to the next level
- <detail deliberately left out>
```

Level 4 docs add the signatures, schemas and state tables in code blocks beneath the diagrams.

## flows.md

One section per scenario: a sentence stating the trigger and the outcome, a `sequenceDiagram` whose participants are named as they appear in the level diagrams, and a short list of the failure branches with what the caller observes in each.

# Design doc layout

Follow the repository's existing docs convention when it has one. Otherwise create:

```
docs/design/<system-slug>/
├── DESIGN.md                    spine: statements, status, decisions, traceability, build order
├── 1-context.md                 level 1 diagram and notes
├── 2-containers.md              level 2 diagram and notes
├── 3-components/<container>.md  one per container designed at level 3
├── 4-code/<component>.md        one per component designed at level 4
├── flows.md                     end-to-end sequence diagrams
└── deployment.md                when placement, identity or failure boundaries matter
```

Create each file when its level starts. `DESIGN.md` links to every other file and is the place a new reader starts.

## DESIGN.md

```markdown
# <System name> design

Status: <framing | level N in progress | in review | blocked | ready for planning> · Updated: <date>

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
| 4 Code | <selected component docs, or agreed deferrals and reasons> | not started |
| Flows | [flows.md](flows.md) | not started |
| Deployment | <deployment.md when needed, otherwise reason omitted> | not started |

## Glossary
| Term | Meaning |
| --- | --- |

## Decisions
| # | Level | Decision | Alternatives considered | Reason |
| --- | --- | --- | --- | --- |

## Open questions
| # | Question | Classification | Affected work | Owner |
| --- | --- | --- | --- | --- |

## Accepted risks
| # | Uncertainty and impact | User acceptance | Owner | Validation step | Must precede |
| --- | --- | --- | --- | --- | --- |

## Traceability
| Goal | Delivered by | Acceptance criterion | Verification method and conditions | Evidence/status |
| --- | --- | --- | --- | --- |

## Build order
<Filled at hand-off: slices in dependency order, with the risks to prove first.>
```

Record a decision in the table when it is made. When the repository keeps ADRs, write decisions that are hard to reverse and the result of a real trade-off as ADRs in its format, and link them from the table.

Approval statuses describe the current contents. Reopen materially changed artifacts and affected dependents as specified in [the review loop](../SKILL.md#2-descend-the-levels). Record deferred scope and its reason in the design map so an intentional omission remains distinguishable from unfinished work.

Classify open questions and record accepted risks using [the handoff criteria](../SKILL.md#4-hand-off). Traceability should specify observable pass/fail criteria and how to check them. For example: `p95 event delivery <= 10s at 100 events/s with healthy endpoints`, verified by a timed integration load test; mark it `proposed` until measured. A validation plan is not evidence that the design has passed it.

## Review publication

Keep the current design on the review branch/draft PR described in `SKILL.md`. Each level doc shows each diagram once. When embedding a rendered preview, keep editable diagram source in a separate linked source file. The PR description links to `DESIGN.md`, the current review level and its image. Push updated diagrams and docs together before requesting the next review. List existing unreviewed diagrams as candidates, not approved levels.

## Level docs

```markdown
# Level <N>: <Context | Containers | Components of X | Code of Y>

Zooms into: <link to the parent element's doc> · Status: <in review | approved date>

## Diagram
<A single rendered structural view with separately linked source, scope, title and legend.>

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

Record review status. Use one section per scenario: a sentence stating the trigger and the outcome, a `sequenceDiagram` whose participants are named as they appear in the level diagrams, and a short list of the failure branches with what the caller observes in each. Trace each participant to its deepest agreed level and identify intentionally deferred detail.

## deployment.md

When needed, record the environment, review status and a Mermaid deployment view following [the deployment guide](c4-levels.md#supporting-view-deployment). Link each runtime instance to its logical container doc and explain the relevant placement, identity and failure boundaries. Link the operational flows and acceptance criteria this view supports.

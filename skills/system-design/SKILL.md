---
name: system-design
description: Design a complex system or software architecture before planning or coding. Frame the problem statement and proposed solution, then grill the user and draw C4 diagrams level by level (context, containers, components, code), producing reviewed design docs that plan.md and implementation build from.
---

# System design

Design comes before the plan. The user states a problem and a proposed solution; you descend the C4 model one level at a time, grilling until each diagram is correct and the user approves it. The result is a design set that the user understands end to end, and that planning and implementation can follow without rediscovering the architecture.

The user's understanding is the product. A diagram the user approved without being able to explain it is a failed level, however accurate it is.

## Roles

Decisions belong to the user: put each one to them with your recommendation and wait. Facts belong to you: read the code, manifests, vendor docs and existing ADRs yourself, and cite what you found. Ask the user only what cannot be looked up.

## 1. Frame

Write two statements with the user, in this order, before any diagram.

1. **Problem statement**: what hurts today, for whom, and what it costs. It names no technology that is part of the answer. If the user's problem statement contains the solution ("we need a management plane"), grill for the pain underneath it.
2. **Proposed solution**: the approach and named technologies the user intends to use, as a hypothesis the design will test. Add goals as observable outcomes, non-goals, and hard constraints (platform, budget, team, compliance, deadlines).

Create the design directory and `DESIGN.md` from [the design doc layout](references/design-docs.md) and record both statements there. In an existing codebase, survey what already exists that the solution touches before asking anything, and record it as the current state.

Done when the user confirms both statements as written in `DESIGN.md`.

## 2. Descend the levels

Work levels 1 to 4 in order. On entering a level, read its section of [the C4 level guide](references/c4-levels.md) for its scope, element vocabulary, question bank, diagram conventions and exit checks. Run this loop at every level:

1. **Research.** Gather the facts this level depends on: existing code, the real capabilities and limits of each named technology, deployment environment. A proposed technology that cannot do what the solution assumes is a finding to raise now.
2. **Grill.** Interview the user in rounds. A round is every question whose prerequisites are already settled, numbered, each with your recommended answer and its reason. Wait for answers; they settle decisions and unblock the next round. Probe with concrete scenarios and failure cases ("the gateway is down while an agent is mid-task: what does the caller see?") in preference to abstract questions. Continue until no open question would change this level's diagram.
3. **Draw.** Write the level's diagram and its doc. Every element carries a name, a one-line responsibility and, from level 2 down, its technology. Every relationship carries a verb phrase and, from level 2 down, its protocol. Mark anything you assumed without an answer as an assumption in the doc.
4. **Review.** Present the diagram to the user: the file path, then a read-back in plain sentences of each element and relationship, the assumptions, and what the diagram deliberately leaves to the next level. Walk one key scenario through it. Ask what is wrong, missing or unclear.
5. **Refine.** Apply the corrections, grill any decision they reopen, and review again. Repeat until the user explicitly approves the level.
6. **Record.** Mark the level approved in `DESIGN.md`, log the decisions made with their alternatives and reasons, and move unresolved items to open questions with an owner.

A level is done when its exit checks pass and the user has approved it. Approval of one level is not approval of the next; start each level with a fresh grill.

Levels 3 and 4 fan out: level 3 runs once per container, level 4 once per component that warrants it. Before fanning out, agree the order and the set with the user, and complete the loop for one target before starting the next.

**Consistency across levels.** Each element at a level lives inside exactly one element of the level above, and each relationship that crosses a boundary appears, at coarser grain, in the level above. When a lower level reveals that an upper diagram is wrong, correct the upper diagram and its doc first, tell the user what changed, then continue. Use one name for one thing across every diagram and doc; record the names in the glossary in `DESIGN.md`.

## 3. Tie it together

After level 4, prove the design holds as a whole. With the user, choose the scenarios that matter: the main success paths, the most important failure, and one operational path (deploy, upgrade or recovery). For each, write a sequence diagram in `flows.md` that follows the request through every level, naming the container, component and code element at each hop.

Then complete the traceability table in `DESIGN.md`: each goal mapped to the elements that deliver it, and each element mapped to a goal. A goal with no element is a gap; an element with no goal is scope to cut or justify. Resolve both with the user.

Done when every chosen scenario traces through the diagrams without an undrawn element or relationship, and the user can narrate one of them back.

## 4. Hand off

Finish `DESIGN.md` with a build order derived from the dependency direction in the diagrams, the risks worth proving early, and the remaining open questions. State that the design is ready for planning. Planning and implementation are separate work: write `plan.md` or code only when the user asks, and build it from this design set.

When implementation later contradicts the design, update the affected diagram and doc in the same change so the design set stays a true map of the code.

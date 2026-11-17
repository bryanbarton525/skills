---
name: system-design
description: Design a complex system or software architecture before writing a plan or code. Frames the problem statement and proposed solution, then grills the user and draws C4 diagrams level by level (context, containers, components, code) into reviewed design docs that plan.md and implementation build from. Use whenever the user wants to design, architect or think through a new system, platform, service or major feature, asks for C4 or architecture diagrams, wants a design doc before plan.md, or wants to understand how the pieces of a proposed system tie together, even if they never say "C4".
---

# System design

Design comes before the plan. The user states a problem and a proposed solution; you descend the C4 model one level at a time, grilling until each diagram is correct and the user approves it. The result is a design set that the user understands end to end, and that planning and implementation can follow without rediscovering the architecture.

The user's understanding is the product. A diagram the user approved without being able to explain it is a failed level, however accurate it is.

## Roles

Decisions belong to the user: put each one to them with your recommendation and wait. A decision you make silently is one the user cannot explain later, which defeats the point. Facts belong to you: read the code, manifests, vendor docs and existing ADRs yourself, and cite what you found. Ask the user only what cannot be looked up, so their attention goes to judgement rather than lookups.

## 1. Frame

Write two statements with the user, in this order, before any diagram.

1. **Problem statement**: what hurts today, for whom, and what it costs. It names no technology that is part of the answer, because a problem framed as a solution can only ever be solved one way. If the user's problem statement contains the solution ("we need a management plane"), grill for the pain underneath it.
2. **Proposed solution**: the approach and named technologies the user intends to use, as a hypothesis the design will test. Treating it as a hypothesis lets later levels push back when a technology cannot do what the solution assumes. Add goals as observable outcomes, non-goals, and hard constraints (platform, budget, team, compliance, deadlines). Give each goal an acceptance criterion and a way to verify it, including relevant quality attributes such as reliability, latency or cost. Recommend measurable targets where missing, and confirm them with the user.

Create the design directory and `DESIGN.md` from [the design doc layout](references/design-docs.md) and record both statements there. In an existing codebase, survey what already exists that the solution touches before asking anything, and record it as the current state.

Done when the user confirms both statements as written in `DESIGN.md`.

## 2. Descend the levels

Work levels 1 to 4 in order. Each level's decisions are the prerequisites of the next: containers cannot be chosen until the boundary is agreed, and components cannot be cut until the containers are. Working one level at a time also keeps each review small enough for the user to hold in their head. On entering a level, read its section of [the C4 level guide](references/c4-levels.md) for its scope, element vocabulary, question bank, diagram conventions and exit checks. Run this loop at every level:

1. **Research.** Gather the facts this level depends on: existing code, the real capabilities and limits of each named technology, deployment environment. A proposed technology that cannot do what the solution assumes is a finding to raise now.
2. **Grill.** Interview the user in rounds. A round is every question whose prerequisites are already settled, numbered, each with your recommended answer and its reason. Wait for answers; they settle decisions and unblock the next round. Probe with concrete scenarios and failure cases ("the gateway is down while an agent is mid-task: what does the caller see?") in preference to abstract questions. Continue until no open question would change this level's diagram.
3. **Draw.** Write the level's diagram and its doc. Every element carries a name, a one-line responsibility and, from level 2 down, its technology. Every relationship carries a verb phrase and, from level 2 down, its protocol. Mark anything you assumed without an answer as an assumption in the doc.
4. **Review.** Show the diagram in the response using a rendered Mermaid block, or provide an accessible rendered preview when the interface cannot render Mermaid. Check rendering with available tooling; if rendering is unavailable, say so and provide the Mermaid source and a plain-language walkthrough. Link the saved doc alongside the visual. Read back each element and relationship, the assumptions, and what the diagram deliberately leaves to the next level. Walk one key scenario through it. Ask what is wrong, missing or unclear. The visual and read-back let the user review both the structure and what it means.
5. **Refine.** Apply the corrections, grill any decision they reopen, and review again. Repeat until the user explicitly approves the level.
6. **Record.** Mark the level approved in `DESIGN.md`, log the decisions made with their alternatives and reasons, and move unresolved items to open questions with an owner.

A level is done when its exit checks pass and the user has approved it. Approval of one level is not approval of the next; start each level with a fresh grill.

Levels 3 and 4 fan out: level 3 runs once per container, level 4 once per component that warrants it. Before fanning out, agree the order and the set with the user, and complete the loop for one target before starting the next.

**Consistency across levels.** Each element at a level lives inside exactly one element of the level above, and each relationship that crosses a boundary appears, at coarser grain, in the level above. Use one name for one thing across every diagram and doc; record the names in the glossary in `DESIGN.md`.

**Reopen changed decisions.** When a correction changes approved responsibilities, interfaces, relationships, technology choices or trust boundaries, mark that diagram and its doc `in review` in both the level doc and `DESIGN.md`. Check dependent diagrams, flows and acceptance criteria; mark affected approved artifacts `in review` too, while preserving unaffected approvals. If a lower level exposes an error above it, revise and present the upper level first, explain the impact, and wait for renewed approval before resuming dependent design work. Review affected downstream artifacts in order. Approval applies to the version shown; a rejection or correction starts another review round. Editorial fixes that preserve meaning do not reopen approval.

## 3. Tie it together

After the agreed level 4 work, prove the design holds as a whole. With the user, choose the scenarios that matter: the main success paths, the most important failure, and one operational path (deploy, upgrade or recovery). For each, write a sequence diagram in `flows.md` that follows each hop to its deepest agreed level, using names from the approved diagrams. A component deliberately left out of level 4 remains a component in the flow; record the deferred detail and its reason rather than inventing code elements. Use separate diagrams for different zoom levels when that makes the walkthrough easier to follow.

When infrastructure placement, identity or failure isolation affects the design, add `deployment.md` using [the deployment view guide](references/c4-levels.md#supporting-view-deployment). Start it alongside level 2 when those concerns drive container decisions, and finalize it with the operational flows. Review it with the same loop and keep it consistent with the logical container diagram. An operational sequence explains what happens over time; this view explains where the software runs.

Then complete the traceability table in `DESIGN.md`: each goal mapped to the elements that deliver it, its acceptance criterion and the verification method. Include the workload, failure conditions or baseline needed to make measurements meaningful. Distinguish proposed checks from evidence already collected. Each element must support a goal; a goal with no element is a gap, and an element with no goal is scope to cut or justify. Resolve both with the user.

Done when every chosen scenario traces through the agreed diagrams without an unexplained element or relationship, every goal has a verification method, the user has approved the flows and any deployment view, and the user can narrate one scenario back.

## 4. Hand off

Finish `DESIGN.md` with a build order derived from the dependency direction in the diagrams, the risks worth proving early, and the remaining open questions. Classify each question as an architecture blocker or a deferred implementation detail. A question is a blocker if its answer could change feasibility, boundaries, contracts, technology choices or the ability to meet an acceptance criterion.

Mark the design `ready for planning` only when all required artifacts have current approval and each blocker is resolved or explicitly accepted by the user as a risk. For each accepted risk, record the uncertainty, impact, owner, validation step and the work it must precede; planning must respect that dependency. If a blocker remains unaccepted, keep the status `blocked` and identify the evidence or decision needed. Deferred implementation details carry an owner and the work they affect.

Planning and implementation are separate work: write `plan.md` or code only when the user asks, and build it from this design set. Stopping here gives the user a clean point to review the whole design before effort shifts to building it.

When implementation later contradicts the design, update the affected diagram and doc in the same change so the design set stays a true map of the code.

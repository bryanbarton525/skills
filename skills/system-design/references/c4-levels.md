# C4 level guide

Each level zooms into one element of the level above. Read the section for the level you are entering. The loop that uses these sections is in [SKILL.md](../SKILL.md).

## Diagram conventions (all levels)

Prefer LikeC4 for browsable structural views. Use editable DOT and a static render for standalone figures when that suits the review. Use the repository’s established renderer if it can reproduce the same conventions. Keep one box per element in a view. Put the name, C4 type, known technology and one-line responsibility on the box. Give an undecided technology an explicit review note.

Use rounded boxes with dark text on white. Fill elements in scope pale blue (#d7eaf8), neighbours grey (#edf0f3), and outline the named parent boundary in blue (#41769b). Put the view type, subject and key on the image. Draw a directed arrow from the dependent element to its dependency. Label it with the action and the protocol for inter-process communication. Match the action label to the arrow color. For platform architectures use purple (#703b89) for publication/configuration, blue (#145886) for access, green (#146451) for execution and brown (#8b4a13) for state. Choose meaningful categories once per project and carry the same key across views. Labels must convey the meaning in greyscale.

Level 1 shows one product with its people and neighbours. Level 2 opens the product into applications and stores. Each level 3 view opens one named container. Each level 4 view opens one named component into code elements. Use separate linked sequence or path drawings for a time-ordered journey. Keep a prototype code view explicitly scoped to its example.

Start from the [editable component example](component-example.dot). Render with `dot -Tsvg component-example.dot -o component-example.svg`. Inspect the image at the width reviewers will see. Check for crossed paths, clipped labels, ambiguous arrowheads and boundary labels obscured by edges. Show one rendered representation per diagram and link its editable source.

When presenting several levels together, lead with a zoom overview. Select one traceable branch. Highlight the exact parent box, draw a labeled zoom connector from it to the next panel, and repeat its name and outline color at the expanded scope. Distinguish zoom connectors from runtime dependencies. Show a legible subset in each panel and link the full diagrams. Mark any level drawn from example code. If a lower level has no agreed design or code, end the branch there and name the gap. [Archi example](https://www.archimatetool.com/wp-content/uploads/2020/04/c4-overview.png) · [Archimetric overview](https://www.archimetric.com/the-comprehensive-guide-to-the-c4-model-for-software-architecture/)

## Level 1: System context

**Scope.** The system as one box, the people who use it and the external systems it depends on or serves. No internals, no technology inside the box.

**Elements.** Person (a role, not an individual), the system, external systems (anything the team does not build or operate as part of this design, including adopted platforms and third-party services).

**Grill for.**

- Who uses it, in which roles, and what each is trying to get done? Which role matters most?
- What is inside the system boundary, and what is an external system the design adopts as is?
- What does the system call, and what calls it? Which of those already exist?
- What data crosses the boundary, in which direction, and who owns it?
- Who is trusted, how do they authenticate, and who must be kept out?
- What happens to users when each external system is unavailable?
- What is explicitly out of scope for this design?

**Exit checks.** Every person and external system has a labelled relationship to the system. Every goal in `DESIGN.md` is visible as at least one relationship. The boundary answers "do we build this or use it" for every named technology in the proposed solution.

## Level 2: Containers

**Scope.** Inside the system boundary: each separately deployable or runnable unit and each data store, with the technology chosen and how they communicate.

**Elements.** Container: service, web or CLI application, worker, controller or operator, database, queue, object store. A C4 container is an application or data store, independent of how it is packaged or deployed. Kubernetes CRDs define API schemas; document them as contracts of the API/controller and show the relevant storage boundary. The controller/operator is a runnable container; a CRD is not. Level 1 people and external systems reappear as neighbours. See the [C4 container definition](https://c4model.com/abstractions/container).

**Grill for.**

- What are the deployable units, and why is each one separate (scaling, failure isolation, ownership, release cadence, security boundary)?
- What technology does each use, and what alternative was rejected?
- Where does each piece of state live, and which single container owns writes to it?
- How does each pair communicate: synchronous or asynchronous, which protocol, who initiates?
- Where are the trust boundaries, and how is identity carried across each hop?
- What fails when each container is down, and what keeps working?
- How is it deployed, configured, upgraded and observed?
- For an adopted platform, which parts are configured and which are extended with custom code?

**Exit checks.** Every level 1 relationship lands on a specific container. Every container has a technology, one owner of each store is identified, and every edge has a protocol. A request for the main scenario can be traced container to container.

## Level 3: Components

**Scope.** Inside one container: the major structural parts, their responsibilities and their interfaces. Run once per container the team builds. A container that is adopted unmodified, or a plain data store, needs no component diagram; record that choice.

**Elements.** Component: a module, package or group of code behind an interface, such as an API handler set, a reconciler, a domain service, a repository, an adapter to an external system. Neighbouring containers appear as single boxes.

**Grill for.**

- What are the responsibilities of this container, and which component holds each one?
- What is each component's interface, and what does it hide?
- Which direction do dependencies run, and where are the seams for testing and replacement?
- Which component owns each external call and each store access?
- Where are validation, authorization, retries, idempotency and error translation handled?
- What runs concurrently, and what state is shared?
- Which components carry the real complexity or risk?

**Exit checks.** Every level 2 edge touching this container lands on a specific component. Each component has one stated responsibility and dependencies form no cycle. The user can name which component they would open to change a given behaviour.

## Level 4: Code

**Scope.** Inside one component: the types, interfaces, data shapes and state that implementers must agree on before writing it. This is a design of contracts, not a drawing of every class. Run for the components the user selects; recommend those with public contracts, persistent schemas, state machines, concurrency or nontrivial algorithms, and record the ones left to implementation.

**Diagrams.** Show structural relationships among types, interfaces or stored data. Link supporting state and sequence views when lifecycle or call order needs explanation. Pair diagrams with the actual signatures or schemas in code blocks in the project's language.

**Grill for.**

- What are the public interfaces and their exact signatures? What do callers need to know and nothing more?
- What are the core types and their invariants? Which states are legal, and what moves between them?
- What is the stored schema, its keys and its versioning or migration path?
- What errors exist, which are retryable, and how do they surface to the caller?
- What is the concurrency model, and who owns each resource's lifetime?
- How is each piece tested, and what is faked at the seam?
- Which project conventions (layout, naming, error handling) apply?

**Exit checks.** Every level 3 interface of the component in scope has a concrete signature or schema. Every state machine shows its terminal and failure states. An implementer could write the first test for this component from the doc alone. Components deliberately deferred retain their level 3 contracts and a recorded reason for deferral.

## Supporting view: Deployment

Use when placement, identity or infrastructure failure boundaries affect the architecture, such as a Kubernetes platform spanning namespaces or clusters. This supplements the logical levels; it is not a fifth level. See the [C4 deployment diagram guidance](https://c4model.com/diagrams/deployment).

**Scope.** One named environment, such as production. Show instances of the existing containers inside nested deployment nodes using Mermaid `flowchart` subgraphs. Keep logical container names recognizable and distinguish replicas from separate containers.

**Grill for.**

- Where does each container run, and what infrastructure or managed service hosts it?
- Which cluster, namespace, zone or host boundaries affect placement and failure isolation?
- Which identities, permissions, ingress and network boundaries govern communication?
- What happens when a replica, node, zone or external dependency fails?
- How do rollout, rollback and recovery preserve the agreed availability and data guarantees?

**Exit checks.** Each runtime instance maps to a logical container; relevant infrastructure nodes, identity and failure boundaries are explicit. The operational flow agrees with the deployment view and the relevant acceptance criteria. Record and review infrastructure decisions through the same design loop.


## Navigable architecture reviews

Give each element a stable ID and define it once. Reuse it in scoped views and dynamic sequences. Label relationships with actions and carry meaning in text as well as color. Link responsibilities to the design record and distinguish accepted behavior, experimental code and open questions. Stop each branch where the evidence ends.

Publish a browser-accessible explorer using the repository’s approved access path. Link the context entry, a representative deep view and the editable model. Preserve published view IDs across revisions. Validate and build the model, then open the built artifact and exercise parent-to-child navigation, back navigation and a sequence. For protected hosting, report the rollout, sign-in gate and authenticated browser check separately.

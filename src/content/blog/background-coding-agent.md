---
title: 'A background coding agent is a trust machine'
description: 'What I learned building Clipper, an agent that turns an issue into a pull request on a large, containerized, mostly PHP codebase.'
pubDate: '2026-09-15'
heroImage: '../../assets/illustrations/background-coding-agent/00-header.png'
subject: 'Coding agents'
---

Over the summer I led the design of **Clipper** at Evaneos, where I work: you give it an issue, it writes the code, checks it, and opens a pull request, without anyone at the keyboard. A background agent. A small team built it with me, and it now belongs to our R&D teams.

The first version that "works" takes an afternoon: a headless agent in a CI job, a token, and the agent reads the issue, patches, pushes. The demo is spectacular, and misleading. Whether a model can write code stopped being the question a while ago. The question that shaped every design choice I made was another one: **can you trust the pull request that comes out?**

## The bar is trust, not code

Context matters here. I work on a large fleet of applications, mostly PHP, some of it legacy, everything containerized: tests run against a database and message queues started in Docker. Nothing like a greenfield project where `npm test` answers in three seconds.

In that world, code from an agent has no value by itself. A pull request a reviewer has to redo from scratch costs *more* than one written by hand, because you first have to understand what the agent believed it was doing. Value appears only when the PR is reliable enough for the review to become a check rather than an investigation.

Moving from "the agent produces code" to "the agent produces confidence" became my first design principle. The rest follows.

## Execution and review are two systems

I kept two things apart that are often packed together:

- **execution**, from an issue to a pull request: that's Clipper;
- **review**, from a pull request to well-directed human attention: who should read it, what is the blast radius, where to look.

Execution is optimistic by nature; review has to doubt. Asking the same agent to write and then judge its own work is exactly how you manufacture a *false green*. The pull request is the clean border between the two: Clipper produces an artifact, and review picks it up cold, without inheriting the optimism of the run.

## From one opaque run to a workflow engine

Clipper started as a **single run**: one agent call, a verify loop inside it, a PR at the end. It works on small, well-framed tasks and breaks silently on bigger ones. When the agent heads the wrong way after ten minutes, you only find out at the end, after paying for the whole run.

So I split the run into **phases with checkpoints**, first as chained CI jobs, then on a typed workflow engine. Today a run goes through analysis, decomposition into slices, builds of those slices (in parallel when they don't collide) and an integration step that opens the PR. Artifacts passing from one phase to the next are validated by schema, and a run can pause at a gate and resume later:

- a **plan gate**, where a human approves, revises or rejects the decomposition;
- a **question gate**, when the task is ambiguous and the agent needs an answer before going on.

![A canal lock: a barge waits in the chamber, both pairs of gates closed, until the next one opens.](../../assets/illustrations/background-coding-agent/01-canal-locks.png)

The engine became a small platform: workers that run phases, a live view of each run as a conversation, single sign-on, a GitHub App so the agent acts on behalf of the person who asked. And one thing I refused from the start: duplicating pipelines. **You extend the system by adding skills and gates, not new pipelines.** One infrastructure composes several workflows.

The definition of done also moved. A run is done when **the pull request's own CI is green**, not when the agent says so. When CI fails, a bounded repair loop gets two attempts, with an adversarial reviewer on each fix, and otherwise the PR stays a draft. The CI of the repository is the final oracle.

## Size beats context, and splitting has a price

The most counter-intuitive lesson from dogfooding: **a task that doesn't converge is rarely a context problem. It is a size problem.**

On a well-sized task (a precise bug in event-driven code), the agent is autonomous: static analysis, unit and functional tests green on the first pass, run after run. On a huge one (removing a feature spread across thirty files), the same agent spins, blocks, and burns its turn budget. The naive reflex is to give it more: more context, more checks, more turns. Each added check divides its budget instead.

Hence decomposition: smaller slices, each built with a fresh context. But decomposition has a price, and we found it the hard way. Once non-developers started using Clipper for small changes, a trivial task took **an hour and forty-five minutes** through analysis, three waves of builds and integration. Built directly, the same kind of task took **seventeen minutes**. Decomposition was turned off by default for those uses. I let it happen to unblock people, but I don't think it's the answer.

The answer I believe in is a router: send trivial work straight to a build, keep decomposition for what deserves it. Freedom upstream, constraints downstream, and the right amount of machinery for the size of the task.

![Railway points: a single wagon goes straight on, a long train is switched to a siding.](../../assets/illustrations/background-coding-agent/02-railway-points.png)

## No false green

One invariant a background agent can never break: **it must never report green when it is red.** A false positive is worse than an honest failure, because it destroys exactly the confidence you are building. Containers attacked that invariant twice, and both times I didn't see it coming.

**The baked image.** Our CI images contain the source code at build time. The agent edits files afterwards. Our verification was testing the code frozen in the image, not the code the agent had just written, and the repository's own CI then found the error Clipper had declared absent.

**Stateful checks run twice.** The loop ran verification when the agent tried to stop, and a final gate ran it again. For idempotent checks, fine. For functional tests that write to a database and queues, the first pass was green and the second failed massively on the leftovers of the first. The fix is not a reset between runs, it's **tiering**: fast, idempotent checks run inside the agent's loop; slow, stateful ones run once, at the end, on a clean state. The nature of a check decides where it is allowed to run.

Both traps point to the same need: a **real, clean, disposable environment** for every run. Clipper now provisions an ephemeral environment in parallel with the work, puts its link in the pull request, and tests its own change in it through a browser. Agents also run in an isolated sandbox with public egress only.

## Gates that advise, gates that block

When people outside engineering started using Clipper (a translation, a wording change), a new kind of failure appeared: the diff was right, but environment verification failed for reasons that had nothing to do with the change, and a blocking gate turned a good PR into a dead run.

So environment verification became **advisory**: its verdict goes into the pull request as a comment, for the reviewer, instead of preventing the PR. The rule I ended up with: block on what proves the change is wrong, inform on what only raises doubt. A gate that blocks on noise teaches people to route around it.

![A level crossing: the gates are closed across the road, while the semaphore further along only signals.](../../assets/illustrations/background-coding-agent/03-signal-and-barrier.png)

## A thin harness

One thread runs through all of my choices: **the harness stays thin.** It types, sequences, and puts deterministic gates at the seams. It does not reason in place of the model.

The temptation, when you tool an agent, is to stack machinery: giant prompts, orchestration layers, custom logic that redoes what the model already does natively. It's a losing bet, because models improve fast, and every line of harness that duplicates a native capability becomes debt the day the model does better on its own. A thin harness is also one people can understand, and understanding is what trust is made of: a developer needs to know what the pipeline guarantees mechanically (the tests really passed, against the real code) and what it does not (design judgment stays human).

## What is still open

- **Routing by size.** Turning decomposition off was a shortcut; deciding automatically what deserves it is the real answer.
- **Where ephemeral environments run.** A production-like stack takes minutes to start, and every run pays for it. The trade-off between cost, concurrency and horizontal scale is the main industrialization question.
- **Cost and rate limits.** The fleet's limit turned out to be the model provider's rate limits, not our machines. A budget per run is part of the design, not an optimization for later.
- **Joining the review side**: trigger, execution, PR, routing the review to the right expert, human merge. That's where the two systems become one loop.

What I'm sure of, though: trust is not declared, it's built piece by piece, and each piece must be usable on its own. An agent that produces reliable pull requests on a narrow scope is worth far more than a demo that touches everything and that nobody dares to merge.

The only metric I really care about: not *how much code the agent writes*, but *how often we merge without looking twice*.

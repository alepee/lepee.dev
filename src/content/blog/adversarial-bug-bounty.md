---
title: 'Find generously, refute coldly'
description: 'An adversarial bug bounty with a fleet of agents: finders that over-produce, skeptics that start from disbelief, and the waste worth cutting.'
pubDate: '2026-06-09'
updatedDate: '2026-10-07'
heroImage: '../../assets/illustrations/adversarial-bug-bounty/00-header.png'
subject: 'Coding agents'
---

An agent reviewing code on its own produces findings that are plausible and wrong. Claiming a bug costs it nothing; checking the claim costs a human an hour. Ask it to be careful and it finds less. Ask it to find more and you drown in false positives. Recall and precision pull against each other inside a single context.

So split them. Give recall to one set of agents and precision to another, and put a wall between them. That's the idea of an adversarial bug bounty, and it works better than I expected. Here is the pattern, what it costs, and where the money is wasted.

## Find generously, refute coldly

Two phases, with a barrier in between.

**Finders** are told to over-produce. Their job is recall, not precision. Each one covers a single dimension of review (correctness, concurrency, types and units, lifecycle, security, error handling) and is blind to the others.

**A deduplication step** sits on the barrier. Finders with different lenses regularly land on the same problem under different names, so candidates that point at the same mechanism are merged into one claim before anyone tries to refute them.

**Skeptics** get almost nothing: the claim, a `file:line` pointer and a one-sentence failure scenario. **Never the finder's reasoning.** They must re-derive the failure path by hand on the real code, start from the assumption that the claim is wrong, and, when they reject it, say why with one of a few classes: unreachable, by design, handled elsewhere, not a bug. Two skeptics per claim: two confirmations and it survives, two refutations and it's gone. When they disagree, which happens on one or two claims out of ten, a third skeptic breaks the tie with the two sets of evidence, not the reasoning.

Three rules hold the whole thing up:

1. **A fresh context for every skeptic.** Share the finder's reasoning and refutation turns into confirmation bias.
2. **No verdict without evidence.** Every verdict cites code; a structured output schema makes it non-negotiable.
3. **Survivors are inferred, not confirmed.** The fleet pre-filters. Only something outside it (a test that reproduces the bug, a fix, an incident) confirms.

## What it costs

To calibrate it, I ran an early version once at scale, before the deduplication and the tie-breaker existed: six finders, two skeptics per candidate, **190 agents in 36 minutes**. Of 92 candidates, 48 % were refuted, 14 % ended split and 38 % survived, about twenty unique bugs once duplicates were merged by hand. The bill was about **$360**, roughly $15 per surviving bug, and it would have been $1,660 without prompt caching.

![A bag of coins flying away on a pair of feathered wings, dropping a few coins as it goes.](../../assets/illustrations/adversarial-bug-bounty/01-flying-money.png)

A refutation rate around half is healthy, not waste: precision comes from refutation, not from timid finders. If your skeptics rarely refute, your finders aren't trying hard enough. And the survivors were real, mostly the kind you don't find by reading: interactions between settings, lifecycle edge cases, data silently lost or counted twice.

The cost was very lopsided: **refutation took 77 % of the budget.** Fresh contexts are expensive by construction: every skeptic reads the relevant code from scratch. That run also showed where the waste was, and that's where the two later steps came from:

- **Duplicates by meaning, not by text.** Deduplicating on file, line and title let the same bug, found by three finders under three titles, reach refutation three times: six skeptics doing identical work, about 30 % of the survivors. Worse, two findings survived under one framing and were refuted under another (the same data loss confirmed as an error-handling bug, rejected as an accepted concurrency trade-off). Merging by mechanism before refuting fixes both.
- **Split votes pile up.** 14 % of the candidates ended *unknown*: honest, but each one is human work postponed. A third skeptic on disagreement costs a few agents and clears them.
- **Refutation classes must fit the audit.** "Pre-existing" makes sense when reviewing a pull request, none when auditing a whole codebase. A confused agent at frontier prices is the most expensive kind.

## The same idea, priced differently

A colleague built his own version of the pattern, and comparing the two taught me as much as the run did. His trade-offs were the opposite of mine on almost every point.

- **One skeptic per packet, not two per claim.** His finders' output is grouped into packets of at most five findings, one skeptic each. Five came out of many benchmark runs: beyond that, too many false positives slip through. Two skeptics per finding was simply too expensive for him.
- **Fewer false positives at the source.** Rather than paying skeptics to catch them, he spent a lot of experiments making the finders produce less noise in the first place.
- **The cost isn't where you think.** On his runs, 96 % of what the agents consume is cache reads. Skeptics don't reason much; they read.
- **A human in the loop.** His review runs on a pull request and ends in a table a developer decides on: fix, skip, needs a human, or known limit (two fix attempts already failed). Mine runs unattended, overnight, with nobody reading the findings, which is exactly why false positives cost me so much and why I keep two skeptics.

We agreed on the part that isn't negotiable: the reviewers must be separate agents, isolated from the context that wrote the code. And we disagreed, usefully, on the rest. With a single skeptic per packet, a skeptic that is wrong is wrong alone; that's where I think you become blind. With two per claim, you pay for it. The idea we left on the table sits in between: hand each skeptic's evidence to a tiny, nearly free model that scores how solid it is, and only launch a second skeptic when the score is low. Put a near-free model on the output of the things that cost a lot.

## What I would still change

Estimates, not measurements:

- **Escalate instead of doubling up.** Run the first vote on a mid-sized model; about half of the refutations were easy ones (a misread, an obviously unreachable path). Call the frontier model only when the first vote confirms or hesitates. The confidence-scoring idea above is the cheapest version of the same move.
- **Batch the skeptics.** Refutation is massively parallel and doesn't care about latency. A batch API halves that line of cost, at the price of a longer run: fine for a nightly audit, not for an interactive one.
- **Design prompts for the cache.** Caching is already the difference between $360 and $1,660. Keep the skeptics' preamble identical byte for byte, put the claim last, never interpolate timestamps or run IDs into the shared prefix, and schedule skeptics working on the same file together so they hit a warm cache.
- **Remember what was refuted.** Refuted findings, with their class and reasoning, are an asset. Feed them to the deduplication step (not to the finders, which would bias recall): a rediscovered claim already refuted skips refutation unless its code has changed.
- **Pick a model per role.** Finders, skeptics and the orchestrator don't need the same model. Public bug-finding benchmarks now make that choice measurable, and staying provider-agnostic is a side benefit.

## When to use it, and when not

Use it when the blast radius is high, the codebase is unfamiliar or long-lived, or a review backlog makes pre-filtered, evidence-backed findings worth about $15 each. Don't use it on a small diff (one adversarial reviewer after implementation does the job for a fraction of the tokens), on a prototype, or anywhere a false positive costs minutes rather than hours.

And it's always a human who starts it, never an agent. Burning seven-figure token counts is a budget decision, and announcing the expected cost before launch is part of the deal.

What I keep from it goes beyond bug hunting: **redundancy is what you pay for, and waste is what you cut.** Blind finders, evidence-only handoffs and a default of disbelief make the pattern work. How much redundancy to buy depends on who reads the output: a developer deciding on a table can afford one skeptic; a loop that ships overnight can't.

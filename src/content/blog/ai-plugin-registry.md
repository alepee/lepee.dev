---
title: 'Skills are company assets'
description: 'A skill is know-how written down for an agent. Left alone, skills get copied, drift and vanish. Managed like assets, they become one of the pillars that make agents useful, and lasting, in a company.'
pubDate: '2026-09-28'
updatedDate: '2026-11-18'
heroImage: '../../assets/illustrations/ai-plugin-registry/00-header.png'
subject: 'Skills & plugins'
---

By the summer, skills were everywhere at work and nowhere in particular. People shared them as zip files on Slack, reinstalled them after every change, improved the same one in parallel and ended up with copies of the same name drifting apart. A designer had three proposals from colleagues waiting somewhere in a marketplace, with no idea what had happened to them. Nobody could say which version of a skill was the right one.

It looked like a tooling problem. It's really a question of what skills *are*.

## A skill is know-how, written down

A skill tells an agent how something is done here: the steps of a procedure, the conventions to follow, the context it needs, when to use it and when not to. A code review checklist, a brand's tone of voice, the way sales qualifies a lead, the way finance closes a month. Things that used to live in people's heads, in a wiki nobody reads, or in the habits of one team.

That makes skills something new: **tacit knowledge, made explicit enough for a machine to apply.** And they aren't only for engineers. Some of the most useful ones I've seen come from brand, design and sales operations.

They're also what turns a generic assistant into a colleague who knows the house. Without them, every person re-explains the same context to their agent, every day, a little differently. With them, the company's way of doing things travels with the agent.

## Unmanaged, they behave like any unmanaged asset

Things of value that nobody manages degrade in predictable ways, and skills were doing all of them:

- **Duplicated and drifting.** Three versions of the same skill, each improved by someone, none merged.
- **Without an owner.** Nobody to accept an improvement, nobody accountable when it's wrong.
- **Of unknown status.** Is this the official one, or someone's experiment? Nobody can tell from the file.
- **Invisible.** People didn't know a skill for their job already existed, and rewrote it.
- **Fragile.** A skill lives on someone's laptop; when they leave, it leaves.
- **Locked in.** Written in one assistant's format, it dies with that assistant, or with that format's next version.

None of this is specific to AI. It's what happens to code without a repository, to documents without a home, to any asset without a register.

## So manage them like assets

That's what the registry I built at work is for: one place where anyone, engineer or not, publishes, finds and improves skills and MCP servers, and uses them in whichever assistant they work with. Each property of an asset maps to a design choice:

- **An inventory.** One catalogue, searchable from the web and from inside the assistant. The content and its full history live in Git; the catalogue, owners and channels live in a database.
- **Ownership and governance.** Plugins are either **open**, where anyone can add to them, or **protected**: administered by their owners, who decide which skills, connectors and hooks go in. Running the registry doesn't make you the owner of anyone's plugin.
- **Quality.** Every publication goes through checks, some of them judged by a model, most of them warnings rather than refusals. They taught me something about my own skills: none of my descriptions said *when* to use them.
- **Versioning and distribution.** A fix published once reaches everyone, automatically. That sounds obvious; it wasn't the default, and for weeks updates reached nobody.
- **Portability.** The registry follows a vendor-neutral standard and stores what a component is *meant* to do, then projects it to each assistant's format. Assistants and formats will change; the know-how shouldn't have to be rewritten each time.
- **Measurement.** Usage is tracked like a product, with a twist: in the analytics, the user is the agent, a person and their assistant.

## One pillar among a few

Making agents work in a company rests on a handful of pillars: access to models, context about the company and its data, security around what agents can reach, and people who know how to use them. Skills are one of those pillars, the one that carries *how we do things*.

It's also the one that makes the investment last. Models get replaced every few months, assistants come and go, but a well-written procedure, owned and versioned, survives all of them. A company that treats its skills as assets keeps its know-how when it changes tools; one that leaves them on laptops starts over every time.

## What people taught me along the way

I expected people to ask for search. They asked for trust.

- **Governance before discoverability.** The first person I interviewed outside engineering, in sales operations, said before any demo that the most important thing was "someone who tells me this is the official one". Protected plugins, with a named owner, are the answer to that sentence.
- **Control must be real, not just visible.** Brand and design teams didn't fear sharing; they feared a skill that *looks* official without anyone owning it.
- **Checks speak engineer.** The first import by a designer produced 361 errors, most of them component identifiers mistaken for secrets. The checks were right on substance and wrong on language for her.
- **A proposal nobody sees is a proposal nobody accepts.** The loop worked from day one; nothing told the owner something was waiting.
- **Installing must be a button.** "Add this marketplace to your settings" means nothing to most people. A button, or a prompt to paste, works.

And the work around the tool was most of the work: onboarding team by team, in each community's own words, a talk to the whole company, and retiring the old marketplace on a date announced early and kept.

## Where it stands

Two months after production: **163 components, 34 contributors, 62 % of the people concerned with an account, and half of them with an assistant connected.**

Not everything worked. Ownership is rarely shared: owners still review proposals to their plugins alone. You can't install one skill without its whole plugin. And agents turned out to be expensive contributors, opening pull requests day and night.

But the shift that matters has happened. Skills stopped being personal tricks passed around in zip files, and became something the company owns, improves and keeps.

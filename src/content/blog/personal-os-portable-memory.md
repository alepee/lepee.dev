---
title: 'Your agent forgets. Your memory should not.'
description: 'Why I keep my coding agents'' memory in plain Markdown files that outlive any single harness.'
pubDate: '2026-11-21'
heroImage: '../../assets/illustrations/personal-os-portable-memory/00-header.png'
subject: 'Agent memory'
---

Every session with a coding agent starts from zero. The agent is brilliant for two hours, then the window closes and everything it learned about me, my projects and the decisions we took together is gone. The next session asks the same questions, rediscovers the same constraints, and sometimes undoes a choice we made the day before.

The tools answer this with built-in memory. Claude Code has its memory files, Codex its own, every new harness ships another one. Each of them works, inside its own walls. The day I open a different tool, or the day the tool changes its format, that memory stays behind.

I work with several agents every day. So I made the opposite bet: **the memory belongs to me, not to the agent**, and it lives in files any agent can read.

## The rule: capture a lot while it is hot, curate a little when it is cold

The whole system hangs on one sentence. During work, the agent writes down what matters, generously, in an append-only journal. Later, away from the work, a slower pass decides what deserves to last, and I approve every promotion to long-term memory.

Capture is cheap and frequent. Curation is rare and supervised. Mixing the two is how memory systems rot: an agent that rewrites its long-term memory in the middle of a task ends up keeping what was salient at 3 pm on a Tuesday, not what is true.

## Plain Markdown, versioned

The memory is a folder of Markdown files with a bit of YAML front matter. One file is one note. Relations between notes are wikilinks in the front matter (`Belongs to:`, `Related to:`), so the graph is readable by a human, by an agent with nothing but `cat` and `grep`, and by any note-taking app that understands wikilinks.

Everything is versioned. When an agent gets something wrong, I see exactly what changed, and I can always go back to what the system believed last month.

![Cross-section of a nautilus shell: every chamber, from the first to the last, stays sealed and intact.](../../assets/illustrations/personal-os-portable-memory/01-nautilus.png)

No database, no embeddings, no service to keep running. The cost of that choice is search: past a few hundred notes, plain `grep` and an agent walking links start to show their limits. I accept the cost for now, and I wrote down when I would revisit it (more on that below).

## Four layers

The vault is made of four kinds of files, each with one job:

| Layer | Files | Role |
|---|---|---|
| Identity | `USER.md`, `SOUL.md` | Who I am, who the agent is |
| Rules | `AGENTS.md` | How the agent behaves |
| Config | `agent-config.yaml` | What it acts on, in this instance |
| State | `MEMORY.md`, daily notes | What it knows |

Identity and rules change rarely, config changes per instance, state changes every day. Keeping them apart means each one can evolve without dragging the others along.

## One rulebook, included everywhere

`AGENTS.md` is the single source of truth for every agent. The harness-specific entry points do nothing but include it: `CLAUDE.md` for Claude Code, `GEMINI.md` for Gemini CLI, while Codex and other tools that follow the `AGENTS.md` convention read it directly. Adding a harness means creating its entry file and pointing it at the rulebook. Rules are never duplicated, so they never drift apart.

![Three cells of different shapes, each carrying the same DNA helix in its nucleus.](../../assets/illustrations/personal-os-portable-memory/02-cells.png)

Configuration is kept out of the rules on purpose. `AGENTS.md` says *how* to query a source (a calendar, a chat tool, meeting notes); `agent-config.yaml` says *which* calendar, *which* workspace, *which* thresholds. The rules could be handed to someone else as they are; the config is rewritten per instance.

## Typed notes, and a small long-term memory

Not everything is a note in a flat pile. Each note declares a type in its front matter (person, project, topic, meeting, document, daily), and each type is itself a note in a `type/` folder that carries its template and its capture contract: which sections can be rewritten, which one is append-only, how a block is formatted. Adding a type to the vault means writing one file. Nothing hardcodes that a person's note grows in a *Timeline* section; whoever writes reads the type.

`MEMORY.md`, the long-term memory loaded at the start of every session, stays small: an index pointing to the typed notes, plus the few decisions and patterns that cut across them. The detail lives in the notes. Above 300 lines, the file is not split mechanically; the line count is a signal to investigate, in order: curate, migrate to typed notes, split, and only then add an index.

## Nothing is deleted

Notes that stop mattering are archived, never deleted: a flag in the front matter hides them from the active views, and they stay searchable and linked. A memory loses value when you erase it; the cost of keeping an archived note is close to zero.

![A neuron whose active branches are dark and strong, while the dormant ones are pale but still attached.](../../assets/illustrations/personal-os-portable-memory/03-neuron.png)

## What it buys me

I switch tools during the day, sometimes in the middle of a task. The next agent picks up where the last one stopped, because what it needs is in the vault, not in the previous tool.

Several agents write into the same journal. Claude Code and Codex both append to today's daily note, and each block is signed with the tool and the session it came from, so I always know who wrote what.

I can read what my agents remember. When something is wrong, I fix it in a text editor, in a file I understand, instead of asking a tool to forget.

And when a tool changes its memory format, or disappears, I lose nothing.

## What it does not solve

Writing memory is easy. Writing the *right* memory, at the right moment, without duplicating what is already there, is where the work is. It happens in three moments: capture during the session, a catch-up at the end of the day, and consolidation once a week.

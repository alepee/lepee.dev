---
title: 'One door to shared tools'
description: 'Everyone should be able to search the web from their assistant, without anyone handing out API keys. A small MCP proxy, then the registry itself, became that door. And sometimes the right door is not a shared one.'
pubDate: '2026-07-03'
updatedDate: '2026-11-05'
heroImage: '../../assets/illustrations/mcp-proxy/00-header.png'
subject: 'Skills & plugins'
---

Agents are only as useful as the tools they can reach, and web search is the first one everyone asks for. We use [Linkup](https://www.linkup.so): good results, an MCP server, an API key per account. Everyone at work should be able to use it from their assistant.

The obvious way is to give everyone a key. Then someone creates them, hands them out, rotates them, revokes them when people leave, and watches the bill of each one. Nobody wants that job, and the alternative, sharing one key in a message, is worse.

## A proxy: one sign-in, the key stays on the server

So I put a small proxy, running at the edge, in front of the MCP server:

- **One sign-in.** Assistants connect to a single address and authenticate with the company identity, through OAuth. Background agents get service tokens instead.
- **The key stays on the server.** The proxy holds the Linkup key and relays everyone's calls with it. Nobody receives a key, nobody can leak one.
- **Only the allowed tools.** Besides search and fetch, Linkup offers a research tool that runs a much deeper investigation and costs far more per call. Only search and fetch go through. Nobody launches a long, expensive research job by accident, and the cost stays predictable.
- **Configuration as code.** Upstreams, rules and filters live in one versioned file.

The filter turned out to matter as much as the key. An MCP server exposes everything its vendor thought useful; a company usually wants a subset, for cost, for safety, or simply to keep the assistant's choices clear.

## From a proxy to the registry

The proxy worked, and adding a tool to it still meant a pull request and a deployment in a repository only my team touched. The capability was there; access to it wasn't.

So its principles moved into the skill registry, where people already find the plugins they use. Whoever publishes a plugin can declare a **relayed connector**: the upstream server, the credential kept server-side, the tools allowed through. It's exposed behind the same company sign-in, to the people who installed the plugin, not to the whole organization. Two rules come with it:

- **Closed by default.** Only the tools the owner allowed are exposed. When the upstream adds a new tool, it stays hidden until the owner validates it.
- **Someone answers for it.** Protected plugins are administered by their owners, who decide what goes in, connectors included.

## When a shared door is the wrong door

Relaying one key works for Linkup because the key carries no personal rights: everyone is allowed to search the web, and the only question is cost.

Now take our HR tool. HR staff see everyone's records; an employee sees their own information and the org chart, nothing more. Put that tool behind a proxy with a single account and every agent gets the HR view. That's not a convenience, it's a leak.

For that kind of tool, each person must connect with **their own account and their own rights**. The assistant signs in as the employee, and the tool applies the permissions it already enforces: HR asks and gets the full picture, everyone else gets their own data and the org chart. The work here is not hiding a credential, it's making sure the identity travels all the way to the tool.

So the question to ask, tool by tool, is simple:

- **Is the tool's value the same for everyone, and the only issue the key or the cost?** Share the access, hold the key server-side, filter the tools. Web search is the textbook case.
- **Do the tool's own permissions matter?** Relay the person's identity, never a master key. HR, finance, anything with personal or restricted data.

## What I keep from it

- **The bottleneck is access, not capability.** A tool nobody can reach is a tool nobody uses.
- **A filter is a feature.** Exposing fewer tools keeps costs predictable and assistants focused.
- **Put the door where people already are**, next to the skills that need the tools.
- **Share access, or relay identity, but decide on purpose.** Convenience and accountability don't always point the same way.

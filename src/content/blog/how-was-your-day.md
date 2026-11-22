---
title: 'A meeting recorder that shows its sources'
description: 'How Was Your Day records, transcribes and separates voices on my Mac, then writes a summary where every point links back to the moment it comes from. The hard part was the voices.'
pubDate: '2026-10-25'
updatedDate: '2026-11-21'
heroImage: '../../assets/illustrations/how-was-your-day/00-header.png'
subject: 'Tools I build'
---

At the end of a day of meetings, I remember the decisions and not who argued for what, the action items and not the reasons behind them. Meeting assistants exist, but most of them send the audio somewhere, and all of them hand me a summary I have to take on faith. When a summary says "we agreed to postpone the launch", I want to hear who said it, and how.

So I built [How Was Your Day](https://github.com/alepee/how-was-your-day), a small Mac app with one promise: **record, transcribe and separate the voices on my own machine, then write a summary where every point links back to the moment it comes from.** In the interface, each point carries a little button like `▸ 29:13 +2`: hover to see the passages it rests on, click to jump the playback there.

## How it works

- **Capture.** The microphone and the computer's sound (the other side of a call) are recorded as two separate, synchronized tracks, in five-minute chunks. Keeping them apart is what makes everything downstream possible.
- **Transcription** runs on the Mac with Apple's speech framework, the language detected per track from the first minute and a half. I chose it over Whisper on purpose: the app has to stay light on older machines.
- **Diarization** (who speaks when) runs offline per track, and each voice gets an embedding, a numerical fingerprint used later to recognise it.
- **The summary** is optional and, honestly, the one step that isn't necessarily local: it can use a local model server, a hosted model with your own key, or your own coding agent, which hands the result back through a narrow MCP tool. A benchmark of small local models on my machine concluded, for now, that none is good enough to recommend.
- **Output** is versioned Markdown and JSON, with every generation kept and checksummed, so other tools, and agents through a read-only MCP server, can use the sessions without the app.

The privacy rules are simple: audio, notes and voice prints never leave the Mac, voice prints live in the system keychain and never in exports, and before recording other people the app asks me to confirm they know and agree.

## The hard part was the voices

Transcription works. What took most of the effort was answering a question that sounds trivial: *how many people are speaking, and who are they?*

After diarization, every session goes through five steps before I see the voices:

<figure class="diagram"><svg viewBox="0 0 680 520" role="img" aria-labelledby="pp-title" xmlns="http://www.w3.org/2000/svg"><title id="pp-title">Voice post-processing: diarized voices go through five steps (echo, merge, split, identify, minor) before review.</title><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,1 L10,5 L0,9 z" fill="currentColor"/></marker></defs><g fill="none" stroke="currentColor" stroke-width="1.2"><rect x="100" y="10" width="480" height="40" rx="2"/><line x1="340" y1="50" x2="340" y2="70" marker-end="url(#a)"/><rect x="20" y="70" width="640" height="56" rx="2"/><line x1="150" y1="70" x2="150" y2="126"/><line x1="340" y1="128" x2="340" y2="148" marker-end="url(#a)"/><rect x="20" y="148" width="640" height="56" rx="2"/><line x1="150" y1="148" x2="150" y2="204"/><line x1="340" y1="206" x2="340" y2="226" marker-end="url(#a)"/><rect x="20" y="226" width="640" height="56" rx="2"/><line x1="150" y1="226" x2="150" y2="282"/><line x1="340" y1="284" x2="340" y2="304" marker-end="url(#a)"/><rect x="20" y="304" width="640" height="56" rx="2"/><line x1="150" y1="304" x2="150" y2="360"/><line x1="340" y1="362" x2="340" y2="382" marker-end="url(#a)"/><rect x="20" y="382" width="640" height="56" rx="2"/><line x1="150" y1="382" x2="150" y2="438"/><line x1="340" y1="440" x2="340" y2="460" marker-end="url(#a)"/><rect x="100" y="460" width="480" height="40" rx="2" stroke-dasharray="4 3"/></g><g fill="currentColor" font-family="var(--font-type), monospace" font-size="14"><text x="340" y="35" text-anchor="middle">Voices from diarization, mic and computer tracks</text><text x="36" y="103" font-family="var(--font-display), serif" font-size="18">1. Echo</text><text x="166" y="89" font-size="13">A mic voice that overlaps the computer's sound 70 % of the</text><text x="166" y="107" font-size="13">time or more is a probable echo of the call.</text><text x="36" y="181" font-family="var(--font-display), serif" font-size="18">2. Merge</text><text x="166" y="167" font-size="13">Two voices whose fingerprints match at 0.75 or more are the</text><text x="166" y="185" font-size="13">same person.</text><text x="36" y="259" font-family="var(--font-display), serif" font-size="18">3. Split</text><text x="166" y="245" font-size="13">A voice whose passages don't agree with each other may hold</text><text x="166" y="263" font-size="13">two people: its passages are proposed for a split.</text><text x="36" y="337" font-family="var(--font-display), serif" font-size="18">4. Identify</text><text x="166" y="323" font-size="13">Each remaining voice is compared with the voices I've</text><text x="166" y="341" font-size="13">already named, kept in the keychain.</text><text x="36" y="415" font-family="var(--font-display), serif" font-size="18">5. Minor</text><text x="166" y="401" font-size="13">Under 30 seconds and under 1 % of the speech: kept, but out</text><text x="166" y="419" font-size="13">of the way.</text><text x="340" y="485" text-anchor="middle">Named voices, with proposals for me to review</text></g></svg></figure>

**The call leaks into the microphone.** On speakerphone, the other side of the call comes out of the speakers and back into the mic. Diarization then sees extra "people" on the microphone track who are really the remote participants. Echo cancellation helps (on one speakerphone session it cut repeated words from 122 to 68), but it doesn't remove them all. What separates them is simpler: the overlap with the computer's sound. The voices I kept on the mic overlapped it about 6 % of the time; the ones I had removed by hand, 55 % on average, often 85 to 100 %. A mic voice overlapping the system track 70 % or more is now flagged as a probable echo. All nine flagged that way were voices I had already removed by hand. The margin is thin, though: the highest genuine voice was at 67 %.

![A candlestick telephone and a horn loudspeaker: the sound from the horn loops back into the telephone's mouthpiece.](../../assets/illustrations/how-was-your-day/01-call-echo.png)

**One person becomes two, two people become one.** Diarization regularly splits one speaker into several voices, and sometimes merges two. In one 105-minute meeting, a single "voice" from the call held two people, one for 21 minutes and one for 74 seconds. When I asked the app to remember that voice, it learned from its first usable minute, which happened to be the wrong person, and later sessions proposed the wrong name. The fix checks each voice's coherence: the two halves of that one only matched at 0.56, so its passages are now proposed for a split. It reuses the fingerprints computed during diarization, so the check costs nothing instead of four extra minutes.

![Two nearly identical tuning forks on their resonance boxes, their sound waves overlapping.](../../assets/illustrations/how-was-your-day/02-tuning-forks.png)

**Calibrate on your own corrections.** I didn't have a labelled dataset. I had something better: months of my own manual fixes. I replayed the rules on 45 sessions and 209 detected voices and compared them with what I had corrected by hand. Merging duplicates holds up well: fourteen voices merged with similarities from 0.76 to 0.99, while the closest pair of genuinely different people sat at 0.63. Twenty-four voices are classed as "minor" (under 30 seconds and under 1 % of the speech) and kept out of the way. Splitting is the least proven rule: two true cases, both from the same meeting, against nine rejected ones, and it only works with guards on passage length and sound level.

## The small things that make it usable

- **Forgotten recordings.** After five minutes with no speech on either track, detected on the Mac, the app asks whether I'm done, and stops on its own two minutes later.
- **A queue for heavy work.** Fixing voices used to be blocked while a transcription ran; now heavy jobs wait their turn and quick ones run at once.
- **Bluetooth headsets** run the microphone and the computer's sound on two clocks that drift apart, about 450 ms over two and a half hours. They're realigned in software.

## Where it stands

The first public version came out on October 25, 2026; a month and eighteen releases later, it's signed, notarized, updates itself, and installs with Homebrew. It's still experimental, Apple Silicon and the latest macOS only, in French and English. An iPhone version is a study for now: iOS can't capture other apps' audio, so it would be a microphone-only companion sharing one history with the Mac.

What I take from building it: **a summary you can't check is a rumour.** Linking every point to its source changed how I read my own notes, and it set the bar for everything else in the app, the voices included. If the app can't tell who said something, the link is only half a proof.

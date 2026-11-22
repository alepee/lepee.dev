---
title: 'Catching a refrigerant leak before the heat pump notices'
description: 'A heat pump rarely breaks, it degrades. How I try to spot a slow refrigerant loss with nothing but temperatures, and why each machine must be compared to itself.'
pubDate: '2026-10-25'
heroImage: '../../assets/illustrations/refrigerant-leak-detection/00-header.png'
subject: 'Home energy'
---

This summer my freezer started running almost all the time. Its power draw when running hadn't changed, the compressor was fine, it just couldn't reach −22 °C anymore. Defrosting it changed nothing: empty and clean, it still ran 82 % of the time. The frost had been a consequence, not the cause. The likely culprit is the one nobody sees: refrigerant slowly escaping.

A freezer is cheap. A heat pump is not, and it fails the same way. It almost never breaks outright. It **degrades**, for months: refrigerant leaking out, a filter clogging, an exchanger scaling, a sensor drifting. By the time the house feels cold or the outdoor unit ices over, the compressor has been working too hard for a long time. Leak checks exist, but they are periodic, done by a technician once a year. I wanted something continuous.

## Working with what the machine tells you

I maintain a [Home Assistant integration for Hitachi heat pumps](https://github.com/alepee/hass-hitachi_yutaki), read through a Modbus gateway. On the refrigerant side it exposes temperatures, the opening of the expansion valves, the compressor frequency and current. **No pressure sensors.** That rules out the textbook diagnosis, which works with pressures, and leaves physics by proxy.

The physics is simple enough. When charge is missing, the evaporator is starved: the gas leaving it gets hotter than it should, and the electronic expansion valve opens wider to compensate. Neither signal alone means much. Together, at the same outdoor temperature, they tell a story. So the detector watches the **joint drift** of two things: a temperature difference on the gas line, and the opening of the outdoor expansion valve.

My first version got the name of the first signal wrong, and that mistake was instructive. I called it superheat. The datasheet says otherwise: the sensor I used sits on the gas line, not on the suction, and in heating mode that difference is a lift of 40 to 60 K, not a superheat of a few degrees. My plausibility cap of 40 K was silently throwing away 85 to 98 % of the readings on some models. The detector wasn't wrong, it was starving. The fix was a better name, "gas-line superheat", and a valid range declared per machine model instead of one constant.

## Every machine is its own reference

Owners who opt in send anonymous telemetry, and that fleet changed the design. Across it, the same signal differs by **up to 26 K between two units of the same model**. Installation, refrigerant line length, emitters, settings: no two machines are alike. A universal threshold is not hard to pick, it's impossible.

![Two compressors of the same kind, each with its own gauge, the needles at clearly different positions.](../../assets/illustrations/refrigerant-leak-detection/01-two-compressors.png)

So the detector compares each machine to itself. It spends about two weeks learning what normal looks like for this installation, then watches the relative drift. It shows one of four states: *learning*, *ok*, *watch*, *alert*, with a button to restart learning after a service visit. The fleet is only used for what it's good at: sanity ranges per model, to reject readings that can't be real.

## Testing it on data, not on hope

Before shipping, I replayed the detector on 45 consecutive days of fleet data, spring, on machines presumed healthy. **Zero false alerts** over 61 to 70 verdicts. The one borderline case, a 5.5 K drift of the gas-line signal, was neutralised by the conjunction: the valve didn't follow, so no alert. *Watch* appeared on 6 to 10 % of machine-days during the seasonal transition, which is why *watch* is informational and never raises an alarm on its own.

Replaying again in October, still no false alerts, but a new warning sign: the gas-line signal drifts by about 0.5 K for every degree of outdoor temperature, so a cold snap could put a series of machines in *watch* this winter. And the telemetry archive started in April: it has never seen a temperature below 0 °C. The detector will only be calibrated for winter once it has lived through one.

## Designed to be doubted

A false alert here has a real cost: a worried owner, a technician called for nothing, sometimes money spent. So the product choices lean on caution:

- **Off by default.** The detector needs both a machine model that exposes the right sensors and the owner's explicit consent. When it's off, nothing runs and nothing is stored.
- **A clue, not a diagnosis.** The wording says it in four languages: double-check before spending anything. It doesn't replace the regulatory leak check.
- **Labelled beta for a year or two**, the time to collect several seasons of data.
- **An alert doesn't expire on its own.** Other detectors forget their verdict after two weeks without valid data, because a heating curve doesn't get tuned in August. A leak doesn't fix itself, so its alert stays until someone acts.

## One detector, then a family

The refrigerant detector turned out to be the first of a family: hydraulics, short cycling, scaling of the hot water exchanger, sensor drift, and a few more, each with its signal, its physics and its coverage across the fleet.

Building them taught me there are two kinds of faults, and they need opposite tools. A **slow drift**, like a leak, needs a learned baseline: compare the machine to its own past. A **stable bad state**, like a heat pump that short-cycles all day, needs the opposite: a baseline would learn the defect as normal and never report it. Those get absolute thresholds per operating regime, calibrated on the real fleet, not copied from a textbook.

And, as with my freezer, the best indicator is often not the obvious one. Not how much energy the machine uses, but how often it manages to stop.

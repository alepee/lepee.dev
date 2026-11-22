---
title: 'Heating a stone house: one heat pump, thirteen valves and a virtual room'
description: 'How I let Home Assistant run my heating: seasons from degree days, setpoints by type of room, probes that correct the valves, and a single number sent to the heat pump.'
pubDate: '2026-10-09'
updatedDate: '2026-11-13'
heroImage: '../../assets/illustrations/heating-control/00-header.png'
subject: 'Home energy'
---

My house is an old stone house from the Gironde, with thick, uninsulated walls. That gives it a huge inertia: depending on the room, it takes 41 to 80 hours to respond. The kids' bedrooms are the exception, under the roof, behind glass wool and light framing: they cool down in a few hours. Heat comes from an air-to-water heat pump feeding radiators, and every radiator now has a Zigbee thermostatic valve, thirteen of them.

Since October, Home Assistant runs all of it. Not by replacing the heat pump's own logic, but by giving each part of the system the one job it does well.

## Who does what

- **The heat pump** makes hot water, following its *water law*: the colder it is outside, the hotter the water. It corrects that water temperature with a room temperature it receives.
- **The valves** dose the heat room by room, against their setpoint.
- **Home Assistant** chooses the season, sets every setpoint, tells each valve the real temperature of its room, and sums up the needs of the whole house in a single number sent to the heat pump.

One rule shaped the design: if Home Assistant stops, the house must keep heating. The heat pump keeps its water law, the valves keep their last setpoint. Home Assistant optimizes; it is never the only thing standing between the family and a cold night.

## Seasons from degree days

The heat pump doesn't need the same behaviour in October and in January, so the house has three seasons: **warm** (heat pump off, valves off), **mid-season** (the heat pump runs at night, on off-peak electricity, and during the day only if the house is really short of heat) and **cold** (it runs continuously).

The season follows [degree days](/blog/degree-days/) averaged over three days, with hysteresis. It moves to a colder season at 3 and 9 degree days per day, back to a warmer one at 6 and 1, and never warmer less than seven days after the last change. Getting colder is checked every hour; getting warmer only at 6 am, and only if the last 24 hours agree, a guard added after a run of mild days switched the heating off at the start of a cold snap.

## Setpoints by type of room

Rather than thirteen schedules, there are six types of room, each with an *occupied* and an *unoccupied* setpoint and its own hours:

| Type | Occupied | Unoccupied | When occupied |
|---|---|---|---|
| Living rooms | 20 °C | 18 °C | 7 am to 10 pm |
| Our bedroom | 19 °C | 17 °C | 10 pm to 7 am |
| Kids' bedrooms | 20 °C | 17 °C | evenings and nights, all day when they're home |
| Guest rooms | 19 °C | 16 °C | when a guest is there |
| Bathroom | 22 °C | 18 °C | 6:30 to 9 am |
| Buffer zones (hall, landing, utility room) | 19 °C, fixed | | |

The kids' rooms know about school days and holidays from a calendar, and a button flips that for the odd day off. Any group can be forced occupied or unoccupied for a while, from the wall tablet or by voice.

Inertia turns the usual logic upside down. With walls that take two to three days to react, lowering the temperature at night saves little, and warming a room just in time is hopeless. So the house **charges at night**: during off-peak hours, every room gets its occupied setpoint, and the stone carries that heat into the day. Heat made at night costs me about 40 % less than heat made during the day.

## Valves lie, so I gave them probes

A thermostatic valve measures the temperature next to the radiator. Last winter, I compared mine to independent room sensors: the living room valve read **3 °C too high** on average, 4.7 °C when the water was above 55 °C. The room was actually at 17.4 °C and more than a degree below its setpoint 72 % of the time; the valve thought so only 10 % of the time.

![A thermostatic radiator valve in section, its motorized head open, linked without wires to a small thermometer on the wall.](../../assets/illustrations/heating-control/01-valve-and-probe.png)

So every room now has its own small temperature probe, and an automation copies its value into the valve as an external temperature, at each reading and every 30 minutes. The details matter:

- these probes only report when the temperature changes, so two or three hours of silence is normal. A first rule that dropped a probe after 90 minutes of silence kept disabling them; it's six hours now;
- one sensor once reported −280 °C. Values outside 0 to 50 °C are ignored, and one valve that doesn't answer no longer stops the loop for the others;
- a firmware update silently resets the valve to its internal sensor; the automation turns the probe back on.

## A virtual room for the heat pump

The heat pump can only listen to one room temperature. I first sent it the coldest room's. Bad idea: the heat pump adds about **2.2 °C of water per degree of lag** it receives, so the worst room kept the water about 2 °C too hot all the time, and 5 to 7 °C too hot whenever one room fell behind. A plain average was no better: warm rooms hid cold ones.

![Three real rooms, each with its radiator and thermometer, feed a fourth room drawn in dashed lines: only that ghost room is connected to the heat pump.](../../assets/illustrations/heating-control/02-virtual-room.png)

What it receives now is a **virtual room** that sums up the house:

- only rooms that matter count: rooms whose type has been occupied for more than three hours, plus the hall and landing;
- if some rooms are below their setpoint, the demand is the average lag of those rooms, capped at 1.5 °C, and multiplied by how widespread it is: one cold room counts for a third, three or more for full weight. A single chronically cold room is a radiator problem to fix locally, not a reason to heat the water for the whole house;
- if every room is served, the demand goes negative, down to −1.5 °C, so that the heat pump actually stops: its controller only cuts the demand when the room it receives is 1.5 °C above setpoint, which two years of history confirmed.

The result is smoothed to 0.2 °C every three minutes and sent as "setpoint 20 °C, room at 20 minus the demand".

## The short-cycling saga

None of that prevented the real problem of the first weeks: **short cycles**. In one week, 608 compressor starts, runs of six minutes, five or six starts an hour, the compressor stuck at its 31 Hz minimum. Nine stops out of ten were the heat pump reaching its water temperature and shutting off.

Three causes added up. Most valves were closed, on rooms already warm, so the heat pump couldn't get rid of even its minimum output. Its water law was the highest of any machine using my integration (50 °C at 7 °C outside), and above 44 to 46 °C my model starts a second compressor stage with an even higher minimum output. And the setpoints I had just raised made the rooms close their valves even more.

The fixes, one at a time so each could be measured:

- **A lower water law**, set on the heat pump's own controller: 30 °C water at 20 °C outside, 70 °C at −10 °C.
- **Valves that never close completely.** Each valve now keeps half its travel open at rest, so the heat pump always has somewhere to put its heat. Finding out how took a dictaphone: I timed the motor noises and discovered that the valves' "adaptive" mode silently ignores that setting. With adaptive mode off, it works.

One night against another, at similar outdoor temperatures: starts fell from **6.9 to 3.9 an hour**, runs grew from **4 to 10.6 minutes**, and the heat produced per hour went from 4.1 to 6.7 kWh. Better, not solved: cycles are still short as long as the water goes above the threshold of the second stage. The next lever is the curve again.

## What I keep from it

- **The house is the system.** Heat pump, water law, valves and rooms interact; tuning one in isolation moved the problem elsewhere every time.
- **Measure what the user feels, not what the device reports.** The valves were sure the living room was warm. A "heat shortfall" metric, the sum of the gaps below setpoint in the rooms that count, is now what decides whether something works.
- **Change one thing at a time.** I disabled a perfectly good automation that lowered the water law, just to keep a single lever and see its effect.
- **Fail safe.** Home Assistant optimizes, the hardware keeps the house warm without it.

Still on the list: a learning loop for the water law, balancing three radiators that fight each other on the ground floor, and using solar surplus instead of night tariffs in mid-season. And a kid's room under the roof that stays behind whatever I do. That one is probably a radiator, not an algorithm.

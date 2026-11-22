---
title: 'Degree days: the number that makes a winter comparable'
description: 'Why I measure my heating in kWh per degree day, how degree days now drive my house, and what a wrong one costs.'
pubDate: '2026-10-20'
heroImage: '../../assets/illustrations/degree-days/00-header.png'
subject: 'Home energy'
---

My heat pump used 6,265 kWh last winter. Is that good? I have no idea, and neither does anyone who compares two winters by their bills. A mild winter makes any house look efficient; a cold one makes any change look useless. Before I could say whether a setting, a valve or a new control loop helped, I needed a way to take the weather out of the numbers.

That way has existed for a century, and every energy engineer knows it: **degree days**. In France they are called *DJU*, *degrés-jours unifiés*.

## What a degree day measures

Pick a base temperature, the outdoor temperature above which a building no longer needs heating. In France the usual base is 18 °C. Every day, count how far and how long the outside stayed below it: a day that averages 8 °C is worth 10 degree days, a day at 20 °C is worth zero. Add the days up and you get a number proportional to how hard the weather pushed against your walls that month or that winter.

The textbook way averages the day's minimum and maximum. I prefer integrating the actual temperature curve, reading by reading: a cold night followed by a sunny afternoon is not the same day as a grey one at the same average. My Home Assistant integration, [Heating & Cooling Degree Days](https://github.com/alepee/hass-heating_cooling_degree_days), does exactly that, and also counts cooling degree days for summer.

## Use one: compare what can be compared

Divide energy by degree days and the weather falls out. My house used about **5.2 kWh of heat pump electricity per degree day** last winter (base 18 °C). That number, not the 6,265 kWh, is the one I can compare from one winter to the next, and the one that tells me whether a change worked.

![A gas meter and a thermometer weighed against each other on a balance.](../../assets/illustrations/degree-days/01-meter-and-thermometer.png)

It also changes the conversations I have with myself. Comparing two seasons, heating consumption dropped by 13 % while degree days dropped by 7 %: the honest gain is about 6 % per degree day, not 13 %. Half of the "improvement" was just a milder winter.

Plotting consumption against degree days, day by day, gives one more thing for free: where the line crosses zero. For my house, heating demand vanishes around **16.7 °C** outside, a bit below the 18 °C convention. That's the house's real balance point, with its insulation, its sun and the heat of the people and appliances inside.

## Use two: let the weather drive the house

Once degree days are measured well, they make a good control signal. My heating has three seasons: warm, mid-season and cold. Each one changes the heat pump's behaviour and the room setpoints. Rather than switching by hand, or by calendar, the season follows degree days averaged over three days, with thresholds and hysteresis: it gets colder quickly, and it waits a week of mild days before getting warmer again. Simulated on last winter, that's about fourteen changes a year, not fourteen a week.

The first real autumn found a flaw within days. After a run of mild days, the three-day average slipped under the threshold one morning and switched the house to the warm season, while the previous 24 hours had been cold enough to need heating. Valves closed, the heat pump stopped, a bedroom dropped to 18 °C. The fix is asymmetric, like the risk: moving to a colder season is evaluated every hour, moving to a warmer one only happens at 6 am, and only if the last 24 hours agree.

## Garbage in, garbage out

A degree day is only as good as the temperature behind it, and that part is easy to get wrong.

My first source was a single outdoor sensor that had quietly gone unavailable, so the integration happily published zeros. I now use the median of five outdoor probes, so one sensor in the sun or a dead battery can't move the number. Going back through history, I also found a cold day in January recorded at 4.9 degree days, when rebuilding it from raw readings gave about 21. A control loop fed with that number would have decided it was spring.

![A louvred weather screen sheltering several thermometers, next to a single thermometer left in the sun on a post.](../../assets/illustrations/degree-days/02-weather-screen.png)

And then there were bugs in my own code. An audit of the integration this autumn found that the tests were green and the numbers were wrong: readings closer than a minute apart were ignored, a temperature that didn't change counted as zero, units weren't converted, missing data was published as a normal day, and degrees were over-counted when the temperature crossed the base. Version 1.2.0 fixed all of it: the last known value is held between readings, missed days are recalculated, and every day carries a coverage figure, so a day built from half the data says so.

## Why it matters

Degree days are a humble number, and they changed how I think about my house. They turn a bill into a measurement, a winter into an experiment, and the weather into an input instead of an excuse. They are also a reminder I keep relearning, at home as at work: before you automate on a number, make sure the number is true.

---
tags: [robotics, autonomy]
---

# Automation vs Autonomy

**Repeat a fixed plan flawlessly** vs **generate a new plan when the world surprises you**. Builds on [Introduction to Robotics & Autonomy](introduction.md), motivates [The Autonomy Stack](autonomy-stack.md).

## Common root: the intelligent agent

**Intelligent agent**: perceives environment, takes actions that maximize chance of success (Russell & Norvig). A robot = **physically-situated** agent doing Sense → Plan → Act → Learn. Autonomy here = *bounded capability for a specific goal*, not general AI. Inherited from the **mechanical** governor (flyball), not the political sense. **Bounded rationality**: all agents have time/info/compute limits → robot autonomy is always *bounded*.

## Definitions

- **Automation**: physically-situated **tools** doing **repetitive, pre-planned** actions on **well-modeled** tasks under the **closed-world** assumption.
- **Autonomy**: physically-situated **agents** that **adapt to the open world** (env/tasks unknown a priori) by **generating, monitoring, re-planning, and learning**, within bounded rationality.

Hinge = **which world assumption holds.**

## Closed vs open world

| | **Closed** (automation) | **Open** (autonomy) |
|---|---|---|
| Knowledge | all known a priori | models partial, unpredictably wrong |
| Modeling | fully modelable | not fully modelable |
| Control | stable loops for all expected cases | sense + dynamically adapt |
| Sensing | can minimize/eliminate | rich sensing **mandatory** |

**Frame problem**: can't enumerate everything relevant (and unchanged) when acting. Automation **dodges** it by engineering the world; autonomy must **confront** it by sensing + re-deciding.

## Industrial robots = pure automation

- Focus: control + joint motion for **fastest, most repeatable** trajectory.
- Everything **fixtured** (lighting, part pose, sequence).
- Often **cheaper to engineer the world than the robot** (shake & sort parts).
- Trend: add sensors → less fixturing → nudge toward autonomy.

See [Mechanical Configuration & Actuation](../hardware/mechanical-configuration.md), [Forward & Inverse Kinematics](../kinematics/forward-inverse-kinematics.md), [Control Systems & PID](../autonomy/control-pid.md), [Robot Programming & Manipulators](../hardware/robot-programming.md).

## The 4-axis contrast

| Axis | **AUTOMATION** | **AUTONOMY** |
|------|----------------|--------------|
| **Plans** | execution (plan once, repeat) | generation (constant re-planning) |
| **Actions** | deterministic | non-deterministic |
| **Models** | closed world | open world |
| **Knowledge** | signals | symbols |

Automation = bottom-left (fixed plans, deterministic, complete models, signals); autonomy = top-right. Real systems sit **in between**.

## Why it matters

**1. Programming style** — automation: formal stable control loops for few repetitive tasks; autonomy: AI (perception/decision/learning) for varied dynamic tasks.

**2. Hardware** — autonomy needs rich sensing. An automation/teleop robot is **not** made autonomous by "just adding software" — sensors may not be there. Match the **ecological niche**: tasks × environment × platform.

**3. Failure modes** (gotchas):
- **Tunnel vision** — wrong models → robot misses things, blindly follows stale rules.
- **Slow human recovery** — operator can't fix fast enough without transparency + smooth handover (autopilot failures).
- **Substitution myth** — automation reshapes the human's job, doesn't remove it; can *add* coordination burden.

→ [System Integration & Robustness](../autonomy/integration-robustness.md) exists to catch these.

## Deciding (heuristic)

Interrogate the 4 axes: one plan forever vs re-plan; deterministic vs adaptive; complete vs partial model; signals vs symbols. **The more you can engineer the world predictable, the more automation suffices** (cheaper/faster/reliable). More autonomy is **not automatically better** — only worth its cost when the world is genuinely open.

## Related

- [Introduction to Robotics & Autonomy](introduction.md)
- [The Autonomy Stack](autonomy-stack.md)
- [Mission Logic & FSM](../autonomy/mission-fsm.md)
- [Planning & Navigation](../autonomy/planning.md)
- [Sensors & State Estimation](../autonomy/state-estimation.md)
- [Perception](../autonomy/perception.md)
- [System Integration & Robustness](../autonomy/integration-robustness.md)
- [Robot Programming & Manipulators](../hardware/robot-programming.md)

## Handbook references
Conceptual framing — not a core focus of the MIT texts. Closest context:
- *Underactuated Robotics* — [Fully-actuated vs Underactuated Systems](https://underactuated.csail.mit.edu/intro.html)
- *Robotic Manipulation* — [Introduction](https://manipulation.csail.mit.edu/intro.html)

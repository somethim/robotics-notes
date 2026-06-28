---
tags: [robotics, autonomy]
---

# Automation vs Autonomy

A robot that **repeats a fixed plan flawlessly** and a robot that **figures out a new plan when the
world surprises it** are doing fundamentally different things — even if both look "automatic". This note
draws the line between **automation** and **autonomy**, the concepts behind it (closed vs open world,
the frame problem, bounded rationality), and why the distinction reshapes how you program, what hardware
you buy, and how the system fails. It builds on [Introduction to Robotics & Autonomy](introduction.md) and motivates
the whole [The Autonomy Stack](autonomy-stack.md).

## The intelligent agent (the common root)

Both ideas descend from one definition:

> An **intelligent agent** is a system that **perceives its environment and takes actions which
> maximize its chances of success.** *(Russell & Norvig, 2003)*

In AI a robot is simply a **physically situated intelligent agent**. Such an agent is typically expected
to **Sense → Plan → Act → Learn**. Crucially, an agent is "intelligent" and "self-governing" **even if
it is heavily bounded** — autonomy here means *autonomous capability for a specific goal*, not
general-purpose AI and not "the robot can do the whole job alone".

## Two traditions of "self-governing"

"Autonomy" (Merriam-Webster) is *the quality or state of being self-governing*. But robotics inherits
the word from the **mechanical** tradition of self-governing devices (the flyball/centrifugal
**governor** on a steam engine), not the political/moral sense. And **bounded rationality** reminds us
that *all* cognitive agents — silicon or biological — have limits on time, information, and computation.
So robot autonomy is always **bounded** autonomy: maximizing success for a mission within real
constraints.

## Definitions

> **Automation** is about **physically-situated tools** performing **highly repetitive, pre-planned
> actions** for **well-modeled tasks** under the **closed world assumption**.

> **Autonomy** is about **physically-situated agents** that not only perform actions but can also
> **adapt to the open world** — where the environment and tasks are **not known a priori** — by
> **generating new plans, monitoring and changing plans, and learning**, within the limits of their
> **bounded rationality**.

The hinge between them is **which world assumption holds**.

## Closed world vs. open world

| | **Closed world** (automation) | **Open world** (autonomy) |
|---|------------------------------|---------------------------|
| Knowledge | Everything relevant is **known a priori** — no surprises | Models are available but only **partially and unpredictably correct** |
| Modeling | The world **can be completely modeled** | The world **cannot** be fully modeled |
| Consequence for control | If modeled accurately, build **stable control loops** for all expected situations | Must **sense relevant aspects** of the world to **dynamically adapt** actions |
| Consequence for sensing | If the world is **controlled**, you can **minimize or eliminate sensing** | **Rich sensing is mandatory** — you act *as an agent* |

**The frame problem** is the deep reason the open world is hard: it is impossible to enumerate and
encode *everything* that might be relevant (and everything that stays unchanged) when an action is taken.
Closed-world automation **dodges** the frame problem by *engineering the world* so the unmodeled simply
cannot happen; open-world autonomy must **confront** it by sensing and re-deciding continuously.

## Industrial robots and fixturing — automation in its purest form

Classic industrial robots epitomise closed-world automation:

- Focus is on **control theory and joint movement** to get the **fastest, most repeatable trajectory**.
- They achieve **high repetition** in a world where **everything is fixtured** to be in the right place
  at the right time — fixed lighting, fixed part positions, fixed sequence.
- Often it is **cheaper to engineer the world than the robot**: just **shake the parts and sort them**
  into a standard pose for a standard manipulator, rather than add perception.
- The modern trend is to **add sensors to reduce the need for fixturing** — i.e. nudging these systems
  a step toward autonomy precisely because rich sensing buys flexibility.

This is the mechanical/control-heavy world of [Mechanical Configuration & Actuation](../hardware/mechanical-configuration.md),
[Forward & Inverse Kinematics](../kinematics/forward-inverse-kinematics.md), [Control Systems & PID](../autonomy/control-pid.md), and [Robot Programming & Manipulators](../hardware/robot-programming.md).

## The 4-axis contrast

The cleanest way to classify a problem is along **four axes**:

| Axis | **AUTOMATION** | **AUTONOMY** |
|------|----------------|--------------|
| **Plans** | **Execution** — plan once, then repeat that plan forever | **Generation** — constantly generating new plans |
| **Actions** | **Deterministic** — the system can be modeled deterministically | **Non-deterministic** — too complex to model deterministically |
| **Models** | **Closed world** — the model contains everything | **Open world** — models will only ever be partial |
| **Knowledge representation** | **Signals** — control/decisions at the signal level | **Symbols** — control/decisions with symbols or labels |

Reading the table: automation lives in the bottom-left world of *fixed plans, deterministic dynamics,
complete models, raw signals*; autonomy lives in the top-right world of *generated plans,
non-determinism, partial models, symbolic reasoning*. Most real systems sit **somewhere in between** and
borrow from both.

## Why the difference matters

Three concrete reasons (with the caveat: *not always* — many systems blend both):

**1. It affects programming style.**

| | Closed world (automation) | Open world (autonomy) |
|---|---------------------------|-----------------------|
| Delegating for | a **small set of repetitious tasks** | a **variety of tasks** in **dynamic environments** |
| Focus is on | **formal, stable control loops** | **artificial intelligence** (perception, decision, learning) |

**2. It affects hardware design.** Autonomy **requires rich sensing** to monitor the key elements of a
dynamic world. So a robot built for **automation or teleoperation is not automatically usable
autonomously by "just adding software"** — the sensors may simply not be there. Think of the robot as
fitting an **ecological niche**: the **tasks** it must do to "survive", the **environment** it lives in,
and the **platform** must all match. This is why autonomy pulls hard on
[Sensors & State Estimation](../autonomy/state-estimation.md) and [Perception](../autonomy/perception.md).

**3. It affects how systems break.**

- **Tunnel vision** — if the models are wrong in a complex world, the robot can **miss things** and
  blindly follow rules that no longer fit reality (e.g. following rules of engagement that overruled what
  was actually happening).
- **Slow human recovery** — when the robot has a problem, a human may not be able to fix it fast enough
  **unless the robot provides transparency and a smooth transfer** of control (e.g. autopilot failures).
- **The Substitution Myth** — the false belief that *a machine perfectly substitutes for a person*.
  Automation reshapes the human's job rather than removing it; *"two heads are nine times better than
  one"* for systems designed for a single operator. Adding automation can **add** coordination burden.

These failure modes are exactly what [System Integration & Robustness](../autonomy/integration-robustness.md) exists to catch.

## How to decide: automation or autonomy?

You will usually use **a bit of both**. To choose, interrogate the application along the four axes:

1. **Is planning involved?** One fixed plan forever → automation. Constantly re-planning → autonomy.
2. **What kinds of actions?** Deterministic and repeatable → automation. Non-deterministic, must adapt →
   autonomy.
3. **What kind of world model?** Complete and controllable → closed world → automation. Partial and
   surprising → open world → autonomy.
4. **What knowledge representation?** Signal-level control → automation. Symbolic reasoning over
   labels/objects → autonomy.

**Heuristic:** the more you can **engineer the world to be predictable** (fixturing, fixed lighting,
fixed sequence), the more **automation** suffices — and the cheaper, faster, and more reliable it is.
The more the world is **open and unmodelable**, the more **autonomy** (and its rich sensing, estimation,
perception, and decision-making) you genuinely need. **More autonomy is not automatically better** — it
is only worth its cost when the world demands it.

## Related

- [Introduction to Robotics & Autonomy](introduction.md)
- [The Autonomy Stack](autonomy-stack.md)
- [Mission Logic & FSM](../autonomy/mission-fsm.md)
- [Planning & Navigation](../autonomy/planning.md)
- [Sensors & State Estimation](../autonomy/state-estimation.md)
- [Perception](../autonomy/perception.md)
- [System Integration & Robustness](../autonomy/integration-robustness.md)
- [Robot Programming & Manipulators](../hardware/robot-programming.md)

---
tags: [robotics, introduction]
---

# Introduction to Robotics & Autonomy

This note frames the whole subject: **what a robot is**, why the field is inherently
**inter-disciplinary**, how robots differ from disembodied AI, and the **Sense–Think–Act** loop that
every later note expands on. It is the on-ramp to [The Autonomy Stack](autonomy-stack.md) and to the
[Automation vs Autonomy](automation-vs-autonomy.md) distinction that decides how much intelligence a given application actually
needs.

## What is a robot?

A working definition used in this course:

> **A robot is an embodied agent that can be programmed to perform physical tasks.**

There is **no universally accepted definition** — asking "what is a robot?" is famously *a good way to
start a fight at a robotics conference*. Several reasonable definitions coexist, each emphasising a
different aspect:

| Source | Definition | Emphasis |
|--------|-----------|----------|
| Dictionary / Wikipedia | A machine — especially one programmable by a computer — capable of carrying out a complex series of actions automatically | **programmability + automation** |
| Robotics Industries Association | A reprogrammable, multifunctional **manipulator** designed to move material, parts, tools or devices through variable programmed motions | **industrial manipulator** view |
| IEEE | An **autonomous** machine capable of **sensing** its environment, **computing** to make decisions, and **performing actions** in the real world | **autonomy + Sense–Think–Act** |

The lack of a crisp definition hints at **deep philosophical questions** (what is intelligence? free
will?) and also reflects the **youth of the field** — robotics only became its own academic discipline
in the 1960s.

**Why it matters:** because there is no single definition, it is more useful to measure a system's
**degree of "roboticity"** than to argue a binary yes/no.

## Degrees of roboticity

Rather than "is it a robot?", grade a system along several axes — none of which yet has a formal metric:

| Axis | Question it answers | Low end → High end |
|------|--------------------|--------------------|
| **Embodiment** | Does it have a physical body that acts on the world? | pure software → physical machine |
| **Autonomy** | How much does it decide for itself vs. being told? | teleoperated → self-governing |
| **Complexity** | How rich are its behaviours and internal models? | single reflex → multi-stage missions |
| **Programmability** | How freely can its behaviour be reprogrammed? | fixed-function → general re-tasking |

A thermostat scores high on autonomy-for-its-task but near-zero on complexity; a chess engine is complex
but **not embodied**; a modern drone scores meaningfully on **all four**.

## Robotics vs. Artificial Intelligence — embodiment is the dividing line

Most roboticists agree on one clean distinction:

- **A robot needs to be embodied** — it has a physical body, lives in the real world, and its actions
  have real, irreversible physical consequences.
- **AI need not be embodied** — an algorithm that plays Go, translates text, or recognises faces is
  intelligent without ever touching the world.

**Why embodiment changes everything:** an embodied agent must contend with **noisy sensors, imperfect
actuators, real-time deadlines, energy limits, and a world that does not pause** while it thinks. This
is exactly why robotics is harder than "AI plus a body" — see [Automation vs Autonomy](automation-vs-autonomy.md) and
[System Integration & Robustness](../autonomy/integration-robustness.md).

## Robotics as an inter-disciplinary field

Robotics **integrates science and engineering** and overlaps heavily with many disciplines. It is not a
single technique but a **synthesis**:

- **Artificial Intelligence** — decision-making, reasoning, learning
- **Computer Vision** — interpreting images and 3-D scenes ([Perception](../autonomy/perception.md))
- **Machine Learning** — learning behaviours and models from data
- **Control Theory** — closing the loop on continuous dynamics ([Control Systems & PID](../autonomy/control-pid.md))
- **Electronics & Mechanical Engineering** — actuators, sensors, structure ([Mechanical Configuration & Actuation](../hardware/mechanical-configuration.md))
- **Systems Engineering** — making many imperfect parts work together reliably ([System Integration & Robustness](../autonomy/integration-robustness.md))

It also connects to optimization, information theory, theoretical computer science, applied math, and
neuroscience — and offers a lens on the *big* questions (what is intelligence? consciousness?). The
emphasis of this course is **pragmatic**: implementing practical algorithms for **mobile robotics** that
are proven to work in real applications.

## Anatomy of a robotic system — and the Sense–Think–Act paradigm

Every robot, however simple or complex, reduces to **three functional parts**:

| Component | Role | Examples |
|-----------|------|----------|
| **Sensors** | acquire information about self and world | IMU, optical-flow camera, GPS, LiDAR ([Sensors & State Estimation](../autonomy/state-estimation.md)) |
| **Computation** | turn sensor data into decisions and commands | onboard computer, estimator, planner, controller |
| **Actuators** | act physically on the world | motors, rotors, wheels, grippers |

These map onto the **Sense–Think–Act** loop — the heartbeat of every robot:

```mermaid
flowchart LR
    W([World]) -->|physical phenomena| S[SENSE<br/>sensors gather data]
    S -->|raw measurements| T[THINK<br/>estimate, perceive, plan, decide]
    T -->|commands| A[ACT<br/>actuators move the robot]
    A -->|changes the world| W
```

**The loop never opens:** the robot acts, the world changes, the sensors measure the change, computation
reacts, and the cycle repeats. The full engineering elaboration of this loop — estimation, perception,
planning, control, mission logic, and the supervision that holds them together — is the subject of
[The Autonomy Stack](autonomy-stack.md).

## A little history (for curiosity)

The *idea* of artificial servants is ancient; the **engineering** is recent.

| Era | Milestone | Significance |
|-----|-----------|--------------|
| ~1000 BC | **Talos** (Greek myth) | mythological bronze automaton |
| ~300 BC – 100 AD | **Early automata** | first mechanical self-moving devices |
| ~1500s | **Leonardo da Vinci** | mechanical knight and automata sketches |
| ~1600s | **Descartes** | proposed **animals as automata** — a mechanistic view of life |
| ~1700s | **More complex automata** | clockwork figures that write, draw, play music |
| ~1800s | **Charles Babbage** | programmable computation (the "Think" part) |
| **1920** | **Karel Čapek — *R.U.R.*** | coins the **word "robot"** (Czech *robota* = "labor"/"work") |
| ~1950s | **Unimate** (Devol & Engelberger) | first industrial robot — robotics enters the real economy |
| 1960s → today | **Academic discipline** | huge progress in theory, algorithms, hardware — *but still a long way to go* |

The key cultural note: the word "robot" was born in **fiction** (Rossum's Universal Robots) and literally
means **labor** — robots were imagined as workers first, intelligences second. That tension between
"repeat the labor" and "decide for yourself" is exactly the [Automation vs Autonomy](automation-vs-autonomy.md) split.

## State of the art

Two landmark systems show how far autonomy has come:

- **Mars Rovers** — *Spirit* and *Opportunity* (landed late 2004; Spirit silent 2010, Opportunity 2018),
  and the still-active *Curiosity* (2012), *Perseverance* (2021), and *Zhurong* (2021). They are ~1.6 m,
  ~180 kg, carry **9 cameras** (Hazcams, Navcams, Pancams, microscopic), and combine **remote human
  planning with local autonomy** — autonomy that *increased* as missions matured, because the light-speed
  delay to Mars makes real-time teleoperation impossible. A textbook case of bounded, mission-specific
  autonomy ([Automation vs Autonomy](automation-vs-autonomy.md)).
- **DARPA Grand Challenge 2005 — "Stanley"** (Stanford). Completed a **175-mile desert course fully
  autonomously in 6 h 54 min**, guided down a rough GPS "corridor", doing **road-following and obstacle
  avoidance** with laser range-finders and vision. The proof-of-concept that launched modern self-driving.

## Why robotics is hard — and why it matters

**Why it is hard:** the real world is **open, noisy, and unforgiving**. Sensors lie, actuators slip,
models are approximate, computation is bounded, and there is no "undo". Stitching imperfect modules into
a system that stays safe under all of this is the central engineering challenge ([System Integration & Robustness](../autonomy/integration-robustness.md)).

**Why it matters:**

- **Massive economic and social consequences**, with strong interest from industry and government.
- **Fascinating technical challenges** with **beautiful connections** to AI, ML, control, vision,
  optimization, information theory, and applied math.
- **A lens on the big questions** — intelligence, what makes us human, consciousness, free will.

## Two ways to organize robotics

| Organising principle | Example categories | Trade-off |
|----------------------|--------------------|-----------|
| **By application** (nature of the work) | aerial / UAS, medical, humanoid, industrial | intuitive, but hides shared structure |
| **By core concepts / techniques** | estimation, control, planning, perception | reveals that **many domains share the same challenges** |

This vault follows the **concept-first** organisation: master the core ideas once (see
[The Autonomy Stack](autonomy-stack.md)) and apply them across every application domain.

## Example course-project themes

Concrete missions where these concepts come together:

- **Autonomous drone delivery** — plan, fly, and deliver a package without human control.
- **Indoor mobile-robot navigation** — operate where GPS is unavailable.
- **Autonomous exploration / coverage** — map or sweep an unknown environment.
- **Precision landing** — bring a drone down accurately on a target.

Each of these is a slice through the same stack: sensing → estimation → perception → planning →
trajectory → control → mission logic, all supervised for robustness.

## Related

- [Automation vs Autonomy](automation-vs-autonomy.md)
- [The Autonomy Stack](autonomy-stack.md)
- [Sensors & State Estimation](../autonomy/state-estimation.md)
- [Perception](../autonomy/perception.md)
- [Control Systems & PID](../autonomy/control-pid.md)
- [Planning & Navigation](../autonomy/planning.md)
- [Mission Logic & FSM](../autonomy/mission-fsm.md)
- [System Integration & Robustness](../autonomy/integration-robustness.md)

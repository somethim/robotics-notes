---
tags: [robotics, architecture]
---

# The Autonomy Stack

**Hub note**: every vault topic as one closed-loop block diagram. [Introduction to Robotics & Autonomy](introduction.md) gives Sense–Think–Act; [Automation vs Autonomy](automation-vs-autonomy.md) gives *why*; this shows *how blocks connect* and how a fault propagates.

## Master block diagram

```mermaid
flowchart TD
    GOAL([Mission Goal]) --> FSM[Mission Logic / FSM]
    FSM --> PLAN[Planning / Navigation]
    PLAN --> TRAJ[Trajectory Generation]
    TRAJ --> CTRL[Control - PID]
    CTRL -->|thrust / torque| ROBOT[Robot / Quadcopter]
    ROBOT --> SENS[Sensors: IMU, GPS, camera, altimeter]
    SENS --> EST[State Estimation - EKF]
    SENS --> PERC[Perception]
    EST -->|state estimate x̂ + confidence| CTRL
    EST -->|where am I| PLAN
    PERC -->|obstacles / free space| PLAN
    EST -->|health / confidence| ROB[Integration / Robustness]
    PERC --> ROB
    ROB -->|supervision, fallback, emergency| FSM
```

Each arrow = a dependency + interface. **Down the left** = commands (decide → plan → shape → control → act); **up the right** = knowledge (measure → estimate → interpret → inform). Robustness watches all.

## Acting vs Knowing

| | **Acting** ("what to do + make happen") | **Knowing** ("what's true") |
|---|---|---|
| Blocks | FSM, Planning, Trajectory, Control | Sensors, Estimation, Perception |
| Notes | [Mission Logic & FSM](../autonomy/mission-fsm.md), [Planning & Navigation](../autonomy/planning.md), [Trajectory Generation & Tracking](../autonomy/trajectory.md), [Control Systems & PID](../autonomy/control-pid.md) | [Sensors & State Estimation](../autonomy/state-estimation.md), [Perception](../autonomy/perception.md) |

Inside Knowing: **estimation** = "where am *I*?" (self pose/velocity); **perception** = "what's *around* me?" (obstacles/free space). Both rest on [State-Space Modeling](../autonomy/state-space.md).

## Integration / Robustness = supervisor

[System Integration & Robustness](../autonomy/integration-robustness.md) sits **above** the chain, not in it. Ingests health/confidence; watches **delay, stale data, frame mismatch, saturation, faults**; feeds supervision/fallback/emergency to the FSM. Ensures locally-correct modules → **globally safe** system.

## Closed loop in words

Act (Control→Robot) → world responds → sensors measure → estimation cleans to a state → perception interprets → flows up to planning/FSM → decide next. **Never runs open**; each tick = one trip around the cycle.

## Quadcopter mission (time-ordered)

```mermaid
sequenceDiagram
    participant M as Mission Manager (FSM)
    participant P as Planner
    participant T as Trajectory Gen
    participant C as Controller (PID)
    participant R as Robot
    participant S as Sensors
    participant E as State Estimation (EKF)
    participant V as Perception
    participant H as Health Monitor

    M->>P: goal (Takeoff → Transit)
    P->>T: route from current state to target
    T->>C: smooth, feasible, time-based reference
    C->>R: thrust / torque commands
    R->>S: motion happens in the world
    S->>E: IMU, GPS, camera, altimeter readings
    E->>C: clean state estimate x̂ + confidence
    S->>V: raw data
    V->>P: obstacles, free space, environment model
    H->>M: battery, confidence, faults
    M->>M: continue? replan? return? land?
```

## Cross-topic dependencies (gotchas)

A weak block **silently corrupts** those downstream:

| Weak block | Damages | Why |
|------------|---------|-----|
| **Estimation** | Control + Planning | both consume `x̂`; wrong state → track/plan from wrong place |
| **Perception** | Navigation | missed obstacle routed straight through |
| **Planning** | Trajectory | bad route → dynamically impossible trajectory |
| **Mission logic** | whole mission | bad decisions continue a doomed mission |
| **Integration** | everything | weak supervision makes good modules unsafe |

**Lesson**: a correct-in-isolation module still crashes on stale data, wrong frame, or no fallback. **Correctness must be defined at the integrated-system level, under uncertainty/degradation** — remit of [System Integration & Robustness](../autonomy/integration-robustness.md).

## Where each block lives

- **Decide:** [Mission Logic & FSM](../autonomy/mission-fsm.md)
- **Route:** [Planning & Navigation](../autonomy/planning.md)
- **Shape:** [Trajectory Generation & Tracking](../autonomy/trajectory.md)
- **Act:** [Control Systems & PID](../autonomy/control-pid.md)
- **Estimate:** [Sensors & State Estimation](../autonomy/state-estimation.md)
- **Understand:** [Perception](../autonomy/perception.md)
- **Model:** [State-Space Modeling](../autonomy/state-space.md)
- **Supervise:** [System Integration & Robustness](../autonomy/integration-robustness.md)

## Related

- [Introduction to Robotics & Autonomy](introduction.md)
- [Automation vs Autonomy](automation-vs-autonomy.md)
- [Control Systems & PID](../autonomy/control-pid.md)
- [Sensors & State Estimation](../autonomy/state-estimation.md)
- [Trajectory Generation & Tracking](../autonomy/trajectory.md)
- [Perception](../autonomy/perception.md)
- [Planning & Navigation](../autonomy/planning.md)
- [Mission Logic & FSM](../autonomy/mission-fsm.md)
- [State-Space Modeling](../autonomy/state-space.md)
- [System Integration & Robustness](../autonomy/integration-robustness.md)

## Handbook references
- *Underactuated Robotics* — [Output Feedback (Pixels-to-Torques)](https://underactuated.csail.mit.edu/output_feedback.html)
- *Robotic Manipulation* — [Introduction](https://manipulation.csail.mit.edu/intro.html)

---
tags: [robotics, trajectory]
---

# Trajectory Generation & Tracking

## Core distinctions

| Term | Meaning |
|------|---------|
| **Setpoint** | one desired value ("go to z = 10") |
| **Path** | route **geometry** — *where*, no timing |
| **Trajectory** | path **+ timing** — *where AND when* |
| **Tracking** | following a time-indexed trajectory |
| **Following** | staying on a path, timing can flex |

Key split: **path = pure geometry**, **trajectory = geometry bound to time** (position + derivatives at every instant).

## Why needed — dynamic feasibility

A robot can't jump instantly between waypoints; motion must respect **velocity, acceleration, actuator limits**. A geometrically valid route can be impossible: a **sharp corner** demands infinite acceleration. Smooth trajectories generate commands inside actuator limits → flyable.

## Quintic (5th-order) polynomial per axis

    p(t) = c₅·t⁵ + c₄·t⁴ + c₃·t³ + c₂·t² + c₁·t + c₀

- **6 coefficients** ↔ **6 boundary conditions**: position, velocity, acceleration at `t=0` and `t=T`.
- Solve `A·c = b` once per axis (vel/accel rows = 1st/2nd derivatives at endpoints).
- Vel & accel pinned to **zero at both ends** → smooth start/stop, feasible by construction.
- **Larger `T`** stretches motion → gentler accelerations.

## Higher-order / minimum-snap

- Match **jerk** too → 8 conditions → **degree-7** polynomial.
- **Minimizing snap** (4th derivative of position) gives smoothest quad trajectories: **snap couples directly into required torques** → gentler demand on the [Control Systems & PID](control-pid.md) inner loop.
- **Quintic** matches up to acceleration — fine for point-to-point.
- **Degree-7 / min-snap** also matches jerk — preferred for aggressive, multi-segment flight.

## Differential flatness

Quadrotor is **flat** in `[x, y, z, ψ]`: choose smooth curves for these four flat outputs and **all** other states + motor inputs follow algebraically from their derivatives. So you shape four output curves instead of solving full nonlinear dynamics — and inputs depend on high derivatives, which is why snap matters.

## Feasibility constraints

- max velocity
- max acceleration
- jerk / snap smoothness
- thrust / tilt limits
- controller bandwidth

A geometrically valid path can still be dynamically impossible — feasibility is about **timing and dynamics**, not shape.

## Planning vs generation vs control

- **[Planning & Navigation](planning.md)** picks *where* — obstacle-free route/waypoints.
- **Trajectory generation** makes it *flyable* — adds time, respects limits.
- **[Control Systems & PID](control-pid.md)** makes it *happen* — tracks the reference using the estimated state.

## Failure mode

**Over-aggressive (infeasible) trajectory** → drives controller into **saturation** → can't track → error blows up despite a geometrically fine path. Fix upstream: respect feasibility, or slow down (increase `T`). [System Integration & Robustness](integration-robustness.md) monitors saturation and switches to safe-hover when tracking error grows.

## Related

- [Control Systems & PID](control-pid.md) — tracks the generated trajectory; saturates on infeasible references.
- [Planning & Navigation](planning.md) — supplies the geometric route that trajectory generation times.
- [Sensors & State Estimation](state-estimation.md) — provides the state the tracking controller compares against.
- [State-Space Modeling](state-space.md) — the dynamic limits and flatness come from the system model.
- [System Integration & Robustness](integration-robustness.md) — feasibility checking and saturation monitoring.
- [The Autonomy Stack](../foundations/autonomy-stack.md) — where trajectory generation sits among the acting blocks.

## Handbook references
- *Underactuated Robotics* — [Trajectory Optimization](https://underactuated.csail.mit.edu/trajopt.html)
- *Robotic Manipulation* — [Motion Planning](https://manipulation.csail.mit.edu/trajectories.html)

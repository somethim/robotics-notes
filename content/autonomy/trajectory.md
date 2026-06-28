---
tags: [robotics, trajectory]
---

# Trajectory Generation & Tracking

## Core distinctions

| Term | Meaning |
|------|---------|
| **Setpoint** | one desired value ("go to z = 10") |
| **Path** | the **geometry** of the route — *where*, no timing |
| **Trajectory** | path **+ timing** — *where AND when* |
| **Tracking** | following a trajectory over time |
| **Following** | staying on a path, with possibly flexible timing |

The key split is **path vs trajectory**: a path is pure geometry; a trajectory binds that geometry to **time**, assigning a position (and its derivatives) to every instant. **Tracking** then means a controller chasing that time-indexed reference; **following** is the looser cousin where timing can flex.

## Why it's needed (dynamic feasibility)

A robot **cannot jump instantly** between waypoints. Motion must respect **dynamic feasibility** — limits on **velocity, acceleration, and actuator capability**. A geometrically valid route can still demand impossible motion: a **sharp corner** requires an instantaneous change of direction, i.e. **infinite acceleration**, which no actuator can deliver. Smooth trajectories are easier and safer to **track**, because the commands they generate stay inside what the motors and the airframe can actually produce. Trajectory generation is what turns a raw route into something **flyable**.

## Quintic (5th-order) polynomial per axis

To move smoothly from a start to a goal over time `T`, fit a **5th-order polynomial per axis** so that **position, velocity, AND acceleration** all match the boundary conditions at both ends:

    p(t) = c₅·t⁵ + c₄·t⁴ + c₃·t³ + c₂·t² + c₁·t + c₀

A quintic has **6 coefficients**, matched to **6 boundary conditions**: position, velocity, and acceleration at `t = 0` and the same three at `t = T`. Conceptually, you write those six conditions as a linear system `A·c = b` — where the velocity and acceleration rows are simply the **first and second derivatives** of the polynomial evaluated at the endpoints — and solve once for the six coefficients (independently for x, y, z). Because velocity and acceleration are pinned to **zero at both ends**, the robot **starts and stops smoothly** — dynamically feasible by construction. A **larger `T`** stretches the same motion over more time, so accelerations are gentler.

## Higher-order / minimum-snap

Matching **one more derivative (jerk)** at each end adds two conditions per segment → **8 conditions**, requiring a **degree-7** polynomial (8 coefficients). Minimizing **snap** — the **4th derivative of position** — produces the smoothest quadcopter trajectories, because **snap couples directly into the required torques**: smoother snap means gentler torque demands on the [Control Systems & PID](control-pid.md) inner loop. So:

- **Quintic** matches up to **acceleration** — fine for point-to-point moves.
- **Degree-7 / minimum-snap** also matches **jerk** and is preferred for **aggressive, multi-segment** flight.

## Differential flatness

A quadrotor is **differentially flat** in the outputs `[x, y, z, ψ]`: once you choose smooth curves for those four **flat outputs**, **all** other states and motor inputs follow algebraically from their derivatives. This is what makes trajectory design tractable — instead of solving the full nonlinear dynamics, you just **shape four output curves** and let differentiation recover the rest. It also explains why snap matters: the inputs depend on high derivatives of these outputs.

## Feasibility constraints

A good trajectory must respect:

- **max velocity**
- **max acceleration**
- **jerk / snap smoothness**
- **thrust / tilt limits**
- **controller bandwidth**

*A geometrically valid path can still be dynamically impossible to fly* — feasibility is a property of the **timing and dynamics**, not just the shape.

## Planning vs trajectory generation vs control

A clean division of labor across the [The Autonomy Stack](../foundations/autonomy-stack.md):

- **[Planning & Navigation](planning.md)** picks *where* — the route/waypoints (geometry, obstacle-free).
- **Trajectory generation** makes it *flyable* — adds time, respects the dynamic limits above.
- **[Control Systems & PID](control-pid.md)** makes it *happen* — tracks the time-based reference using the estimated state.

## Failure mode

An **over-aggressive (infeasible) trajectory** — timing too tight for the vel/accel/thrust limits — drives the controller into **saturation**: it commands more than the motors can deliver, can no longer track the reference, and tracking error blows up *even though the path was geometrically fine*. The fix is upstream: respect the feasibility constraints when generating the trajectory, or slow it down (increase `T`). [System Integration & Robustness](integration-robustness.md) guards against this by monitoring control-effort saturation and switching to a safe-hover fallback when tracking error grows.

## Related

- [Control Systems & PID](control-pid.md) — tracks the generated trajectory; saturates on infeasible references.
- [Planning & Navigation](planning.md) — supplies the geometric route that trajectory generation times.
- [Sensors & State Estimation](state-estimation.md) — provides the state the tracking controller compares against.
- [State-Space Modeling](state-space.md) — the dynamic limits and flatness come from the system model.
- [System Integration & Robustness](integration-robustness.md) — feasibility checking and saturation monitoring.
- [The Autonomy Stack](../foundations/autonomy-stack.md) — where trajectory generation sits among the acting blocks.

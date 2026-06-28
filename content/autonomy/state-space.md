---
tags: [robotics, state-space]
---

# State-Space Modeling

Compact description of **continuous evolution** — the shared substrate under estimation, control, and mission logic. Two equations, **state-transition** + **measurement**:

    xₖ₊₁ = f(xₖ, uₖ, wₖ)        yₖ = h(xₖ, vₖ)

Next state = function of current state, input, disturbance; output = function of state + measurement noise. Same `f`/`h` pair driving the Bayes/Kalman machinery in [Sensors & State Estimation](state-estimation.md).

## Symbol table

| Symbol | Meaning |
|--------|---------|
| `x_k` | **state** (minimal variables to predict the future) |
| `u_k` | control **input** (thrust, torques) |
| `w_k` | process **disturbance** (wind, model error) |
| `y_k` | measured **output** (sensor reports) |
| `v_k` | measurement **noise** |

`w` acts on the *physics*, `v` corrupts the *measurement* — they enter at different points and map to the Kalman **process-noise `Q`** vs **measurement-noise `R`** covariances.

## Typical drone state vectors

Minimal flying state: `x = [x, y, z, vx, vy, vz, ψ]ᵀ` (position, velocity, yaw).

Energy-aware (mission reacts to battery): `x = [x, y, z, vx, vy, vz, ψ, b]ᵀ`.

`b` is what the low-battery FSM in [Mission Logic & FSM](mission-fsm.md) reasons over — simultaneously a **continuous variable** and a **discrete transition trigger**. Lesson: pick the state vector to match the questions the system answers — add a variable only when something downstream needs it.

## Continuous vs discrete — need both

| Layer | Model | Answers |
|-------|-------|---------|
| Continuous | state-space `xₖ₊₁ = f(xₖ, uₖ, wₖ)` | **how** does it move? |
| Discrete | finite state machine | **what** should it do? |

Physics is continuous (estimation/control live here); mission logic is discrete (one mode at a time, modeled by an **FSM**, see [Mission Logic & FSM](mission-fsm.md)). **Real autonomy uses both at once** — FSM selects mode/goal, state-space realizes motion within it.

## Two structural properties

Checked **before** tuning any filter or gains — they decide whether estimation/control are even possible.

- **Observability** — can full state be inferred from outputs? If a variable is unobservable, no estimator recovers it → add a sensor / change the model. Precondition for [Sensors & State Estimation](state-estimation.md).
- **Controllability** — can inputs drive the state anywhere needed? If a direction is uncontrollable, no controller reaches it. Precondition for [Control Systems & PID](control-pid.md).

## Underactuation

Quadcopter: **6 DoF** (3 position + 3 orientation), only **4 inputs** (thrust + roll/pitch/yaw torque) → **underactuated**, can't command lateral motion directly. To translate it must **tilt** so thrust (body z-axis) gains a horizontal component — *attitude control precedes position control*. Why drone control is cascaded (attitude inner, position outer) in [Control Systems & PID](control-pid.md); the input matrix simply has no direct lateral-force entry.

## Related

- [Mission Logic & FSM](mission-fsm.md) — the discrete partner to the continuous state-space model; the both-at-once recipe.
- [Control Systems & PID](control-pid.md) — uses the model to design control; controllability is its precondition.
- [Sensors & State Estimation](state-estimation.md) — estimates `x` from `y` using `f` and `h`; observability is its precondition.
- [Pose & Kinematics](../kinematics/pose-kinematics.md) — what the position/orientation components of the state mean physically.
- [Trajectory Generation & Tracking](trajectory.md) — generates feasible references over this state.

## Handbook references
- *Underactuated Robotics* — [Fully-actuated vs Underactuated Systems](https://underactuated.csail.mit.edu/intro.html) · [Linear Quadratic Regulators](https://underactuated.csail.mit.edu/lqr.html) · [Multi-Body Dynamics](https://underactuated.csail.mit.edu/multibody.html) · [State Estimation](https://underactuated.csail.mit.edu/state_estimation.html)

---
tags: [robotics, state-space]
---

# State-Space Modeling

**Purpose.** Compactly describe **how the robot evolves continuously** — the shared mathematical substrate beneath estimation, control, and mission logic. The model has two equations, a **state-transition** (how the state advances) and a **measurement** equation (how the world is observed):

    xₖ₊₁ = f(xₖ, uₖ, wₖ)        yₖ = h(xₖ, vₖ)

The first says the next state is a function of the current state, the control input, and a random disturbance. The second says the measured output is a function of the state plus measurement noise. This is the same `x = f(x,u,w)`, `z = h(x,v)` pair that drives the Bayes/Kalman machinery in [Sensors & State Estimation](state-estimation.md).

## Symbol table

| Symbol | Meaning |
|--------|---------|
| `x_k` | robot **state** (the minimal variables needed to predict the future) |
| `u_k` | control **input** (thrust, torques, …) |
| `w_k` | process **disturbance** (wind, model error, unmodeled dynamics) |
| `y_k` | measured **output** (what sensors report) |
| `v_k` | measurement **noise** (sensor imperfection) |

The distinction between `w` (acts on the *physics*) and `v` (corrupts the *measurement*) is essential: they enter at different points and are handled by the **process-noise** `Q` and **measurement-noise** `R` covariances respectively in a Kalman filter.

## Typical drone state vectors

A minimal flying state tracks position, velocity, and heading:

    x = [x, y, z, vx, vy, vz, ψ]ᵀ        (position, velocity, yaw)

When **decisions depend on energy** — i.e. when the mission logic must react to battery — extend the state with battery charge `b`:

    x = [x, y, z, vx, vy, vz, ψ, b]ᵀ

This extended vector is exactly what the low-battery FSM in [Mission Logic & FSM](mission-fsm.md) reasons over: `b` is simultaneously a **continuous state variable** and the **trigger** for a discrete mission transition. The lesson is that the state vector is *chosen to match the questions the system must answer* — add a variable only when something downstream needs it.

## Continuous vs discrete — why you need both

The physical system is **continuous**: position and velocity flow smoothly through time, and this is the world that **estimation and control** operate in via the state-space model. The mission logic is **discrete**: the robot is in exactly one mode (Takeoff, Transit, Inspect, …) and jumps between them, modeled by an **FSM** (see [Mission Logic & FSM](mission-fsm.md)).

| Layer | Model | Question it answers |
|-------|-------|---------------------|
| Continuous | state-space `xₖ₊₁ = f(xₖ, uₖ, wₖ)` | **how** does the robot move? |
| Discrete | finite state machine | **what** should the robot be doing? |

State-space says **how** the robot moves; the FSM says **what** it should be doing. **Real autonomy uses both at once** — the FSM selects the goal and mode; the state-space model and its controllers/estimators realize the continuous motion within that mode.

## Two structural properties

These properties decide whether estimation and control are even *possible* on a given model — they are checked before tuning any filter or gains.

- **Observability** — can the **full state be inferred from the available outputs**? If a state variable is unobservable, no estimator (however good) can recover it from the sensors; you must add a sensor or change the model. This is the precondition for [Sensors & State Estimation](state-estimation.md) to work at all.
- **Controllability** — can the **inputs drive the state anywhere it needs to go**? If a direction of the state space is uncontrollable, no controller can steer it there. This is the precondition for [Control Systems & PID](control-pid.md) to achieve its references.

## Underactuation

A quadcopter has **6 degrees of freedom** (3 position + 3 orientation) but only **4 independent inputs** (total thrust + roll/pitch/yaw torque). With fewer inputs than DoF it is **underactuated**: it **cannot command lateral motion directly**. To translate sideways it must first **tilt** so that its thrust vector (which always points along the body z-axis) gains a horizontal component — *attitude control is the prerequisite for position control*. This coupling is why drone control is cascaded (attitude inner loop, position outer loop) in [Control Systems & PID](control-pid.md), and it is a structural fact the state-space model makes explicit: the input matrix simply has no direct lateral-force entry.

## Related

- [Mission Logic & FSM](mission-fsm.md) — the discrete partner to the continuous state-space model; the both-at-once recipe.
- [Control Systems & PID](control-pid.md) — uses the model to design control; controllability is its precondition.
- [Sensors & State Estimation](state-estimation.md) — estimates `x` from `y` using `f` and `h`; observability is its precondition.
- [Pose & Kinematics](../kinematics/pose-kinematics.md) — what the position/orientation components of the state mean physically.
- [Trajectory Generation & Tracking](trajectory.md) — generates feasible references over this state.

---
tags: [robotics, actuation]
---

# Mechanical Configuration & Actuation

**Actuation** = converting supplied energy into joint motion, downstream of kinematics ([Forward & Inverse Kinematics](../kinematics/forward-inverse-kinematics.md)) and control ([Control Systems & PID](../autonomy/control-pid.md)). Two fluid-power families: **hydraulics** (incompressible oil) and **pneumatics** (compressible air).

---

## 1. Hydraulic systems

**Principle.** Oil is **incompressible + dense** → pump pressure transmits near-losslessly to the actuator; small pump commands large, stiff forces. For **heavy-duty** robots needing high force, precision, reliability.

**Power chain (closed, recirculating):** motor → **pump** (mech→hydraulic) → valves → **piston/cylinder** (→ linear motion) → fluid back to reservoir.

| # | Component | Role |
|---|-----------|------|
| 1 | **Reservoir** | Stores fluid; settles air, dissipates heat. |
| 2 | **Filter** | Removes particles; protects pump/valves. |
| 3 | **Pump** | Mech → hydraulic; draws & pressurises fluid. |
| 4 | **Pressure-Release Valve (PRV)** | Safety; on overpressure dumps fluid to reservoir. |
| 5 | **Control valve** | Directs direction/flow; manual, solenoid, or servo — the electrical→motion link. |
| 6 | **Piston** | Hydraulic → linear motion. |
| 7 | **Piston cylinder** | Sealed chamber; lift/push/pull. |
| 8 | **Return pipe** | Spent fluid back to reservoir. |

**Applications.** Pressing/cutting/forming/lifting; cranes, excavators; flight controls, landing gear; braking, power steering; tractors. (High force + precise control.)

**Advantages.** High power density, precise speed/force control, high reliability/durability, continuous stable operation, low transmission loss. **Upkeep:** oil checks, filter changes, PRV inspection.

---

## 2. Pneumatic systems

**Principle.** **Compressed air**: light, compressible, high flow rate → fast, repetitive, light-to-medium force; clean and safe.

**Power chain (open, exhausts to atmosphere — not recirculated):** ambient air → **inlet filter** → **compressor** → **cooler** + **separator** → **receiver** → **valves** → **actuator**. Air continuously replenished.

| # | Component | Role |
|---|-----------|------|
| 1 | **Inlet filter** | Removes dust/contaminants. |
| 2 | **Compressor** | "Heart"; pressurises air. Reciprocating/rotary/centrifugal. |
| 3 | **Cooler** | Lowers temp, condenses moisture. |
| 4 | **Separator** | Removes moisture + oil. |
| 5 | **Receiver** | Stores air; damps pressure fluctuations; peak backup. |
| 6 | **Feedback** | Gauges/flow meters — real-time monitoring. |
| 7 | **Pressure switch** | At threshold, activates/deactivates compressor/valves. |
| 8 | **Secondary air handling** | Dryer / air filter / oil filter. |
| 9 | **Check valve** | Regulates flow; directional / pressure / flow control sub-types. |
| 10 | **Actuator** | Air → motion: cylinders (linear), motors (rotary), grippers, valves. |

**Applications.** Assembly/packaging; welding/painting; nail guns/drills; dental/surgical; landing-gear, doors, brakes.

**Advantages.** Fast response, simple design, cost-effective, safe (non-toxic, non-flammable).

---

## 3. Hydraulics vs Pneumatics

| Criterion | **Hydraulics** | **Pneumatics** | Winner |
|-----------|----------------|----------------|--------|
| **Force** | **7 000–35 000 kN/m²**; very high force/torque. | **500–700 kN/m²**; far lower. | Hydraulics |
| **Cleanliness** | Oil leaks; banned in clean rooms/pharma/food. | Only leaks air; clean. | Pneumatics |
| **Speed** | Viscous, slower; can't vent fast. | High flow → fast, high duty cycle. | Pneumatics |
| **Energy** | Fluid reused; efficient long-run if maintained. | Compressor runs continuously; air not recycled; leaks waste. | Hydraulics (long-run) |
| **Safety** | Fluids flammable/corrosive/toxic/hot. | Air non-toxic/non-explosive; risk = violent burst. | Pneumatics |
| **Complexity** | Pump, reservoir, piping; more engineering. | Simpler, lower pressure, cheaper. | Pneumatics |
| **Maintenance** | Corrosion; replace seals/pipes/valves. | Easier; service the FRL (filter-regulator-lubricator). | Pneumatics |

**Rule of thumb.** Hydraulics → heavy, high-force, continuous, stiffness-critical (presses, excavators, large arms). Pneumatics → fast, light, repetitive, clean, safety-sensitive (grippers, packaging, medical, food).

---

## 4. Where actuation sits

Bottom of the control stack: controller ([Control Systems & PID](../autonomy/control-pid.md)) computes desired torque/force → actuator turns it into motion. **Control valve** = literal electrical-command ↔ fluid-power interface (solenoid/servo metering flow from PID output).

Medium properties feed back into control:

- **Hydraulics (incompressible)** → **stiff**; predictable, easy precise positioning.
- **Pneumatics (compressible)** → **springy**; trapped air = spring, hard mid-stroke positioning, favours **end-stop** point-to-point motion.

Actuator choice sets achievable force/speed/bandwidth → constrains feasible trajectories and kinematic tasks (e.g. SCARA prismatic vertical stroke driven by a cylinder — see [Forward & Inverse Kinematics](../kinematics/forward-inverse-kinematics.md), [Robot Programming & Manipulators](robot-programming.md)).

---

## Related

- [Control Systems & PID](../autonomy/control-pid.md) — the controller whose command the actuator executes; medium stiffness sets achievable bandwidth.
- [Forward & Inverse Kinematics](../kinematics/forward-inverse-kinematics.md) — kinematics says where joints go; actuation moves them there.
- [Robot Programming & Manipulators](robot-programming.md) — gripper open/close and joint strokes are actuated motions invoked from the program.
- [Trajectory Generation & Tracking](../autonomy/trajectory.md) — actuator force/speed limits bound which trajectories are feasible.
- [System Integration & Robustness](../autonomy/integration-robustness.md) — actuator saturation, leaks, and latency as integration-level failure modes.

## Handbook references
- *Robotic Manipulation* — [Let's get you a robot](https://manipulation.csail.mit.edu/robot.html)

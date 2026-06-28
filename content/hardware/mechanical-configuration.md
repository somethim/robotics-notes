---
tags: [robotics, actuation]
---

# Mechanical Configuration & Actuation

Once kinematics tells us *where* a joint must go (see [Forward & Inverse Kinematics](../kinematics/forward-inverse-kinematics.md)) and control tells us *how hard* to push (see [Control Systems & PID](../autonomy/control-pid.md)), something physical has to actually move the link. **Actuation** is that something — the conversion of stored or supplied energy into mechanical motion at the joints. The two great **fluid-power** families used in heavy and industrial robotics are **hydraulics** (incompressible liquid) and **pneumatics** (compressible gas). Each is a complete subsystem with its own source, conditioning, control, and output stages, and the choice between them shapes the robot's force, speed, cleanliness, and safety envelope.

---

## 1. Hydraulic Systems

**Principle.** A hydraulic system uses a **hydraulic fluid (oil)** to **transfer power and control motion** between robot components such as actuators and manipulators. The key physical fact is that the fluid is **largely incompressible** and **dense**: when the pump pressurises it, that pressure is transmitted almost without loss to the actuator, so a small pump can command very large, stiff forces. This makes hydraulics the choice for **heavy-duty industrial robots** where **high forces, precision, and reliability** are required.

**The power chain.** Mechanical energy (usually from an electric motor) → **pump** converts it to hydraulic (pressure) energy → valves route the pressurised fluid → **piston/cylinder** converts it back into linear mechanical motion → fluid returns to the reservoir to be recirculated. It is a **closed, recirculating loop**: the same oil is used over and over.

### Components

| # | Component | Role |
|---|-----------|------|
| 1 | **Reservoir** | Stores the fluid; lets it **settle, release air bubbles, and dissipate heat**; maintains a consistent fluid level. |
| 2 | **Filter** | Removes dirt, debris and particles to keep the fluid **clean**, protecting pump and valves. Sits inside the reservoir or in-line. |
| 3 | **Pump** | Converts **mechanical → hydraulic energy**. Creates a vacuum at the inlet to draw fluid from the reservoir, then pressurises it to drive the system. |
| 4 | **Pressure-Release Valve (PRV)** | **Safety device** set at a predetermined pressure. On **overpressure** it opens and dumps excess fluid back to the reservoir, preventing damage. |
| 5 | **Two-way / Control valve** | Directs the **direction and flow** of fluid to the actuators. Can be **manual, solenoid (induction), or servo-controlled** — the link between an electrical command and physical motion. |
| 6 | **Piston** | Converts hydraulic energy into **linear mechanical motion**: fluid entering one side pushes the piston. |
| 7 | **Piston cylinder** | The sealed chamber housing the piston; the piston's travel inside it produces motion that can **lift, push, or pull**. |
| 8 | **Return pipe** | Carries spent fluid back to the reservoir after it has done its work, completing the recirculation cycle. |

**Applications.** Manufacturing (**pressing, cutting, forming, lifting**); construction (cranes, excavators, bulldozers); aerospace (flight-control surfaces, landing gear); automotive (braking, power steering, shock absorbers); agriculture (tractors, combine harvesters). All are tasks demanding **high force and precise, reliable control**.

**Advantages.** **High power density** (large force/torque in a small package thanks to incompressibility); **precise control** of speed and force; **high reliability and durability** with relatively low maintenance; **continuous, stable operation** that reduces wear; **high efficiency** with minimal transmission loss in continuous duty. Proper upkeep means regular **oil checks, filter changes, and PRV inspections**.

---

## 2. Pneumatic Systems

**Principle.** A pneumatic system uses **compressed air** as the working medium. A compressor squeezes ambient air into a smaller volume; releasing that stored energy through actuators produces motion. Because air is **light, compressible, and has a high flow rate**, pneumatics excels at **fast, repetitive, light-to-medium-force** tasks, and the medium itself is clean and safe.

**The power chain.** Ambient air → **inlet filter** → **compressor** raises pressure → **cooler** + **separator** condition it (remove heat, moisture, oil) → **receiver** stores it → **check / control valves** route it → **actuator** turns air pressure into motion. Unlike hydraulics, the air is **not recirculated** — it is exhausted to atmosphere after use and must be **continuously replenished** by the compressor.

### Components

| # | Component | Role |
|---|-----------|------|
| 1 | **Inlet filter** | Removes dust, dirt and contaminants from incoming air so only clean air enters. |
| 2 | **Compressor** | The "heart" of the system — pressurises ambient air into a smaller volume. Types: **reciprocating, rotary, centrifugal**. |
| 3 | **Cooler** (after/inter-cooler) | Lowers the temperature of compressed air, **condensing moisture** before it reaches downstream parts. |
| 4 | **Separator** | Removes **moisture and oil** from the air, maintaining air quality. |
| 5 | **Receiver (air reservoir)** | Stores compressed air for a **steady supply**, damps **pressure fluctuations**, and provides backup for peak demand. |
| 6 | **Feedback** | Gauges and flow meters give **real-time** pressure and flow information for monitoring. |
| 7 | **Pressure switch** | Monitors pressure; at a threshold it **activates/deactivates** components such as the compressor or valves. |
| 8 | **Secondary air handling** | Extra conditioning: **air dryer** (removes moisture → prevents corrosion), **air filter** (further filtration), **oil filter** (removes oil vapour from lubricated compressors). |
| 9 | **Check valve** | Regulates flow to actuators. Sub-types: **directional control** (sets direction), **pressure control** (regulates pressure), **flow control** (controls flow rate). |
| 10 | **Actuator** | Converts air energy into motion: **pneumatic cylinders** (linear), **pneumatic motors** (rotary), **pneumatic grippers** (grasping), **pneumatic valves** (flow control). |

**Applications.** Manufacturing (assembly lines, material handling, packaging); automotive (welding, painting, part manipulation); construction (hammers, nail guns, drills); medical (dental and surgical equipment); aerospace (landing-gear control, doors, brakes).

**Advantages.** **Fast response** (high air flow → rapid movement, high cycle rates); **simple design** and installation; **cost-effective** vs hydraulic/electrical; **safe** — compressed air is **non-toxic and non-flammable**, suited to sensitive environments.

---

## 3. Hydraulics vs Pneumatics — Comparison

The two are complementary: hydraulics buys **force and stiffness** at the price of weight, mess, and complexity; pneumatics buys **speed, cleanliness, and safety** at the price of force.

| Criterion | **Hydraulics** | **Pneumatics** | Winner |
|-----------|----------------|----------------|--------|
| **Force** | Dense, incompressible fluid → very high pressure (**7 000–35 000 kN/m²**), so large forces and torque. | Low-density, compressible gas → typically only **500–700 kN/m²**; cannot reach hydraulic forces. | **Hydraulics** |
| **Cleanliness** | Susceptible to **leaks** of oil/fluid; often **prohibited** in clean rooms, pharma, food & beverage. | Only leaks **air**; internally cleaned of oil/water/particles; favoured for clean/green environments. | **Pneumatics** |
| **Speed** | Oil's high viscosity and resistance make it **slower**; slower to start; fluid can't be vented quickly, must return to reservoir. | High air flow rate → **rapid energy release**, high-speed motion and high duty cycles. | **Pneumatics** |
| **Energy** | Fluid is **reused** indefinitely; efficient long-term **if** well filtered/maintained — but the pump still wastes energy. | Compressor must run **continuously**; air **can't be recycled** and any leak wastes energy. | **Hydraulics** (long-run) |
| **Safety** | Fluids may be **flammable, corrosive, toxic, hot**; leaks are a hazard; used fluid needs safe disposal. | Air is **non-toxic, non-corrosive, non-explosive**; main risk is a violent burst causing physical injury. | **Pneumatics** |
| **Complexity** | Needs valves, pipes, externally-powered pump and reservoir — more engineering; can be centralised for a plant. | Simpler designs, lower pressures, cheaper materials; no anti-corrosion/anti-flammability precautions needed. | **Pneumatics** |
| **Maintenance** | Main enemy is **corrosion**; needs non-corrosive piping, regular monitoring, replacement of seals/pipes/valves. | Cleaner and easier; routine checks for seals and leaks; key task is servicing the **filter-regulator-lubricator** unit. | **Pneumatics** |

**Rule of thumb.** Reach for **hydraulics** when the job is **heavy, high-force, continuous and stiffness-critical** (presses, excavators, large manipulators). Reach for **pneumatics** when the job is **fast, light, repetitive, clean, or safety-sensitive** (assembly grippers, packaging, medical, food).

---

## 4. Where Actuation Sits in the Robot

Actuation is the **physical muscle** at the bottom of the control stack. The controller (see [Control Systems & PID](../autonomy/control-pid.md)) computes a desired joint torque or force; the actuator — hydraulic cylinder, pneumatic cylinder, or (most commonly in arms) an electric motor — turns that command into motion. The **control valve** is the literal interface between the **electrical command** and the **fluid power**: a solenoid or servo valve receiving a PID output and metering flow accordingly. Crucially, the medium's properties feed back into control design:

- **Incompressible hydraulics** behave **stiffly** — small valve changes produce predictable motion, easing precise position control.
- **Compressible pneumatics** behave **springily** — the trapped air acts like a spring, making precise mid-stroke positioning harder and favouring **end-stop** (point-to-point) motion over smooth servoing.

The actuator choice therefore propagates upward: it sets the achievable **force, speed, and bandwidth**, which constrain the feasible **trajectories** the controller can track and the **kinematic** tasks the arm can perform (the prismatic vertical axis of a SCARA arm, for instance, is exactly the kind of pick/place stroke a pneumatic or hydraulic cylinder drives — see [Forward & Inverse Kinematics](../kinematics/forward-inverse-kinematics.md) and [Robot Programming & Manipulators](robot-programming.md)).

---

## Related

- [Control Systems & PID](../autonomy/control-pid.md) — the controller whose command the actuator executes; medium stiffness sets achievable bandwidth.
- [Forward & Inverse Kinematics](../kinematics/forward-inverse-kinematics.md) — kinematics says where joints go; actuation moves them there.
- [Robot Programming & Manipulators](robot-programming.md) — gripper open/close and joint strokes are actuated motions invoked from the program.
- [Trajectory Generation & Tracking](../autonomy/trajectory.md) — actuator force/speed limits bound which trajectories are feasible.
- [System Integration & Robustness](../autonomy/integration-robustness.md) — actuator saturation, leaks, and latency as integration-level failure modes.

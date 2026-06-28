---
tags: [robotics, programming]
---

# Robot Programming & Manipulators

Industrial manipulators are not commanded with continuous PID loops by the end user — they are **programmed** with a high-level, line-numbered **teach-pendant (TP) language** that sits on top of the controller. The programmer specifies *where* to move, *how* to get there, *how fast*, *how precisely to stop*, and *what logic* to run in between (I/O handshakes, counters, branches). The robot's motion planner and servo loops then realise each instruction. This note covers the TP instruction set conceptually and then walks a complete **SCARA quality-control** application as a worked scenario — without reproducing any program listing.

---

## 1. What a Robot Program Is

A robot program is a sequence of **user-specified commands**, each on its own **numbered line**, that tells the robot how to perform operations plus the "detailed program information" defining the program's attributes. A program weaves together three kinds of instruction:

- **Motion** — how and where the arm moves (the motion format, target position, speed, and positioning path).
- **Logic / control flow** — changing execution order when conditions are met (`IF`, `JMP/LBL`, `CALL/END`, `WAIT`, `FOR`).
- **Data & I/O** — storing numbers in **registers**, positions in **position registers**, and exchanging **digital signals** with peripheral devices.

Every program terminates with an **END** symbol indicating no further instructions. A well-structured application is split into a **main program** plus **subprograms** (called for reusable actions such as opening a gripper).

---

## 2. Motion Instructions

A **motion instruction** moves the arm to a taught point at a given speed along a specified trajectory. It has four parts: a **motion format** (trajectory type), **position data** (the target), a **speed** (rate), and a **positioning path** (how to arrive). An **additional** instruction (e.g. acceleration override) can ride along during the move.

**Motion format** — four trajectory types:

| Format | Letter | Trajectory |
|--------|--------|------------|
| **Joint** | **J** | All axes accelerate, move at a feed rate, decelerate and stop **together**; the tool follows whatever curved path results in joint space. Fastest, used when the exact path doesn't matter. |
| **Linear** | **L** | The tool-centre point follows a **straight line** start→end (also used for pure rotary reorientation). |
| **Circular** | **C** | The end-effector centre follows an arc start→end **through a via point**; via and end are given on **one line**. |
| **Arc** | **A** | Circular-arc motion coding **one position per line** (the controller chains successive A points). |

**Speed** is specified per format: for **joint** moves a **percentage 1–100 %** of max (or a time in sec/msec); for **linear/circular/arc** an absolute speed (e.g. 1–2000 mm/sec, or cm/min, inch/min) or an angular rate (deg/sec) for reorientation, or a time.

---

## 3. Positioning Termination — FINE vs CNT

The **positioning path** decides how the robot **terminates** at a point — and this is one of the most important practical knobs:

- **FINE** — the robot **stops exactly** at the point before moving on. Use it where accuracy matters: the precise pick or drop location.
- **CNT (continuous)** — the robot **approaches but does not stop**, rounding the corner toward the next point to keep motion smooth and fast. A coefficient **0–100** sets how close it gets:
  - **CNT0** — passes **closest** to the point (tightest corner) while still not stopping.
  - **CNT100** — takes the **widest** path, never slowing near the point, immediately heading for the next one.
  - **CNT50** — an intermediate rounding, the typical "smooth transit" choice.

In short, **FINE termination stops exactly at the point; CNTxx approximates it** by the percentage given, trading positional exactness for cycle-time and smoothness.

---

## 4. Speed, Acceleration & Data

- **ACC (acceleration override)** — an *additional* instruction scaling the accel/decel of a move (e.g. ACC50 = half acceleration), gentling the motion for fragile payloads or to reduce wear. Other additional instructions include **Skip** (jump if a condition isn't met before arrival), **Offset**, **Tool_Offset**, **INC** (increment), and **BREAK**.
- **Registers `R[i]`** — numeric variables holding an integer or decimal, used as **counters** and for **arithmetic** (`R[i] = value`, plus `+ − × ÷`). The quality-control counters live here.
- **Position registers `PR[i]`** — variables holding **position data** `(x, y, z, w, p, r)`. They can be assigned, summed, or differenced, and reused throughout the program — far more flexible than hard-coded points because the same taught location can be referenced (and offset) in many places. Element access `PR[i, j]` reaches an individual coordinate.
- **Digital I/O** — **`DI[n]`** (digital input) reads sensor/operator signals; **`DO[n]`** (digital output) drives external devices. These are the program's handshake with the cell (start signals, OK/NOT-OK buttons, "box empty" sensors).

---

## 5. Flow Control & Program Structure

| Instruction | Meaning |
|-------------|---------|
| **END** | Marks program end; if the program was **CALL**ed, returns control to the caller. |
| **LBL[i]** | A **label** — a named return point in the program. |
| **JMP LBL[i]** | **Unconditional jump** to a label. |
| **CALL** | Transfers control to the **first line of a subprogram**; on its END, control returns to the line after the CALL. |
| **WAIT** | **Suspends** execution either for a fixed time (timed wait) or **until a condition** (e.g. a DI signal) is met — optionally with a timeout branch. |
| **IF** | **Conditional branch** — jumps to a label/program when a condition holds (single-line test). |
| **IF_THEN … ELSE … ENDIF** | **Block conditional**: lines under THEN run if the condition holds; lines under ELSE run otherwise; **ENDIF** closes the block. THEN and ELSE branches are mutually exclusive. |
| **FOR … ENDFOR** | **Counted loop**; the pair is matched automatically. |
| **R[i] / PR[i]** | Register / position-register assignment and arithmetic (counters, offsets). |
| **DI[n] / DO[n]** | Read digital input / set digital output. |
| **J / L / C / A** | Motion formats (§2). |
| **FINE / CNTxx** | Positioning termination (§3). |
| **ACCxx** | Acceleration override (§4). |

**Program structure.** A real application is **modular**: a **main** program (e.g. an `A_MAIN` that initialises positions, loops over the work cycle, and handles HMI signals) **CALLs subprograms** for discrete actions — open gripper, close gripper, compute the next stack position. Subprograms keep the main readable and let the same action be reused. Labels and JMPs give the main its cyclic, signal-driven structure; registers carry state (which layer, how many items) between cycles.

---

## 6. Worked Scenario — SCARA / RRTR Quality Control

### The cell and the task

A **4-DOF RRTR SCARA** arm performs **quality control** on a production line. The cell contains a **production line** (where products arrive), an **operator post** (with an OK / NOT-OK panel), and **two boxes**. The cycle: the arm **picks** an arriving product, **presents** it near the operator who visually inspects it and presses **OK** or **NOT-OK**; on **OK** the product goes to **box 1**, on **NOT-OK** to **box 2**; the arm then **returns** to start. The robot **counts** the items placed in each box and **resets** the count at **20** (waiting for an "empty box" signal before continuing).

### Kinematic configuration

**RRTR** = Revolute, Revolute, **Translational (prismatic)**, Revolute. The first two revolute joints sweep the arm in the horizontal plane; the **prismatic** third joint (variable `d`) provides the **vertical** pick/place stroke; the final revolute joint orients the gripper. This is the classic **SCARA** geometry — **rigid vertically, compliant horizontally** — ideal for fast planar pick-and-place. All links have length in *x* and *y* except the last, which has length only in *y*.

**DH parameters** (the per-joint geometry feeding forward kinematics — see [Forward & Inverse Kinematics](../kinematics/forward-inverse-kinematics.md)):

| Joint | Type | θ (z) | d (z) | α (x) | a (x) |
|-------|------|-------|-------|-------|-------|
| 0–1 | R | θ₁ = 0 | 0.3 | 0 | 0.2 |
| 1–2 | R | θ₂ = 0 | 0.1 | 180° | 0.15 |
| 2–3 | **T** (prismatic) | 0 | **Var** | 0 | 0.2 |
| 3–4 | R | θ₃ = 0 | 0.1 | 0 | 0 |

Each row defines a link transform **Aᵢ**; the **forward kinematics** is the product **S = A₁ · A₂ · A₃ · A₄**, mapping joint values to the gripper pose. The prismatic joint's **Var** `d` is exactly the commanded vertical depth for picking and dropping.

### Program logic (conceptual walkthrough)

The application is built from the instruction concepts above; no listing is needed to understand its flow:

1. **Initialise.** Move from **HOME** with a linear move at full speed, terminating **FINE** (stop exactly). Set a **return label** (LBL[1]) and zero the two **counters** `R[1]` (box 1) and `R[2]` (box 2).
2. **Wait for start.** **WAIT** up to 10 s for the production-line signal `DI[1]`. If it doesn't arrive (`DI[1] = OFF`), **JMP** back to LBL[1] and wait again — a timeout guard so the arm never proceeds without a part.
3. **Pick.** **CALL** the open-gripper subprogram, then **J** (joint) move to approach point **L** at half speed with **CNT50** (smoothly rounding the corner, no stop), then **L** (linear) to the exact grasp point **L1** at half speed **FINE** (stop precisely), then **CALL** the close-gripper subprogram to grab the product. Retreat **L** back to **L** with **CNT0**.
4. **Present to operator.** **J** move to the operator position register **PR[OP]** at half speed, **FINE**, with **ACC50** (gentle acceleration so the held part isn't jolted). Set an inspection label (LBL[2]).
5. **Conditional sort** — an **IF_THEN / ELSE / ENDIF** block on the operator's verdict:
   - **IF `DI[OK] = ON`** (operator approved): **J** toward box-1 position register **PR[1]** at full speed **CNT50**, approach the drop point **PR[1.1]** at half speed **FINE**, **CALL** open-gripper to release into box 1, retract via **PR[1]** **CNT50**, then **increment** `R[1] = R[1] + 1`.
   - **ELSE**, nested **IF `DI[NOT_OK] = ON`**: the mirror sequence to **PR[2]** / **PR[2.2]** for box 2, releasing and **incrementing** `R[2] = R[2] + 1`. **ENDIF** closes the block.
6. **Return & gate.** **L** back to **HOME** at full speed **FINE**, then **WAIT** for the next start signal `DI[1]`.
7. **Reset at 20.** An **IF … THEN** test: if `R[1] ≥ 20` (or `R[2] ≥ 20`), **WAIT** for the "box empty" signal `DI[BOSH]`, then **reset** the corresponding counter to 0. **WAIT** for start again, then **END**.

```mermaid
flowchart TD
    HOME[HOME - L FINE] --> INIT["LBL1: R1=0, R2=0"]
    INIT --> W{"WAIT DI1 (10s)"}
    W -- timeout/OFF --> INIT
    W -- ON --> PICK["Open gripper - J CNT50 - L FINE - Close gripper"]
    PICK --> PRES["Present: J PR_OP FINE ACC50 (LBL2)"]
    PRES --> Q{Operator verdict}
    Q -- "DI_OK" --> B1["Box 1: PR1 / PR1.1 - release - R1++"]
    Q -- "DI_NOT_OK" --> B2["Box 2: PR2 / PR2.2 - release - R2++"]
    B1 --> RET[Return HOME - L FINE]
    B2 --> RET
    RET --> CHK{"R1 or R2 >= 20 ?"}
    CHK -- yes --> EMPTY["WAIT DI_BOSH - reset counter = 0"]
    CHK -- no --> WS[WAIT DI1]
    EMPTY --> WS
    WS --> END([END])
```

### The key programming ideas illustrated

- **Labels + JMP** create the **cyclic, signal-gated** structure (return to LBL[1] on timeout; loop the work cycle).
- **WAIT-for-signal** synchronises the robot with the **cell and the human** (start signal, OK/NOT-OK buttons, empty-box sensor) — the arm never moves on stale assumptions.
- **Conditional branching** (`IF_THEN/ELSE`) routes the *same* picked part to *different* destinations based on a real-time digital input.
- **Registers as counters** carry **state across cycles** and drive the reset-at-20 housekeeping — exactly the discrete bookkeeping a continuous controller cannot do.
- **Position registers** make the box approach/drop points **reusable and offsettable** rather than hard-coded.
- **FINE vs CNT** is chosen per move: **FINE** at grasp and drop (accuracy), **CNT** on transit corners (speed/smoothness); **ACC** softens the present-to-operator move.

This mirrors the broader autonomy idea that **discrete mission logic** (here: labels, waits, branches, counters) sits **on top of** continuous motion (see [Mission Logic & FSM](../autonomy/mission-fsm.md)); the manipulator program is essentially a small finite-state machine expressed in teach-pendant syntax.

---

## Related

- [Forward & Inverse Kinematics](../kinematics/forward-inverse-kinematics.md) — the DH table and `S = A₁·A₂·A₃·A₄` chain that the motion instructions ultimately command.
- [Mechanical Configuration & Actuation](mechanical-configuration.md) — gripper open/close and the prismatic vertical stroke are actuated motions.
- [Mission Logic & FSM](../autonomy/mission-fsm.md) — labels/waits/branches/counters are a teach-pendant FSM over the work cycle.
- [Trajectory Generation & Tracking](../autonomy/trajectory.md) — J/L/C/A formats and FINE/CNT/ACC shape the executed trajectory.
- [Control Systems & PID](../autonomy/control-pid.md) — the servo loops that realise each commanded point beneath the program.

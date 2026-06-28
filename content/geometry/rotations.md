---
tags: [robotics, rotations]
---

# Rotations & Orientation

**Orientation** (= attitude = rotation): which way a body is turned — the **R** half of pose (translation lives in [Coordinate Frames & Transforms](coordinate-frames.md)). No single best representation; each trades **compactness vs singularities vs compute vs readability**. Pick badly → gimbal lock or estimator divergence.

---

## 1. Rotation matrix (DCM)

Columns = r's axes expressed in w:

    R_r^w = [ x_r^w | y_r^w | z_r^w ]

Each column = one rotated axis seen from the reference (hence **Direction Cosine Matrix**). 2D:

    R(θ) = [ cosθ  −sinθ ]
           [ sinθ   cosθ ]

| Property | Statement | Meaning |
|----------|-----------|---------|
| **Orthogonality** | Rᵀ·R = I | unit-length, mutually ⊥ columns |
| **Inverse = transpose** | R⁻¹ = Rᵀ | undoing is free |
| **Right-handed** | det(R) = +1 | not a reflection (det = −1) |

Elementary rotations:

    Rx(φ) = [ 1     0       0    ]
            [ 0   cosφ   −sinφ   ]
            [ 0   sinφ    cosφ   ]

    Ry(ψ) = [  cosψ   0   sinψ  ]
            [    0    1    0    ]
            [ −sinψ   0   cosψ  ]

    Rz(θ) = [ cosθ  −sinθ   0 ]
            [ sinθ   cosθ   0 ]
            [   0      0    1 ]

Operations (all matrix algebra, no trig):
- Rotate: `p_w = R_r^w · p_r`
- Compose: `R_c^w = R_r^w · R_c^r` (domino rule; **not commutative**)
- Invert: `R_w^r = (R_r^w)ᵀ`

**Drawback**: 9 numbers for 3 DoF (over-parametrized), poor readability.

---

## 2. Euler's theorem → minimal forms

**Euler (1775)**: any rotation = ≤3 elementary rotations, no two consecutive about the same axis → **3 params suffice**.

### RPY (roll-pitch-yaw)

    R_r^w = Rz(γ) · Ry(β) · Rx(α)     (γ=yaw, β=pitch, α=roll)

Minimal + intuitive. Drawbacks:
- **Convention ambiguity** — order + intrinsic/extrinsic not fixed; unlabeled triple is dangerous.
- **Trig-heavy** compose/invert.
- **Gimbal lock** at **pitch = ±π/2**: roll & yaw axes align, lose a DoF, infinitely many (roll,yaw) give same attitude. `R = Rz(δ)·Ry(π/2)·Rx(α+δ)` independent of δ. **No 3-param representation is singularity-free** — singularity just moves.

---

## 3. Axis-angle & Rodrigues

**Euler (1776)**: every rotation = angle θ about unit axis u. Axis-angle `(u, θ)` — visualizable, 4 numbers (3 with unit constraint), gateway to Lie theory.

**Rodrigues** (axis-angle → matrix):

    R = cosθ·I + sinθ·[u]× + (1 − cosθ)·u·uᵀ

    [u]× = [  0   −u_z   u_y ]
           [  u_z   0   −u_x ]
           [ −u_y  u_x    0  ]     (v₁ × v₂ = [v₁]× · v₂)

Back: `θ = arccos((tr(R) − 1)/2)`; **u = eigenvector of R with eigenvalue 1** (R·u = u). Drawbacks: composition needs trig; **not unique** (`R(u,θ) = R(u, θ+2kπ)`). Inverse trivial: `R(u,θ)⁻¹ = R(u,−θ) = R(−u,θ)`.

---

## 4. Quaternions

Singularity-free *and* more compact than a matrix. Unit quaternion (Hamilton 1843):

    q = [ sin(θ/2)·u ; cos(θ/2) ]     (vector v, scalar s)

‖q‖ = 1 → 3D rotation, **4 params, no singularities** (the price of safety). Facts:
- **Double cover**: `R(q) = R(−q)` — q and −q same rotation; sign ambiguity bites some **estimation** problems.
- **Composition** = quaternion product `q_c^w = q_r^w ⊗ q_c^r` — **16 mults** vs **27** for matrices.
- **Inverse**: flip vector part, `q⁻¹ = [−v ; s]`.
- Harder for humans to read.

Pattern: store orientation as **quaternion (x,y,z,w)** (stable, gimbal-lock-free), **convert to RPY only for human/debug** inspection.

---

## 5. Choosing

| Representation | params | Singular? | Readable | Cost | Best for |
|----------------|--------|-----------|----------|------|----------|
| **Matrix (DCM)** | 9 | none | poor | cheap | calculation, estimation, transforms |
| **Euler/RPY** | 3 | **yes (gimbal lock)** | excellent | trig | human I/O, debugging |
| **Axis-angle** | 4 (3 unit) | mild (2π wrap) | good | trig compose | visualization, interpolation |
| **Unit quaternion** | 4 | **none** | fair | cheapest compose | storage, rendering, attitude propagation |

**Course preference**: **matrices for estimation** — sidestep quaternion sign ambiguity, clean matrix algebra. Practical: **mix** — matrices/quaternions internally, RPY at the human interface.

---

## Related

- [Coordinate Frames & Transforms](coordinate-frames.md) — R is the rotation block of every pose and SE(3) transform.
- [Pose & Kinematics](../kinematics/pose-kinematics.md) — how orientation propagates over time via angular rates and gimbal-lock-safe updates.
- [Forward & Inverse Kinematics](../kinematics/forward-inverse-kinematics.md) — elementary rotations chained through DH parameters for arms.
- [Sensors & State Estimation](../autonomy/state-estimation.md) — why estimators favor rotation matrices; attitude drift from gyro integration.
- [Robot Programming & Manipulators](../hardware/robot-programming.md) — orientation as part of an end-effector target pose.

## Handbook references
- *Robotic Manipulation* — [Spatial Algebra (Appendix A)](https://manipulation.csail.mit.edu/spatial.html)
- *Underactuated Robotics* — [Multi-Body Dynamics (Appendix)](https://underactuated.csail.mit.edu/multibody.html)

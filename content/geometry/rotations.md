---
tags: [robotics, rotations]
---

# Rotations & Orientation

**Why this note exists.** Position tells you *where* a body is; **orientation** tells you *which way it is turned*. The terms **orientation**, **attitude**, and **rotation** are used interchangeably for this "which way is it facing" notion. Orientation is the **R** half of every pose (the other half, translation, lives in [Coordinate Frames & Transforms](coordinate-frames.md)). It is deceptively hard: there is no single "best" way to write a rotation, each representation trades **compactness against singularities against computational cost against human readability**, and choosing badly causes a drone to flip at the wrong moment (gimbal lock) or an estimator to diverge. This note surveys the four standard representations and when to reach for each.

---

## 1. The rotation matrix (Direction Cosine Matrix)

The naive-but-clever idea: to describe frame **r** relative to frame **w**, treat the tip of each of r's axes as a point and **stack their coordinates, expressed in w, as the columns** of a matrix:

    R_r^w = [ x_r^w | y_r^w | z_r^w ]

So **each column is one axis of the rotated frame seen from the reference frame** — which is why it is also called the **Direction Cosine Matrix (DCM)** in aerospace. The 2D version is the familiar

    R(θ) = [ cosθ  −sinθ ]
           [ sinθ   cosθ ]

### Properties (what makes a matrix a rotation)

A rotation matrix is **not** a generic matrix — its columns are orthonormal axes obeying the right-hand rule:

| Property | Statement | Meaning |
|----------|-----------|---------|
| **Orthogonality** | Rᵀ·R = I | columns are unit-length and mutually perpendicular |
| **Inverse = transpose** | R⁻¹ = Rᵀ | undoing a rotation is free (just transpose) |
| **Right-handedness** | det(R) = +1 | x × y = z; not a mirror/reflection (det = −1 would be a reflection) |

The elementary 3D rotations about each axis:

    Rx(φ) = [ 1     0       0    ]
            [ 0   cosφ   −sinφ   ]
            [ 0   sinφ    cosφ   ]

    Ry(ψ) = [  cosψ   0   sinψ  ]
            [    0    1    0    ]
            [ −sinψ   0   cosψ  ]

    Rz(θ) = [ cosθ  −sinθ   0 ]
            [ sinθ   cosθ   0 ]
            [   0      0    1 ]

### Operations all reduce to matrix algebra

- **Rotate a point** from r into w: `p_w = R_r^w · p_r`.
- **Compose** rotations: `R_c^w = R_r^w · R_c^r` (subscript of the first matches superscript of the second; **not commutative**).
- **Invert** (orientation of w in r): `R_w^r = (R_r^w)ᵀ`.

These are the same composition/inverse rules used for full poses in [Coordinate Frames & Transforms](coordinate-frames.md); here they are cheap matrix products and transposes, with **no trigonometry**. The drawbacks: 9 numbers for 3 degrees of freedom (heavily **over-parametrized**) and poor human readability — you cannot eyeball "30° of pitch" from nine cosines.

---

## 2. Euler's theorem → minimal representations

**Euler's rotation theorem (1775):** *any* rotation is the product of **at most three elementary rotations** about axes, no two consecutive about the same axis. So **3 parameters suffice** for a 3D rotation — confirming the matrix's 9 numbers are redundant.

### Euler angles & roll–pitch–yaw (RPY)

The popular RPY convention orders the elementary rotations as

    R_r^w = Rz(γ) · Ry(β) · Rx(α)

with **γ = yaw, β = pitch, α = roll**. RPY is attractive because it is **minimal** (3 numbers for 3 DoF) and, with a well-chosen reference frame, **intuitive** — roll leans left/right, pitch tilts fore/aft, yaw turns left/right. But Euler angles carry three real drawbacks:

- **Convention ambiguity** — Euler's theorem fixes neither the axis order nor whether axes are intrinsic/extrinsic; the same physical rotation has *different* angle triples under different conventions, so an unlabeled RPY triple is dangerous.
- **Trigonometric operations** — composing and inverting requires sines and cosines, slower and harder to analyze than matrix products.
- **Singularities = gimbal lock** — at **pitch = ±π/2** the representation collapses: the roll and yaw axes align, a degree of freedom is lost, and infinitely many (roll, yaw) pairs describe the same attitude. Formally `R = Rz(δ)·Ry(π/2)·Rx(α+δ)` is independent of δ. This is **gimbal lock**, the failure that flips physical gimbals and crashes naïve attitude controllers. It is not a quirk of RPY: **no 3-parameter representation can be singularity-free** — the singularity just moves to {0, π} or {±π/2} depending on the axis order.

---

## 3. Axis-angle and Rodrigues' formula

**Euler's other theorem (1776):** every rotation is a rotation by some **angle θ about a single unit axis u** (‖u‖ = 1). This gives the **axis-angle** representation `(u, θ)` — easily visualized, only 4 numbers (3 with the unit constraint), and the gateway to Lie-group theory.

**Rodrigues' rotation formula** converts axis-angle to a matrix:

    R = cosθ·I + sinθ·[u]× + (1 − cosθ)·u·uᵀ

where `[u]×` is the **skew-symmetric cross-product matrix**

    [u]× = [  0   −u_z   u_y ]
           [  u_z   0   −u_x ]
           [ −u_y  u_x    0  ]

which satisfies v₁ × v₂ = [v₁]× · v₂. Going back: `θ = arccos((tr(R) − 1)/2)`, and the **axis u is the eigenvector of R with eigenvalue 1** (the one direction a rotation leaves unchanged, since R·u = u). Drawbacks: composition still needs trigonometry, and it is **not unique** — `R(u, θ) = R(u, θ + 2kπ)`. Its inverse is pleasantly trivial: `R(u, θ)⁻¹ = R(u, −θ) = R(−u, θ)`.

---

## 4. Quaternions

The motivating question: is there a representation that is **singularity-free** *and* **more compact than a matrix**? Hamilton's **unit quaternion** (1843) answers yes. It rearranges the axis-angle pair into four numbers:

    q = [ sin(θ/2)·u ; cos(θ/2) ]     (vector part v, scalar part s)

A **unit quaternion** (‖q‖ = 1) encodes a 3D rotation with **4 parameters and no singularities** — the minimal singularity-free representation (recall every 3-parameter scheme must have singularities, so 4 is the price of safety). Key facts:

- **Double cover:** `R(q) = R(−q)` — `q` and `−q` are the *same* rotation. This sign ambiguity is mostly harmless but, as the course notes, it causes subtle trouble in some **estimation** problems.
- **Composition** is the quaternion product: `q_c^w = q_r^w ⊗ q_c^r` — only **16 multiplications**, versus **27** for matrix composition. This cheapness is why quaternions dominate computer graphics and 3D navigation, where many points are rotated quickly.
- **Inverse** just flips the sign of the vector part: `q⁻¹ = [−v ; s]`.
- Slightly **harder for a human to read** than RPY.

In a simulation pipeline, the robot's **state = position + orientation**, and the orientation is commonly stored as a **quaternion (x, y, z, w)** because it is numerically stable and gimbal-lock-free, then **converted to Euler angles only for human inspection/debugging** (roll/pitch/yaw printouts).

---

## 5. Choosing a representation

| Representation | # params | Singularities? | Human-readable | Compute cost | Best for |
|----------------|----------|----------------|----------------|--------------|----------|
| **Rotation matrix (DCM)** | 9 (for 3 DoF) | none | poor | cheap (products/transpose) | calculation, estimation, transforms |
| **Euler / RPY** | 3 | **yes (gimbal lock)** | excellent | trig-heavy | human I/O, intuition, debugging |
| **Axis-angle (u, θ)** | 4 (3 if unit) | mild (2π wrap) | good | trig for composition | visualization, interpolation theory |
| **Unit quaternion** | 4 | **none** | fair | cheapest composition | storage, fast rendering, attitude propagation |

**The course's working preference:** despite the over-parametrization, **rotation matrices are preferred in estimation problems**, precisely because they sidestep the quaternion sign ambiguity (`R(q) = R(−q)`) that can trip up filters, and because their operations are clean matrix algebra. The practical pattern is to **mix representations**: matrices/quaternions internally for math, RPY at the human interface.

---

## Related

- [Coordinate Frames & Transforms](coordinate-frames.md) — R is the rotation block of every pose and SE(3) transform.
- [Pose & Kinematics](../kinematics/pose-kinematics.md) — how orientation propagates over time via angular rates and gimbal-lock-safe updates.
- [Forward & Inverse Kinematics](../kinematics/forward-inverse-kinematics.md) — elementary rotations chained through DH parameters for arms.
- [Sensors & State Estimation](../autonomy/state-estimation.md) — why estimators favor rotation matrices; attitude drift from gyro integration.
- [Robot Programming & Manipulators](../hardware/robot-programming.md) — orientation as part of an end-effector target pose.

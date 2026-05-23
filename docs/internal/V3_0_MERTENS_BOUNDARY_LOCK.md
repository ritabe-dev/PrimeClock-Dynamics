# v3.0 Mertens Boundary Lock

Status: internal planning lock for the next PrimeClock Dynamics theorem
surface. This is not a public artifact, not a DOI record, not a posted
preprint, and not peer reviewed.

## Title

```text
PrimeClock Dynamics v3.0:
The Mertens Boundary of Angular Kubilius Chaos
```

Subtitle:

```text
Mertens-Normalized Uncovered Measures in the Complete-CRT Model
```

## Central Object

Work in the complete-CRT probability space

```text
Omega = product_p Z/pZ
```

with independent uniform residues `R_p`. For cutoff `x`,

```text
D_x(R, alpha) = sum_{p <= x} 1_{R_p = r_p(alpha)}
P_x = product_{p <= x} (1 - 1/p)
U_x(R) = Leb{alpha in T : D_x(R, alpha) = 0}
```

The v3.0 object is the Mertens-normalized uncovered measure

```text
nu_x(d alpha) = 1_{D_x(R, alpha)=0} / P_x d alpha.
```

Equivalently,

```text
V_p(alpha) = (1 - 1_{R_p=r_p(alpha)}) / (1 - 1/p)
nu_x(d alpha) = product_{p <= x} V_p(alpha) d alpha.
```

This is the hard endpoint of the v2.0 finite-beta AKC measure under
`beta -> -infinity`.

## Locked Claim Surface

v3.0 should target exactly these theorem labels:

- `PCD-MB-MART`: Mertens-normalized uncovered random measures are martingales.
- `PCD-MB-QPOINT`: q-point local factor formula for the hard endpoint.
- `PCD-MB-L2`: finite L2 total-mass bound for the normalized uncovered measure.
- `PCD-MB-LIMIT`: weak convergence of complete-CRT Mertens-boundary random
  finite measures.
- `PCD-MB-FB-ENDPOINT`: finite-cutoff compatibility with the
  `beta -> -infinity` finite-beta AKC endpoint.

Do not add integer-time diagonal Mertens, high-point, zero-geometry, or
prime-time claims to v3.0.

## Proof Route

The proof route should mirror v2.0, with hard endpoint local factors.

1. One-prime normalization:

```text
E_{R_p} V_p(alpha) = 1.
```

2. q-point hard local factor. For fixed angles
`alpha_1,...,alpha_q`, let

```text
k_p(alpha_1,...,alpha_q)
= |{r_p(alpha_1),...,r_p(alpha_q)}|.
```

Then

```text
L_p^MB(alpha_1,...,alpha_q)
= (1 - k_p/p) / (1 - 1/p)^q.
```

3. Two-point factors:

```text
collision:   1 / (1 - 1/p)
separated:   (1 - 2/p) / (1 - 1/p)^2
           = 1 - 1/(p-1)^2.
```

Separated primes do not create growth. Growth comes only from collision primes.

4. Use the collision-sum bound:

```text
sum_{p <= x, r_p(alpha)=r_p(gamma)} 1/p
<= C0 + C1 log log min(x, C2 / ||alpha-gamma||_T).
```

5. Deduce the two-point density bound:

```text
E rho_x^MB(alpha) rho_x^MB(gamma)
<= C (1 + log(1 / ||alpha-gamma||_T))^C.
```

This is integrable on the circle, giving

```text
sup_x E[nu_x(T)^2] < infinity.
```

6. Use the v2.0 dense `Q`-vector-subspace / Riesz route for weak convergence.

## Gate R Deliverables

The first v3.0 milestone is Gate R, not direct public release.

Expected Gate R surface:

- `docs/MB_V3_0_CLAIM_BOUNDARY.md`
- `paper/mertens_boundary_v3_0_gate_r.md`
- `experiments/mb/run_mb_v3_0_gate_r_support.py`
- `experiments/_workflow/pcd_v3_0_mertens_boundary_gate_r.json`
- `experiments/mb/_workflow/check_mb_v3_0_gate_r.py`

Gate R support should include:

- one-prime hard normalizer;
- q-point hard local factor exactness;
- cell polynomial with `P_x(R;0)=U_x(R)`;
- Mertens-normalized total mass `U_x/P_x`;
- two-point integral support;
- negative-beta approach diagnostic comparing to `U_x/P_x`, not `U_x`;
- slow integer-time transfer diagnostic only as future work.

## Non-Claims

v3.0 must explicitly not claim:

- integer-time transfer;
- diagonal Mertens uncovered-measure theorem;
- `U_n(n) log n -> e^{-gamma}`;
- `beta -> +infinity` high-point theorem;
- Fisher-zero theorem;
- Lee-Yang theorem;
- standard Gaussian Multiplicative Chaos;
- prime-time theorem;
- a new proof of the classical Mertens theorem;
- posted preprint or peer review.

## Next Versions

After v3.0:

- `v3.5`: Soft Integer-Time Transfer for Mertens-normalized uncovered measures.
- `v4.0`: Diagonal Mertens Uncovered-Measure Program.
- `v5.0`: High Points / Extremal Field, the `beta -> +infinity` direction.

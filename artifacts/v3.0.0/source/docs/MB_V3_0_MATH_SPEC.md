# PrimeClock Dynamics v3.0 Mertens Boundary Math Spec

Status: mathematical specification for the complete-CRT Mertens-boundary
theorem surface. This shared specification supports the reviewed Gate C
surface and the v3.0 public artifact.

## Complete-CRT Space

Let

```text
Omega = product_p Z/pZ
```

with independent uniform coordinates `R_p`.

For `alpha in T`, the selected residue is `r_p(alpha)`, using the repository's
half-open cell convention.

## Hard Endpoint Definitions

```text
D_x(R, alpha) = sum_{p <= x} 1_{R_p = r_p(alpha)}
P_x = product_{p <= x} (1 - 1/p)
U_x(R) = Leb{alpha in T : D_x(R, alpha)=0}
nu_x(d alpha) = 1_{D_x(R, alpha)=0} / P_x d alpha.
```

The one-prime factor is

```text
V_p(alpha) = (1 - 1_{R_p = r_p(alpha)}) / (1 - 1/p).
```

Then `nu_x(d alpha) = product_{p <= x} V_p(alpha) d alpha`.

## Boundary Convention

For each prime `p` and residue `r mod p`, the selected-residue cell is the
half-open circular cell

```text
C_{p,r} = [(r - 1/2)/p, (r + 1/2)/p) mod 1.
```

Pointwise quantities use this convention:

```text
r_p(alpha)=r  <=>  alpha in C_{p,r}
r_p(alpha)=floor(p alpha + 1/2) mod p.
```

This is the same selected-residue convention used by the repository's fixed
PrimeClock models. It gives a unique selected residue even at endpoints.

For integrated quantities, including `U_x(R)` and the cell polynomial
`int_T u^{D_x(R,alpha)} d alpha`, boundary assignments are immaterial. For
finite cutoff the union of all selected-cell boundaries is finite and has
Lebesgue measure zero. Exact cell integrations therefore cut at all boundaries
and sample an interior point of each open cell.

## q-Point Local Factor

For fixed angles `alpha_1, ..., alpha_q`, set

```text
k_p(alpha_1,...,alpha_q)
  = |{r_p(alpha_1),...,r_p(alpha_q)}|.
```

The hard local factor is

```text
L_p^MB(alpha_1,...,alpha_q)
  = (1 - k_p/p) / (1 - 1/p)^q.
```

Hence the complete-CRT q-point factor is the finite product of these local
factors over `p <= x`.

## Two-Point Factors

For two angles, the factor splits into two cases.

Collision:

```text
r_p(alpha)=r_p(gamma)
L_p^coll = 1 / (1 - 1/p).
```

Separated:

```text
r_p(alpha)!=r_p(gamma)
L_p^sep = (1 - 2/p) / (1 - 1/p)^2
        = 1 - 1/(p-1)^2.
```

Separated primes do not create growth; only collision primes contribute a
reciprocal-prime growth factor.

For `p=2`, the separated factor is zero. This is harmless for upper-bound
arguments: use `0 <= L_p^sep <= 1` and never take logarithms of separated
zero factors.

## L2 Route

The expected L2 total mass is controlled by the two-point density:

```text
E[nu_x(T)^2]
  = int_T int_T E[rho_x(alpha) rho_x(gamma)] d alpha d gamma.
```

The route is:

1. Use the q-point formula at `q=2`.
2. Bound separated factors by an absolutely convergent product.
3. Bound collision factors by `exp(C sum_{collision p} 1/p)`.
4. Use the selected-cell diameter implication from the half-open convention:
   `r_p(alpha)=r_p(gamma) => p ||alpha-gamma||_T <= C`, with an absolute
   constant such as `C=2`.
5. Conclude a logarithmic-power two-point bound and integrate it.

## Fixed-Cutoff beta Endpoint

For fixed cutoff `x`, v2.0 AKC satisfies

```text
mu_{x,beta}(d alpha)
  = exp(beta D_x(R, alpha)) / Z_x(beta) d alpha
```

and as `beta -> -infinity`,

```text
exp(beta D_x(R, alpha)) -> 1_{D_x(R, alpha)=0}
Z_x(beta) -> P_x.
```

Thus `mu_{x,beta}` approaches `nu_x` for fixed `x`. The v3.0 theorem surface
does not claim interchange of the `x -> infinity` and `beta -> -infinity`
limits.

For support diagnostics, the total mass is computed from the exact cell
polynomial

```text
P_{x,R}(u) = int_T u^{D_x(R,alpha)} d alpha = sum_k m_k(R) u^k
mu_{x,beta}(T) = P_{x,R}(e^beta) / Z_x(beta).
```

This avoids endpoint-grid bias from sampling points that lie exactly on
selected-residue cell boundaries.

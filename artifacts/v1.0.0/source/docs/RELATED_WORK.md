# Related Work

PrimeClock Dynamics v1.0.0 is built from classical probabilistic number theory,
finite CRT independence, and fixed-cutoff sieve-density identities. It does not
claim new versions of the classical theorems listed here; it uses them as the
background for the PrimeClock residue-class formulation.

- The distinct prime-divisor function `omega(n)`. The `alpha=0` fiber satisfies
  `D(n,0)=omega(n)` under the documented half-open convention.
- The Erdos-Kac theorem for the normal order and distribution of `omega(n)`. The
  `alpha=0` fiber recovers `omega(n)`, while the v1.0 theorem proves the
  corresponding fixed-angle PrimeClock residue-class extension on dyadic
  windows. This is consistent with the classical theorem and is not presented
  as a new strengthening of it.
- Additive arithmetic functions and residue-class additive functions. The
  fixed-angle selector rewrites `D_x(n,alpha)` as a finite prime-indexed sum of
  residue-class indicators.
- Bernoulli sums and triangular-array central limit methods. In the
  complete-CRT model, the selected residue events become independent
  Bernoulli variables with probabilities `1/p`.
- The Chinese remainder theorem as finite independence across prime residue
  coordinates over a complete CRT period.
- Finite-window residue-class counting. The dyadic finite-window step uses
  `N/q+O(1)` residue-class counts to transfer fixed moments from the complete
  CRT model to a slow cutoff.
- Slutsky's theorem and Cramer-Wold. The diagonal result uses L1 tail removal
  and the finite-dimensional result uses fixed Cramer-Wold projections.
- Mertens' product theorem for `prod_{p<=x}(1-1/p)`. The v1.0 Mertens surface is
  the fixed-cutoff CRT uncovered-average identity plus the classical product
  asymptotic; it is not a diagonal Mertens uncovered-measure law.
- Random interval covering models on the circle, including Dvoretzky-type
  covering questions. These remain comparison context only and are not part of
  the v1.0 theorem surface.
- Prime Reciprocal Covering as a separate finite artifact program. PrimeClock
  Dynamics does not claim a theorem extending that artifact line.

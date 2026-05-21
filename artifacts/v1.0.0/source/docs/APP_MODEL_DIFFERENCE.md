# App / Model Difference

This is the canonical model-difference note for PrimeClock Dynamics public
artifacts. The visual app is a display surface, not the exact mathematical
model.

Known differences:

- rendered primes are capped by `MAX_RENDER_PRIME`;
- large-prime arcs use a minimum visual width for readability;
- canvas strokes and hover tolerances are visual aids;
- visual arc strokes do not define `D(n, alpha)` or `U(n)`;
- exact definitions and claims use `docs/MATH_SPEC.md`, the main manuscript,
  and the Python package.

Use the app to explain and inspect the Prime Clock visually. Use the Python
package, tests, and manuscript for mathematical definitions and checks. The
v1.0.0 public artifact may exclude `app/`, but it includes this document so the
app/model boundary remains reviewable.

# NerveSense — Operating Principle & Theory

This document explains *why* NerveSense should work in principle, the physics
behind the distance estimate, and the assumptions that estimate rests on. For
how it was actually tested, see [TESTING.md](TESTING.md).

---

## 1. The intended biological mechanism

NerveSense is a **stimulate-and-record** proximity sensor:

1. **Stimulate.** TENS pads deliver a 20 Hz pulse train to the tissue around the
   surgical site. Clinical work shows ~20 Hz at a few volts of contact drive is
   sufficient to elicit a **compound action potential (CAP)** from a peripheral
   nerve (Ahn et al., 2025).
2. **Re-radiate.** A firing nerve is, electrically, a **propagating current
   source** inside a conductive volume (tissue). It sets up a potential field
   that spreads outward through the surrounding medium (volume conduction).
3. **Record.** A scalpel-mounted electrode (S+) and a distant reference (S−)
   measure the local potential of that field. The **closer the probe is to the
   nerve, the larger the recorded potential.**
4. **Convert.** Amplitude → distance via a calibrated curve.

The signal of interest is **phase-locked to the 20 Hz stimulus**, which in
principle separates "the nerve we are driving" from unrelated tissue noise.

---

## 2. Why amplitude encodes distance

In a conductive medium, the potential from a current source falls off with
distance from that source. The device leans on this monotonic relationship:
more voltage at the probe ⇒ closer to the source.

### Analytical sketch (the physics-first derivation)

Model the path between source and probe as a conductor whose resistance depends
on geometry:

```
R = ρ · L / A
```

- `ρ` — resistivity of the tissue (inverse of conductivity σ; muscle ≈ 0.15 S/m
  across-fiber)
- `L` — effective path length between source and probe (∝ distance)
- `A` — effective cross-sectional area of the conduction path

By Ohm's law the potential seen at the probe scales with this path resistance
for a given source current, and the instrumentation amplifier multiplies the
result by its gain `G`:

```
V_probe(measured) = G · I_source · R(L)  =  G · I_source · ρ · L / A
```

Because the *effective* `A` grows as the field spreads with distance while `L`
also grows, the measured amplitude **decays** as the probe moves away — and the
decay is steeper than linear, which is why an **exponential** fits the data far
better than a straight line. The full closed form (with the geometric
assumptions) is Appendix E of the project report.

> The analytical model gets the **shape** right but depends on `ρ`, geometry,
> and gain that are hard to pin down in messy tissue — which is why the shipped
> firmware uses the **empirical** fit instead (below).

### Empirical model (what actually ships)

```
d = 20 · e^(−7.21 · avg_diff_volts)          (d in cm)      R² = 0.9321
```

Fit to 10 measured (distance, voltage) points in a tissue phantom. See
[TESTING.md](TESTING.md) §5.

---

## 3. Signal conditioning (why the hardware looks the way it does)

The raw CAP is ~100 mV — far too small for the Raspberry Pi Pico's ADC and
buried in noise. The receive chain addresses this:

- **AD620 instrumentation amplifier, ×100** — measures the *difference* between
  S+ and S− (rejecting common-mode noise) and boosts it into the Pico's
  readable range.
- **Custom INA333 PCB + bandpass filter (alternative front end)** — designed to
  additionally reject everything outside the 20 Hz stimulation band. It needs a
  small DC bias to activate (the amplifier only turns on above ~0.1 V), solved
  with a voltage divider + 2.5 V pull-up. It ran reliably for ~3 weeks before
  both boards were destroyed; the AD620 module was the fallback for the demo.
- **AgCl-coated silver electrodes** — a bare stainless-steel electrode
  polarizes and turns the tissue interface into a **capacitor**, distorting the
  reading. Ag/AgCl is the standard **non-polarizable** bioelectrode; we made ours
  by coating silver wire via a bleach reaction.
- **Grounding electrode on the stimulator** — continuously discharges the tissue
  so the stimulus doesn't slowly charge the phantom like a capacitor.

---

## 4. Key assumptions (and where they can break)

| Assumption | Holds when… | Breaks when… |
|------------|-------------|--------------|
| Source behaves like a clean line current source | Nerve fires synchronously to the stimulus | Weak/desynchronized firing; multiple nerves |
| Medium is roughly homogeneous & isotropic near the probe | Uniform phantom | Real tissue: fat/vessel/bone boundaries, anisotropy |
| Amplitude maps 1:1 to distance | Fixed source strength & geometry | Different nerve caliber/orientation → same amplitude, different distance |
| Calibration constants are valid | Same tissue type as calibration | New tissue conductivity → curve shifts (needs recalibration) |

These are exactly the questions a research collaboration would tackle — see
[RESEARCH.md](RESEARCH.md).

---

## 5. How this differs from existing nerve monitors

Commercial intraoperative systems (e.g. NuVasive/Globus NVM5, Medtronic NIM)
and stimulating dissectors work by **stimulating from the instrument and
recording the downstream muscle EMG** — proximity is inferred from the stimulus
current needed to evoke a twitch. NerveSense instead **stimulates proximally and
records the CAP directly at the probe.** That distinction is the potentially
novel part: it does not depend on an intact motor pathway or neuromuscular
junction, so in principle it could apply to sensory nerves and to nerves whose
target muscle isn't accessible. Whether that theoretical advantage survives
contact with a real nerve is the open research question.

---

## References

- Ahn, H.-Y., et al. (2025). *Bioresorbable, wireless dual stimulator for
  peripheral nerve regeneration.* Nature Communications 16(1).
  https://doi.org/10.1038/s41467-025-59835-7
- Zelenski, N.A., Oishi, T., Shin, A.Y. (2023). *Intraoperative Neuromonitoring
  for Peripheral Nerve Surgery.* J Hand Surg 48(4), 396–401.
  https://doi.org/10.1016/j.jhsa.2022.11.022

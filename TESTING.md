# NerveSense — Testing & Validation

> **Read this first if you want to know *how we know NerveSense works*.** Every
> performance number in the README comes from the bench experiments described
> here. NerveSense has **never been tested on a live nerve or living tissue** —
> all validation to date used a controlled *nerve analog* inside a *tissue
> phantom*. This is deliberate (see [Ethics & Safety](#ethics--safety)), and it
> defines exactly what has and has not been proven.

---

## 1. Why a phantom?

We had no access to live nerves, animal models, or ex-vivo nerve preparations,
and our team contract explicitly ruled out testing on any organism. To develop
and characterize the device we therefore built a two-part physical model:

1. A **nerve analog** — a controllable electrical source standing in for a
   firing nerve.
2. A **tissue analog (phantom)** — a conductive medium standing in for the
   volume of tissue between the nerve and the probe.

This lets us vary "distance to nerve" precisely and repeatably, which a real
surgical field never would.

---

## 2. The nerve analog

A **bare copper wire** was embedded in the tissue phantom and driven with:

| Parameter        | Value                          | Rationale |
|------------------|--------------------------------|-----------|
| Amplitude        | **110 mV**                     | Matches the ~100 mV peak of a real compound action potential (CAP) |
| Frequency        | **20 Hz**                      | Same frequency the signaling unit stimulates at; a real nerve re-fires in sync with the stimulus |
| Waveform         | **Pulsed DC**                  | Biphasic pulsing approximates the AC waveform of a propagating CAP |

The wire acts as a **linear current source** inside the conducting medium. When
you stimulate a real nerve, the depolarizing nerve behaves (to first order) like
exactly this kind of line source re-radiating into the surrounding tissue — so
the analog reproduces the *field the probe would see*, without requiring live
excitable tissue.

> **Characterization note.** During curve-fitting we initially drove the analog
> at a **higher-than-physiological voltage** to get a clean, high-SNR
> distance–voltage relationship, then **stepped the amplitude down** toward the
> real ~100 mV CAP level. This was a deliberate choice from interim-demo
> feedback: establish the relationship first, then push it toward realism.

---

## 3. The tissue analog (phantom)

Two media were used over the course of the project:

| Medium | Notes |
|--------|-------|
| **Agar / saline gel** | Castable, homogeneous, tunable conductivity. A batch was mixed toward **~0.15 S/m** — the approximate conductivity of skeletal muscle measured *across* (transverse to) the muscle fibers. Convenient for repeatable geometry. |
| **Chicken breast** | Real biological tissue, heterogeneous and anisotropic, with conductivity close to human soft tissue. **Used for the final demonstration** because it was the most reliable and accessible. |

We settled on **chicken breast** for the demo. Agar/gel was used earlier for
controlled, repeatable trials.

> ⚠️ **Data-availability caveat.** The quantitative results from the
> **0.15 S/m agar-saline gel** runs may **not have been captured/published**
> alongside the chicken-breast data. Treat the agar figures as *indicative*
> until the raw sheets are located and added to this repo. If you have them,
> drop the CSV/spreadsheet in a `data/` folder and update this file.

---

## 4. Measurement setup

```
   [L298N #1] --20 Hz--> [Stimulating TENS pad] ─┐
                                                 │   (in a real patient this
                                                 │    would fire the nerve)
   [Nerve analog: Cu wire @ 110 mV / 20 Hz] ─────┤   embedded at a known depth
                                                 │
   ================ tissue phantom ==============│=====
                                                 │
   [Scalpel probe S+] --+                        │
                        |--> [AD620 x100] --> [Pico ADC0 / GP26]
   [Reference S-]    ---+
```

The probe (S+) is advanced toward the analog at **measured distances**. At each
distance the firmware records the amplified differential voltage.

### What the firmware actually computes

From [`Code/NerveSenseTotal-v1.2.py`](Code/NerveSenseTotal-v1.2.py):

- **`baseline`** — mean ADC reading captured at startup (device at rest).
- **`avg_diff_volts`** — over each **250 ms** window, the mean of
  `(sample − baseline)` converted to volts. This is the signal that encodes
  distance.
- **`distance`** — `calc_distance(avg_diff_volts)` (see §5).

---

## 5. From voltage to distance — two approaches

We derived the distance estimate two independent ways and kept the one that
tracked the data best.

### Analytical (physics-first)
Starting from `R = ρL / A` (resistance of a conductor vs. length and
cross-section) and Ohm's law, combined with the instrumentation-amplifier gain,
we derived a closed-form relationship between probe–source distance and the
amplified voltage. See [THEORY.md](THEORY.md) for the derivation and its
assumptions. This gave the *right functional shape* but was sensitive to
phantom geometry and material constants.

### Empirical (data-first) — **used for the demo**
We sampled `avg_diff_volts` at **10 known distances** and fit an exponential:

```
d = 20 · e^(−7.21 · avg_diff_volts)          R² = 0.9321
```

where `d` is in cm and `avg_diff_volts` in volts. The empirical fit was the
**more accurate of the two** and is what ships in the firmware.

> The 10 raw calibration points live in **Figure 8** of the project report.
> They are **not yet in this repo as data** — adding a `data/calibration.csv`
> plus a plotting script is the single highest-value next commit for
> reproducibility.

---

## 6. Results

| Metric | Result |
|--------|--------|
| Detection range | Signal usable out to **~5 cm** from the analog |
| Distance accuracy | **±0.5 cm** within the 0–5 cm range |
| Goodness of fit | **R² = 0.9321** (10-point empirical exponential) |
| Reliability | **~10 %** of samples show voltage spikes/artifacts |

The device displayed distance and proximity warnings in real time on the LCD
with **no ambiguity** (a single monotonic reading), which was the core goal.

---

## 7. What this validates — and what it does *not*

**Validated (on the phantom):**
- A linear current source embedded in realistic conductive tissue produces a
  **monotonic, fittable voltage-vs-distance falloff** that the probe + AD620 +
  Pico chain can read in real time.
- The empirical exponential predicts distance to **±0.5 cm** over 0–5 cm in
  chicken breast, at the calibrated conditions.

**NOT yet validated (the open questions):**
- **A real excitable nerve as the source.** A copper wire is a far better
  conductor than an axon and is passively driven; a stimulated nerve produces a
  much weaker, biologically-shaped signal. Whether the SNR holds at ~100 mV
  through real tissue at surgical (mm) distances is untested.
- **Transferability of the calibration.** The constants `20` and `−7.21` are
  tied to one phantom, geometry, and tissue type. The device "requires
  recalibration for different tissue types" — quantifying that drift is future
  work.
- **Selectivity.** Everything conductive in tissue contributes to the field;
  the phantom can't show how well the nerve is distinguished from vessels or
  other structures. (See [RESEARCH.md](RESEARCH.md) for a proposed lock-in
  approach.)
- **Amplitude ambiguity.** A small source nearby and a large source farther
  away can read the same amplitude.

These gaps are not flaws in the result — they are the **scope boundary** of a
phantom study, and they define the next experiments in
[RESEARCH.md](RESEARCH.md).

---

## Ethics & Safety

NerveSense is a proof-of-concept and is **not approved for clinical use**. The
team deliberately restricted all testing to non-living phantoms. Any future
work with real nerve tissue must go through the appropriate ethics / animal-use
approvals and add hardware voltage protection and an emergency shut-off before
it goes anywhere near a living subject.

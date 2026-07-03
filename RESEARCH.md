# NerveSense — Research Directions & Open Questions

*A short, honest brief for anyone (a professor, a lab, a follow-on student team)
evaluating whether NerveSense is worth taking further.*

---

## The one-paragraph pitch

NerveSense is a low-cost prototype that estimates the distance from a surgical
probe to a peripheral nerve by **stimulating the nerve and recording its
compound action potential (CAP) directly at the probe**, then mapping the
recorded amplitude to distance. On a tissue phantom with a controlled nerve
analog, a 10-point empirical fit predicts distance to **±0.5 cm over 0–5 cm
(R² = 0.93)** and drives a real-time, unambiguous LCD readout. The physics of
the sensing principle is de-risked; the open question is whether it survives a
**real excitable nerve** and whether it can be made **selective**. That next
step needs an electrophysiology setup we don't have — which is exactly where a
research lab comes in.

---

## Why this might be a real contribution (not just a class project)

**The mechanism is different from what's commercialized.** The dominant clinical
approach — NuVasive/Globus NVM5, Medtronic NIM, stimulating dissectors — infers
proximity by **stimulating from the instrument and recording downstream muscle
EMG**. NerveSense inverts this: **stimulate proximally, record the CAP directly
at the probe.** In principle this removes the dependence on an intact motor
pathway and neuromuscular junction, opening the door to **sensory nerves** and
nerves whose target muscle isn't accessible. Whether that theoretical advantage
holds up is a genuine, scoped research question.

**We have preliminary quantitative data**, not just a concept — a fitted curve
with error bars is something a lab can build on.

---

## What has been proven vs. what hasn't

| Proven (on phantom) | Not yet proven |
|---------------------|----------------|
| Monotonic, fittable voltage↔distance falloff in real tissue | Same behavior with a **real excitable nerve** as the source |
| ±0.5 cm / 0–5 cm / R²=0.93 at calibrated conditions | Adequate **SNR** at ~100 mV CAP through mm of real tissue |
| Real-time, unambiguous readout | **Selectivity** (nerve vs. vessel/other conductors) |
| Ag/AgCl electrodes + grounding fix capacitive artifacts | **Calibration transfer** across tissue types |

See [TESTING.md](TESTING.md) for the full scope boundary.

---

## Proposed next experiments (roughly in order)

1. **Swap the copper wire for a real nerve preparation.** The classic,
   cheap, undergrad-accessible option is a **frog sciatic nerve**; an ex-vivo
   mammalian nerve is the next step up. Repeat the distance–amplitude
   characterization and see whether the exponential relationship (and the SNR)
   survive a biological source. *This is the single most important test and the
   main thing a lab's electrophysiology rig unlocks.*
2. **Add lock-in / synchronous detection at the 20 Hz stimulus frequency.**
   Only the stimulated nerve re-radiates phase-locked to the stimulus; passive
   conductors and noise do not. Phase-sensitive detection should sharply improve
   both **SNR** and **selectivity** — and is itself a publishable methods
   contribution. (Currently the firmware reads raw amplitude.)
3. **Quantify calibration drift across media.** Run the same protocol across
   agar batches of known conductivity (0.05–0.5 S/m) and multiple tissue types
   to measure how far the `d = 20·e^(−7.21·ΔV)` constants move — and whether a
   normalization or self-calibration step can remove the need to recalibrate.
4. **Attack the amplitude-ambiguity problem.** A multi-electrode gradient probe
   or the use of CAP *latency* (not just amplitude) could disambiguate a small
   near source from a large far one.
5. **Medical-grade front end.** Move from the AD620 module to the INA333 PCB
   with proper bandpass filtering, add voltage protection and an emergency
   shut-off — prerequisites before any tissue with a live nerve.

---

## Prior art to cite / differentiate against

- Triggered-EMG proximity systems: NuVasive/Globus **NVM5**, Medtronic **NIM**.
- Patents on nerve-proximity instruments, incl. a scalpel-with-nerve-sensor
  (US 5,928,158) and nerve proximity/direction/pathology systems
  (US 9,931,077 and family).
- Intraoperative neuromonitoring reviews (Zelenski et al., 2023) and
  peripheral-nerve stimulation parameters (Ahn et al., 2025).

The point of citing these is not novelty of the *idea* (nerve-proximity sensing
is well-trodden and patented) but novelty of the **direct-CAP-recording
mechanism** and its rigorous **characterization**.

---

## What a collaborator would get out of it

- A working, documented, low-cost bench prototype (hardware, firmware, CAD, PCB)
  that already produces clean distance–voltage data.
- A tightly scoped, low-risk first experiment (nerve prep) with a clear,
  fundable question.
- A methods angle (lock-in detection) that could stand on its own.

## What we'd need from them

- Electrophysiology setup and nerve-preparation protocols.
- Ethics / tissue-use guidance and approvals.
- Supervision to turn a phantom result into a defensible, publishable study.

---

*Maintained by the NerveSense team (Northeastern University London). Contact
details are in the repo / project report.*

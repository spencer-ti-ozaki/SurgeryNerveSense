# NerveSense: Research Directions and Open Questions

*A brief for researchers evaluating NerveSense as a basis for further work.*

## Summary

NerveSense estimates the distance from a surgical probe to a peripheral nerve by
stimulating the nerve and recording its compound action potential (CAP) directly
at the probe, then mapping the recorded amplitude to distance. On a tissue
phantom driven by a controlled nerve analog, a ten-point empirical fit predicts
distance to within 0.5 cm over a 0 to 5 cm range (R² = 0.93) and produces a
real-time, unambiguous readout. The sensing physics has been demonstrated on the
bench. The two questions that determine whether the approach is clinically
meaningful, whether the relationship holds for a real excitable nerve and whether
the signal can be made selective, remain open and are the natural starting point
for a collaboration.

## Novelty

Existing intraoperative systems infer nerve proximity indirectly. Devices such as
the NuVasive/Globus NVM5, the Medtronic NIM, and stimulating dissectors deliver a
stimulus from the instrument and record the downstream muscle EMG; proximity is
read from the stimulus current required to evoke a twitch. That approach depends
on an intact motor pathway and neuromuscular junction, and it reports a muscle
response rather than a direct measurement at the tool.

NerveSense reverses the arrangement. Stimulation is applied proximally through
surface pads, and the CAP is recorded directly at the probe as a graded,
distance-dependent potential. Because the measurement is taken at the instrument
rather than at a muscle, the method does not require a motor endpoint, which in
principle extends it to sensory nerves and to nerves whose target muscle is
inaccessible. Recovering a continuous distance estimate from CAP amplitude, as
opposed to a binary "stimulus threshold crossed" signal, is the aspect most worth
investigating. Whether the graded relationship survives a biological source at
realistic signal levels is the central unknown.

## Established versus open

| Established on phantom | Open |
|------------------------|------|
| Monotonic, fittable voltage-to-distance falloff in real tissue | Same behavior with a real excitable nerve as the source |
| 0.5 cm accuracy over 0 to 5 cm at calibrated conditions | Adequate SNR at a ~100 mV CAP through millimeters of real tissue |
| Real-time, unambiguous readout | Selectivity of the nerve against vessels and other conductors |
| Ag/AgCl electrodes and a grounding pad suppress capacitive artifacts | Transfer of the calibration across tissue types |

The full scope boundary is documented in [TESTING.md](TESTING.md).

## Proposed next experiments

1. Replace the copper nerve analog with a real nerve preparation. A frog sciatic
   nerve is the standard low-cost option, with an ex-vivo mammalian nerve as the
   next step. Repeating the distance-to-amplitude characterization on a
   biological source, and confirming whether the exponential relationship and the
   SNR both hold, is the single most informative test and the main capability a
   host lab's electrophysiology rig unlocks.
2. Add synchronous (lock-in) detection at the 20 Hz stimulation frequency. Only
   the stimulated nerve re-radiates in phase with the stimulus, so phase-sensitive
   detection should improve both SNR and selectivity, and stands on its own as a
   methods result. The current firmware reads raw amplitude only.
3. Quantify calibration drift across media. Running the protocol across agar
   batches of known conductivity (0.05 to 0.5 S/m) and across tissue types would
   measure how far the fitted constants move, and whether a normalization or
   self-calibration step removes the need to recalibrate per tissue.
4. Address amplitude ambiguity. A multi-electrode gradient probe, or the use of
   CAP latency rather than amplitude alone, could separate a small near source
   from a large far one.
5. Move to a medical-grade front end. The INA333 PCB with proper bandpass
   filtering, voltage protection, and an emergency shut-off is a prerequisite
   before any work involving a living subject.

## Prior art

- Triggered-EMG proximity systems: NuVasive/Globus NVM5 and Medtronic NIM.
- Patents on nerve-proximity instruments, including a scalpel with an integrated
  nerve sensor (US 5,928,158) and nerve proximity, direction, and pathology
  systems (US 9,931,077 and its family).
- Intraoperative neuromonitoring reviews (Zelenski et al., 2023) and
  peripheral-nerve stimulation parameters (Ahn et al., 2025).

Nerve-proximity sensing as a general goal is well established and patented. The
contribution here is the direct-CAP-recording mechanism and its quantitative
characterization, which the prior art does not cover in this form.

## Collaboration

The project provides a working, documented, low-cost bench prototype, spanning
hardware, firmware, CAD, and PCB, that already yields clean distance-to-voltage
data, together with a tightly scoped first experiment and a self-contained
methods angle in the lock-in approach. Advancing it draws on capabilities a host
lab is positioned to provide: an electrophysiology setup, nerve-preparation
protocols, and the ethics and tissue-use approvals required to test on a real
nerve.

*Maintained by the NerveSense team (Northeastern University London). Contact
details are in the repository and project report.*

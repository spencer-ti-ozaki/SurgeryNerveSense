# NerveSense — Operating Instructions

> **Safety Notice:** NerveSense is a research prototype. Do not use on humans outside of a controlled experimental setting supervised by qualified medical personnel.

---

## What You'll Need

- NerveSense control unit (Raspberry Pi Pico + LCD + motor driver box)
- Scalpel/probe assembly with attached electrode wire (S+)
- 3× skin-contact electrodes:
  - 1× grounding electrode (TENS pad)
  - 1× stimulating electrode (TENS pad)
  - 1× reference electrode (S−), placed away from the incision site
- Power supply

---

## Setup & Operation

### Step 1 — Assemble the components
Connect the scalpel probe, electrodes, amplifier module, and LCD to the control unit. Ensure the AgCl electrode wires are properly coated — re-coat in bleach solution if the coating has degraded (dark tarnish indicates active coating; silver/bare wire indicates it needs re-coating). Keep electrodes away from direct sunlight, which degrades the AgCl coating.

### Step 2 — Place the grounding electrode
Attach the grounding TENS pad flat against the skin directly over the surgical site. This prevents charge from building up in the tissue during stimulation.

### Step 3 — Place the reference electrode
If available, place the reference electrode (S−) at the far end of the surgical site, well away from the intended incision point. This gives the amplifier a stable baseline to measure against.

### Step 4 — Place the stimulating electrode
Attach the stimulating TENS pad at the surgical site near the incision point. This pad delivers the electrical pulses that trigger a nerve response.

### Step 5 — Power on and calibrate
Turn on the NerveSense unit. The LCD will display **"Nervesense On"** and the device will spend the first few seconds measuring a baseline voltage. **Wait at least 5 seconds before probing** — moving the scalpel during this window will corrupt the baseline and produce inaccurate readings.

### Step 6 — Begin probing
Insert or advance the scalpel probe into the incision site. The LCD will update in real time:

| LCD Row | Displays |
|---------|----------|
| Row 1   | Proximity status (see below) |
| Row 2   | Estimated distance to nerve (cm) |
| Row 3   | Current voltage (V) |
| Row 4   | Delta voltage — ΔV from baseline (V) |

**Proximity status messages:**

| Message             | Meaning                                          |
|---------------------|--------------------------------------------------|
| `Close to Nerve`    | Probe is very close — proceed with extreme caution |
| `Medium to Nerve`   | Moderate proximity — slow down                   |
| `Far to Nerve`      | Nerve detected but distant                       |
| `Outside of Site`   | Probe is outside the detectable range or signal lost |
| `No samples in 0.25s` | No valid signal received — check electrode contact |

---

## Tips

- If readings are erratic, check that all electrode pads have firm skin contact and that the AgCl wires are properly coated.
- The device is calibrated for a specific tissue type. Readings may drift if the probe moves to a region with significantly different tissue conductivity — power cycle and recalibrate if needed.
- The scalpel probe can be extended or retracted during probing; the device reads continuously.
- Distance estimates are accurate to approximately ±0.5 cm within a 0–5 cm range.

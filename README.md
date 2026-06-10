# NerveSense

**NerveSense** is a surgical proximity device designed to help surgeons detect and avoid peripheral nerves during incision. It estimates the distance between a surgical probe and a nearby nerve in real time, displaying the result on an LCD screen.

> **Disclaimer:** NerveSense is a proof-of-concept prototype developed as a university engineering project. It is not approved for clinical use.

---

## The Problem

Peripheral nerve injuries (PNIs) affect 13–23 people per 100,000 annually in the US, with 8–25% caused directly by medical procedures. Full recovery occurs in only 5.1% of cases. Current nerve-detection technologies (ultrasound, IONM, fluorescent markers) lack real-time, unambiguous proximity sensing — NerveSense addresses this gap.

---

## How It Works

NerveSense is divided into four subsystems: **Signaling → Receiving → Calculating → Displaying.**

```
┌─────────────────────────────────────────────────────────┐
│                    NerveSense System                    │
│                                                         │
│  [TENS Pads] ──► [L298N Driver] ──► Stimulates tissue  │
│       ▲                                    │            │
│  12V Boost                         Compound Action      │
│  (XL6009)                          Potential (CAP)      │
│                                            │            │
│  [Scalpel Electrode (S+)] ◄────── tissue response       │
│  [Reference Electrode (S-)]                │            │
│            │                               │            │
│            └──────► [AD620 Amplifier] ─────┘            │
│                          │ (100x gain)                  │
│                          ▼                              │
│                  [Raspberry Pi Pico]                    │
│                  ADC reads voltage                      │
│                          │                              │
│                          ▼                              │
│                   Distance calculation                  │
│                   d = 20 × e^(−7.21 × ΔV)              │
│                          │                              │
│                          ▼                              │
│                    [20×4 LCD Display]                   │
│             Row 1: Proximity warning                    │
│             Row 2: Distance (cm)                        │
│             Row 3: Voltage                              │
│             Row 4: Delta Voltage                        │
└─────────────────────────────────────────────────────────┘
```

---

### 1. Signaling

Two **TENS unit electrode pads** are placed on the patient's skin over the surgical site. An **L298N motor driver** switches these pads on and off at **20 Hz** — the clinically established frequency for eliciting a Compound Action Potential (CAP) from a nerve. A **XL6009 DC-DC boost module** steps the supply up to **12V** to compensate for the ~40% voltage drop across the pads and skin, ensuring at least 5V reaches the tissue.

A **grounding electrode** was added to the signaling unit to prevent charge buildup in the tissue (which would otherwise behave like a capacitor and corrupt the signal).

### 2. Receiving

When the nerve fires, it produces a CAP — an AC electrical response with a peak voltage of ~100mV. The **scalpel probe (S+)** and a **reference electrode (S-)** measure the voltage difference in the tissue at the surgical site.

Because 100mV is too weak for the Pico's ADC to read directly, the signal passes through an **AD620 instrumentation amplifier module** at a gain of 100×. A custom PCB with an INA333 amplifier and bandpass filter was also designed (using Altium Designer) to isolate the nerve's 20Hz signal — see `/PCB` for design files.

> **PCB Note:** The custom INA333 PCB is a more robust alternative to the AD620 module due to its integrated bandpass filter, which actively filters out non-nerve frequencies and reduces noise. However, if using the PCB, the RG resistor should be swapped to a **1000 Ω resistor** to set the correct gain for this application. Additionally, the PCB in its present state includes **no voltage protection** — adding a clamping circuit or protection resistors before any further use is strongly recommended.

The electrodes are made from **silver wire coated in AgCl** (via reaction with bleach) to minimize capacitive interference — bare stainless steel was found to convert the tissue analogue into a capacitor, skewing readings.

### 3. Calculating

The Raspberry Pi Pico reads ADC samples every millisecond and computes:

- **`baseline`** — average voltage during the first 0.25s (calibration period at startup)
- **`avg_diff_volts`** — average voltage deviation from baseline over the last 250ms window

Distance is estimated using an empirically derived exponential curve fitted to 10 data points (R² = 0.9321):

```
d = 20 × e^(−7.21 × avg_diff_volts)
```

**Proximity thresholds used for display warnings:**

| `avg_diff_volts` | Display Message      |
|------------------|----------------------|
| > 0.40 V         | Close to Nerve       |
| > 0.25 V         | Medium to Nerve      |
| > 0.10 V         | Far to Nerve         |
| ≥ 5V or 0V       | Outside of Site      |

### 4. Displaying

A **20×4 I2C LCD** shows:
- **Row 1:** Proximity warning (e.g., "Close to Nerve")
- **Row 2:** Distance in cm
- **Row 3:** Current voltage reading
- **Row 4:** Delta voltage (`avg_diff_volts`)

---

## Hardware Components

| Component                    | Role                                        |
|------------------------------|---------------------------------------------|
| Raspberry Pi Pico            | Microcontroller / ADC                       |
| L298N Motor Driver (×2)      | Nerve stimulation + testing                 |
| XL6009 DC-DC Boost           | Step up to 12V for signaling                |
| AD620 Amplifier Module       | 100× signal amplification                  |
| 20×4 I2C LCD                 | Distance/voltage display                    |
| TENS Unit Contact Pads       | Stimulating electrodes                      |
| Skintact Electrode Pads (×3) | Receiving electrodes                        |
| AgCl-coated Silver Wire      | Low-capacitance electrode material          |
| Custom PCB (INA333)          | Bandpass filter + amplifier (see `/PCB`)    |

---

## Repository Structure

```
SurgeryNerveSense/
├── CAD/              # STEP files for the scalpel probe, frame, lid, and enclosure
├── PCB/              # PCB design files (Altium), DWG, and design rule check
├── Code/             # MicroPython firmware for the Raspberry Pi Pico
├── README.md         # This file
└── USAGE.md          # Step-by-step operating instructions
```

---

## Limitations & Future Work

- Requires recalibration for different tissue types
- ~10% of samples exhibit voltage spikes
- AgCl electrode coating degrades under sunlight and requires bleach re-coating between uses
- No emergency shut-off or voltage protection circuit

**Suggested future improvements:**
- Replace AD620 with INA333 + proper bandpass filter PCB
- Add voltage protection and emergency shut-off
- Improve UI for clinical accessibility

---

## Team

Developed by **Kona Burgess, Spencer Ozaki, Shreya Chellu, and Rui (Ryan) Geng** as part of the Cornerstone of Engineering II course at Northeastern University London (Spring 2026).

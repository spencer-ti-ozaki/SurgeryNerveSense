# NerveSense — Wiring Reference

All wiring diagrams are based on the final working configuration of NerveSense v1.2. Pin numbers refer to **Raspberry Pi Pico GP pins**.

---

## System Overview

```
                        ┌─────────────┐
         12V Supply ───►│  XL6009     │──► 12V out
                        │  DC Boost   │
                        └─────────────┘
                               │
                               ▼
                        ┌─────────────┐         ┌──────────────────┐
                        │   L298N #1  │──OUT1───►│ Stimulating Pad  │ (TENS, on tissue)
                        │  (Signaling)│──OUT2───►│ Grounding Pad    │ (TENS, on tissue)
                        └─────────────┘         └──────────────────┘
                               ▲
                        ┌──────┴──────┐
                        │ Pico GP13   │ (ENA — PWM speed)
                        │ Pico GP14   │ (IN1)
                        │ Pico GP15   │ (IN2)
                        └─────────────┘

                        ┌─────────────┐         ┌──────────────────┐
                        │   L298N #2  │──OUT1───►│ Shock+ pad       │
                        │  (Testing)  │──OUT2───►│ Shock- pad       │
                        └─────────────┘         └──────────────────┘
                               ▲
                        ┌──────┴──────┐
                        │ Pico GP21   │ (IN3)
                        │ Pico GP19   │ (IN4)
                        └─────────────┘

  ┌──────────────────┐      ┌───────────────┐      ┌─────────────────┐
  │ Scalpel Electrode│──S+─►│  AD620 Module │─OUT─►│  Pico GP26      │
  │      (probe)     │      │  (100× gain)  │      │  (ADC0)         │
  │ Reference Electr.│──S-─►│               │      └─────────────────┘
  └──────────────────┘      └───────────────┘

                        ┌─────────────┐
                        │  20×4 LCD   │
                        │  (I2C)      │
                        └─────────────┘
                               ▲
                        ┌──────┴──────┐
                        │ Pico GP6    │ (SDA)
                        │ Pico GP7    │ (SCL)
                        │ 3.3V / GND  │ (power)
                        └─────────────┘
```

---

## 1. Signaling Unit — L298N #1 to TENS Pads

The signaling unit delivers biphasic pulses to the TENS pads at 20 Hz to elicit a Compound Action Potential (CAP) from nearby nerves.

```
  Raspberry Pi Pico          L298N Motor Driver #1        Electrodes
  ─────────────────          ─────────────────────        ──────────
  GP13 (PWM) ──────────────► ENA                          
  GP14       ──────────────► IN1          OUT1 ──────────► Stimulating TENS Pad
  GP15       ──────────────► IN2          OUT2 ──────────► Grounding TENS Pad
  GND        ──────────────► GND
                             VCC ◄──────────────────────── 12V (from XL6009 boost)
```

> The grounding pad continuously discharges the tissue to prevent capacitive charge buildup, which would corrupt the receiver signal.

---

## 2. Power — XL6009 DC-DC Boost Module

The XL6009 steps an input supply (e.g., a USB power bank or 5V rail) up to 12V to overcome the ~40% voltage drop between the motor driver and the TENS pads.

```
  Input Supply              XL6009 Boost Module         L298N VCC rails
  ────────────              ───────────────────         ───────────────
  5V  ─────────────────────► VIN+                       
  GND ─────────────────────► VIN−         VOUT+ ───────► L298N #1 VCC
                                          VOUT− ───────► L298N #1 GND
                                          VOUT+ ───────► L298N #2 VCC
                                          VOUT− ───────► L298N #2 GND
```

---

## 3. Receiver — Electrodes to AD620 to Pico ADC

The AD620 differential amplifier measures the voltage difference between the scalpel probe and the reference electrode, boosting the ~100mV nerve signal by 100× before the Pico reads it.

```
  Electrodes              AD620 Module              Raspberry Pi Pico
  ──────────              ────────────              ─────────────────
  Scalpel (S+) ─────────► IN+                       
  Reference (S−) ───────► IN−          OUT ────────► GP26 (ADC0)
                           VS+ ◄───────────────────── 3.3V
                           VS− ◄───────────────────── GND
                           REF ◄───────────────────── GND
```

**Gain setting:** The AD620 gain is set by the RG resistor between pins 1 and 8:

```
  Gain = 1 + (49.4kΩ / RG)
  
  For 100× gain:  RG ≈ 499 Ω
```

> If using the **custom INA333 PCB** instead of the AD620 module, swap the RG resistor to **1000 Ω** and add voltage protection before connecting. See `/PCB` for the PCB design files.

---

## 4. Electrode Placement on Tissue

```
  Surgical Site (cross-section view)
  ───────────────────────────────────────────────────────────
  
  ══════════════════ Skin Surface ══════════════════════════
  
  [Grounding Pad]──────────────────────[Stimulating Pad]
       │                                      │
       │         · · · · ·(nerve)· · · ·     │
       │                                      │
       └──────── tissue ──────────────────────┘
                               ▲
                         [Scalpel Probe (S+)]   ← surgeon probes here
  
  [Reference Electrode (S−)] placed far from incision point
  ───────────────────────────────────────────────────────────
```

- **Grounding pad** — flat on skin, over surgical site
- **Stimulating pad** — flat on skin, near incision area
- **Reference electrode (S−)** — far end of surgical site, away from incision
- **Scalpel probe (S+)** — the conductive scalpel blade itself, inserted into incision

---

## 5. LCD Display — I2C

```
  Raspberry Pi Pico          20×4 I2C LCD (address 0x27)
  ─────────────────          ───────────────────────────
  GP6  (SDA) ──────────────► SDA
  GP7  (SCL) ──────────────► SCL
  3.3V       ──────────────► VCC
  GND        ──────────────► GND
```

---

## 6. Full Pin Reference

| Pico GPIO | Function         | Connected To                  |
|-----------|------------------|-------------------------------|
| GP6       | I2C SDA          | LCD SDA                       |
| GP7       | I2C SCL          | LCD SCL                       |
| GP13      | PWM (ENA)        | L298N #1 ENA                  |
| GP14      | Digital OUT (IN1)| L298N #1 IN1                  |
| GP15      | Digital OUT (IN2)| L298N #1 IN2                  |
| GP19      | Digital OUT (IN4)| L298N #2 IN4                  |
| GP21      | Digital OUT (IN3)| L298N #2 IN3                  |
| GP26      | ADC0             | AD620 OUT                     |
| 3.3V      | Power            | LCD VCC, AD620 VS+            |
| GND       | Ground           | All component grounds         |

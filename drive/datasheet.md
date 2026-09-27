# 🚗 REIO-Drive (SPU_105) — Technical Datasheet & Automotive Safety Brief

## 1. Product Overview & Functional Safety Objectives
REIO-Drive (SPU_105) is an ultra-low-latency hardware-based protection shield designed for critical automotive embedded buses, specifically targeting **CAN** (Controller Area Network) and **LIN** (Local Interconnect Network) physical infrastructures.

Engineered to mitigate malicious frame injections, spoofing attacks, and hardware failures (such as *babbling idiot* conditions), the IP core sits inline between the physical layer transceiver and the protocol controller to surgically isolate faulty or compromised nodes.

### Functional Safety Compliance (ISO 26262):
- **Design Philosophy:** Designed as an ultra-minimalist, high-reactivity combinational interceptor. Hardware footprint is restricted to a 2-bit stabilization counter and synchronous output latches, delegating advanced frame decoding and processing validation to the software control plane.

---

## 2. Electrical, Timing & Thermal Metrics (Artix-7)
*Certified post-placement-routing metrics under AMD/Xilinx Vivado v2026.1 targeting the xc7a35tcsg324-1 component (Commercial Temperature Grade).*

| Timing Parameter | Symbol | Target Specification | Validated Slack | Unit |
| :--- | :--- | :--- | :--- | :--- |
| **Core Clock Frequency** | \(f_{CLK}\) | 100.00 | — | MHz |
| **Core Clock Period** | \(T_{CLK}\) | 10.00 | — | ns |
| **Worst Negative Slack (Setup)**| WNS | — | **+7.606** | ns |
| **Worst Hold Slack (Hold)** | WHS | — | **+0.279** | ns |
| **Lockstep Detection Latency**| \(T_{LOCK}\) | **10.00 (Single cycle)**| Compliant | ns |

### Power & Thermal Dissipation Profile:
- **Device Static Power (Vccint, Vccaux):** 72 mW (Hardware static floor).
- **Core Active Dynamic Power (REIO-Core):** < 1 mW.
- **Max Admissible Ambient Temperature ($T_{AMB\_MAX}$):** Validated at **84.6 °C** under standard thermal constraints (ThetaJA = 4.8 C/W, 250 LFM airflow).

---

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*Strict 13-Pin Physical Interface Map validated by Vivado post-synthesis routing (CSG324 Package).*

| Signal Name | Direction | Width | Type | Description / Physical Role |
| :--- | :--- | :--- | :--- | :--- |
| **clk** | Input | 1 bit | STD_LOGIC | Main system clock (100 MHz target, Pin R10) |
| **reset** | Input | 1 bit | STD_LOGIC | Synchronous system hardware reset (Active-High, Pin T10) |
| **flux_data_in[7:0]** | Input | 8 bits | STD_LOGIC_VECTOR | Parallel intercepted high-speed data bus (Pins H14 to A16) |
| **flux_valid_in** | Input | 1 bit | STD_LOGIC | Data valid qualifier strobe signal (Pin V11) |
| **statut_securite** | Output | 1 bit | STD_LOGIC | Hardware Circuit-Breaker status flag ('1' = Nominal, Pin U12) |
| **declencher_secours** | Output | 1 bit | STD_LOGIC | Critical circuit-breaker isolation trigger (Pin V12) |

---

## 📊 4. Behavioral Timing Chronogram & Fault Injection

```text
◀--- Nominal Execution ---▶◀---- Lockstep Mismatch & Fail-Safe Isolation ----
0ns                 10ns                20ns                30ns                40ns

|                   |                   |                   |                   |
   ______              ______              ______              ______              ______
__/      \____________/      \____________/      \____________/      \____________/      \_  SYS_CLK (100 MHz)

XXXXXXXXXX_Nominal_FFF_XXXXXXXXXXXXXXXXXXXXXXXXXXX_Faulty_7FF_XXXXXXXXXXXXXXXXXXXXXXXXXX  CAN_RX_RAW (1 bit)
                                                ▲ (Fault injected during cycle)

_________________________________________________________________
                                                                 \______________________  FAIL_SAFE_MODE (1->0)
                                                                  ▼ (Isolated at next rising edge)

_________________________________________________________________
                                                                 /----------------------  LOCKSTEP_ERR (0->1)
```

---

## ⚖ 5. Commercial Integration & Engineering Services

The REIO-Drive (SPU_105) architecture is part of a high-value engineering portfolio demonstrating professional proficiency in Functional Safety, hardware fault isolation, and RTL synthesis.

*   **Consulting Scope:** Core integration into custom automotive message matrices, Clock Domain Crossing (CDC) hazard mitigation for network boundaries, and documentation support for automotive certification safety cases.
*   **Engagement Model:** Engineering missions are available under contract via freelance platforms or payroll umbrella structures (**SMART Belgium** / direct enterprise contracts).

Use Control + Shift + m to toggle the tab key moving focus. Alternatively, use esc then tab to move to the next interactive element on the page.
Aucun fichier choisi
Attach files by dragging & dropping, selecting or pasting them.

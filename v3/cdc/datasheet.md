# ⛓️ REIO-CDC — Technical Datasheet & Clock Domain Crossing Brief

## 1. Product Overview & Functional Safety Objectives

REIO-CDC is a low-level, high-isolation Clock Domain Crossing (CDC) synchronization IP Core designed for critical heterogeneous System-on-Chip (SoC) architectures. It operates as a **dual physical mitigation barrier** that ensures deterministic signal integrity across independent asynchronous clock boundaries, preventing metastable propagation before feeding the core system plane.

Within the unifed architecture, the module implements two isolated cross-domain pipelines:
*   **Pipeline 1 (High-Speed Network Stream):** Captures and stabilizes critical interrupt indicators coming from the high-frequency **REIO-Chain (400 MHz)** domain down to the unifed System Bus (100 MHz).
*   **Pipeline 2 (Deterministic Automotive Control):** Intercepts and phase-aligns low-frequency safety metrics coming from the autonomous **REIO-Drive (66.67 MHz)** domain up to the unifed System Bus (100 MHz).

### Functional Safety & Metastability Mitigation Invariant:
- **Sequential Metastability Dissipation:** A 3-stage flip-flop cascade dampens the internal oscillatory energy caused by phase shifting or setup/hold violations.
- **Strict Placement Constraining:** Forced structural register proximity prevents cell scattering on the silicon fabric, narrowing skew windows.
- **Active Glitch Shielding:** Intercepts clock gigue and voltage-glitch-induced edge fluctuations to protect downstream crypto and AI coprocessors.

---

## 2. Electrical, Timing & Thermal Metrics (Artix-7)

*Certified hardware metrics extracted from AMD/Xilinx Vivado routed implementation reports targeting the xa7a35tcsg324-1Q device layout.*

### Power & Thermal Dissipation Profile:
- **Total On-Chip Power Consumption:** 0.071 W (71 mW total thermal envelope).
- **Core Dynamic & Static Current Splitting:** 1 mW dynamic / 70 mW static / 0 mW I/O.
- **Junction Temperature (T_J):** 25.3 °C (Max ambient: 124.7 °C).

### Static Timing Analysis (clk_dest_domain @ 100.00 MHz):
- **WNS / WHS / WPWS:** +8.926 ns / +0.131 ns / +4.500 ns (Zero timing violations).
- **Total Hardware Latency Profile:** 3 destination clock cycles (30.00 ns).

---

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*4-pin parallel hardware boundary validated via Vivado post-routing cell distribution.*

| Signal Name | Direction | Width | Type | Description / Physical Role |
| :--- | :---: | :---: | :---: | :--- |
| **CLK_DEST** | Input | 1 bit | STD_LOGIC | Target system domain horloge (100.00 MHz, Destination capture reference) |
| **RESETn_DEST** | Input | 1 bit | STD_LOGIC | Synchronous active-low master master reset line for the 100 MHz plane |
| **ASYNC_IN** | Input | 1 bit | STD_LOGIC | Raw asynchronous input signal originating from a foreign clock layer (400M / 66.6M) |
| **SYNC_OUT** | Output | 1 bit | STD_LOGIC | Hardened, glitch-filtered output line safe for the unifed 100 MHz system bus |

---

## 📊 4. Behavioral Timing Chronogram & Cascaded Stabilization

```text
◀--- Asynchronous Transition ---▶◀-------- 3-Stage Synchronization Latency Loop --------▶
0ns                      10ns                     20ns                     30ns                     40ns

 |                        |                        |                        |                        |
      ______                   ______                   ______                   ______                   ___
_____/      \_______/      \_______/      \_______/      \_______/      \_______/      \_______/      \___  CLK_DEST (100 MHz)
_____________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX________  ASYNC_IN (Unstable)
____________________________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX_________  sync_reg0 (Capture)
_____________________________________________________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX________________  sync_reg1 (Stabilize)
______________________________________________________________________________________/XXXXXXXXXXXXXXXX_______  sync_reg2 (Output)
______________________________________________________________________________________/XXXXXXXXXXXXXXXX_______  SYNC_OUT (Clean)
```

---


# 🔋 REIO-PWR — Technical Datasheet & Power Management Core Brief

## 1. Product Overview & Functional Safety Objectives

REIO-PWR is a low-level, high-reactivity Power-On-Reset (POR) and asynchronous multi-stage sequence controller IP Core designed to secure critical SoC infrastructures against physical fault injections, side-channel power glitching, and under-voltage transient fluctuations. It operates as the ultimate hardware guard ring, monitoring device power stability and enforcing instantaneous global execution freeze to protect cryptographic secrets and logic registers from state corruption.

### Functional Safety & Voltage Integrity Invariant:
- **Asymmetric Graduated Boot Sequence:** Enforces a multi-stage hardware wake-up cascade to ensure structural stabilization of the system interconnect before releasing peripheral acquisition layers and core coprocessors.
- **Inline Glitch Interception:** Continuous monitoring of core and auxiliary voltage supply lines triggers an unconditioned logical collapse if voltage boundaries are breached.
- **Micro-Second Clamping Latency:** Enforces a global system bus freeze and asserts the hardware fault signal in exactly **1 clock cycle (10.00 ns)** upon glitch detection.

---

## 2. Electrical, Timing & Resource Metrics (Artix-7)

*Certified hardware metrics extracted from AMD/Xilinx Vivado routed implementation reports targeting the xa7a35tcsg324-1Q device layout.*

### Power & Thermal Dissipation Profile:
- **Total On-Chip Power Consumption:** 0.071 W (71 mW total thermal envelope).
- **Core Dynamic & Static Current Splitting:** 1 mW dynamic switching logic / 70 mW static core leakage / <1 mW I/O buffer loads.
- **Junction Temperature (\(T_J\)):** 25.3 °C.
- **Maximum Safe Ambient Temperature (\(T_{AMB\_MAX}\)):** 124.7 °C (Automotive Q-Grade Extended Boundary).

### Static Timing Analysis (100.00 MHz Target Clock):
- **Worst Negative Slack (WNS):** **+7.259 ns** (Zero setup violations, required timing metrics met).
- **Worst Hold Slack (WHS):** **+0.212 ns** (Zero timing hold violations).
- **Worst Pulse Width Slack (WPWS):** **+4.500 ns**.
- **Total Hardware Latency Profile:** System isolation and reset clamp asserted in exactly **1 clock cycle (10.00 ns)**.

### Silicon Footprint Allocation:
- **Slice LUTs Utilization:** **14 LUTs** (11 LUT as Logic, 2 LUT combining adjustment, 1 primitive LUT1).
- **Slice Registers Count:** **10 Registers** (10 rising edge-triggered FDCE flip-flops).
- **Unique Control Sets:** 6 unique synchronous control sets.

---

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*8-pin parallel hardware boundary validated via Vivado post-routing cell distribution.*

| Signal Name | Direction | Width | Type | Description / Physical Role |
| :--- | :---: | :---: | :---: | :--- |
| **CLK** | Input | 1 bit | STD_LOGIC | Peripheral system sampling clock input (100.00 MHz, Dedicated Pin F4) |
| **RESETn_PIN** | Input | 1 bit | STD_LOGIC | External master hardware reset line input pin (Pin T10) |
| **VCCINT_STABLE** | Input | 1 bit | STD_LOGIC | Core voltage internal monitor input line ('1' = 1.0V stable, '0' = glitch detected) |
| **VCCAUX_STABLE** | Input | 1 bit | STD_LOGIC | Auxiliary voltage monitor input line ('1' = 1.8V stable, '0' = glitch detected) |
| **RSTn_INTERCONN** | Output | 1 bit | STD_LOGIC | Active-low output driving Stage 1 reset line for REIO-BUS and REIO-CDC |
| **RSTn_PERIPH** | Output | 1 bit | STD_LOGIC | Active-low output driving Stage 2 reset line for CHAIN, DRIVE, SAFE, NVM |
| **RSTn_COPROC** | Output | 1 bit | STD_LOGIC | Active-low output driving Stage 3 reset line for CRYPT and AI execution blocks |
| **PWR_FAULT_FLAG** | Output | 1 bit | STD_LOGIC | High-reactivity physical power fault indicator line output pin (Pin T11) |

---

## 📊 4. Behavioral Timing Chronogram & Séquence Control

```text
◀---- Graduated Power-On-Reset Wake-up Cascade ----▶◀-- Glitch Injection & Global Freeze Clamping --▶
0ns                      100ns                    200ns                    300ns                    400ns

 |                        |                        |                        |                        |
      ______                   ______                   ______                   ______                   ___
_____/      \_______/      \_______/      \_______/      \_______/      \_______/      \_______/      \___  CLK (100 MHz)
___________________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\________  VCCINT_STABLE / VCCAUX
___________________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\________  RESETn_PIN
                           ◀-- 16 Cycles Delay --▶
____________________________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\________  RSTn_INTERCONN (Stage 1)
                                                     ◀-- 16 Cycles Delay --▶
______________________________________________________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\________  RSTn_PERIPH (Stage 2)
                                                                               ____________ 
______________________________________________________________________________/            \________  RSTn_COPROC (Stage 3)
                                                                                            _________
___________________________________________________________________________________________/         \  PWR_FAULT_FLAG (Active)
```

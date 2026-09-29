# 🎛️ REIO-INT — Technical Datasheet & Hardened Interrupt Controller Brief

## 1. Product Overview & Functional Safety Objectives

REIO-INT is a low-level, high-reactivity hardware-enforced interrupt monitoring and rate-limiting IP Core designed to secure critical SoC infrastructure against hardware-level Denial-of-Service (DoS), interrupt flooding, and malicious line-strapping attacks. It acts as an isolation barrier between unconstrained peripheral asynchronous interrupt request (`IRQ`) lines and the core processing plane, enforcing strict execution determinism and protecting CPU availability from adversarial flooding.

### Functional Safety & Intrusion Containment Invariant:
- **Asynchronous Line Rate Limiting:** Continuously tracks input request duty cycles using dual independent 8-bit saturation counters.
- **Surgical Line Disconnection:** If a peripheral breaks the maximum allowed holding threshold (255 clock cycles), the interconnect triggers an unconditioned logical disconnect, crushing that specific output line to **0 Volt** in exactly **1 clock cycle (10.00 ns)**.
- **Hardware Fault Signaling:** Instantly asserts a dedicated physical pin (`INT_FAULT_FLAG`) to signal a severe infrastructure compromise and allow immediate kernel-level containment.

---

## 2. Electrical, Timing & Resource Metrics (Artix-7)

*Certified hardware metrics extracted from AMD/Xilinx Vivado routed implementation reports targeting the xa7a35tcsg324-1Q device layout.*

### Power & Thermal Dissipation Profile:
- **Total On-Chip Power Consumption:** 0.072 W (72 mW total thermal envelope).
- **Core Dynamic & Static Current Splitting:** 1 mW dynamic logic switching / 70 mW static core leakage / 1 mW I/O buffer termination load.
- **Junction Temperature (\(T_J\)):** 25.3 °C.
- **Maximum Safe Ambient Temperature (\(T_{AMB\_MAX}\)):** 124.7 °C (Automotive Q-Grade Extended Boundary).

### Static Timing Analysis (100.00 MHz Target Clock):
- **Worst Negative Slack (WNS):** **+6.543 ns** (Zero setup violations on internal critical paths).
- **Worst Hold Slack (WHS):** **+0.236 ns** (Zero timing hold violations).
- **Worst Pulse Width Slack (WPWS):** **+4.500 ns**.
- **Total Hardware Latency Profile:** Attack isolation and combinatorial output masking executed in exactly **1 clock cycle (10.00 ns)**.

### Silicon Footprint Allocation:
- **Slice LUTs Utilization:** **27 LUTs** (14 LUT2, 10 LUT4, 2 LUT3, and 1 primitive LUT1).
- **Slice Registers Count:** **19 Registers** (19 rising edge-triggered FDCE flip-flops).
- **Arithmetic Carry Blocks (CARRY4):** 4 primitives configured for high-speed counter accumulation.
- **Unique Control Sets:** 4 unique synchronous control sets.

---

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*7-pin parallel hardware boundary validated via Vivado post-routing placement cell map.*

| Signal Name | Direction | Width | Type | Description / Physical Role |
| :--- | :---: | :---: | :---: | :--- |
| **CLK** | Input | 1 bit | STD_LOGIC | Peripheral system sampling clock input (100.00 MHz, Dedicated Pin F4) |
| **RESETn** | Input | 1 bit | STD_LOGIC | Synchronous active-low master reset line input (Pin T10) |
| **IRQ_CHAIN_RAW** | Input | 1 bit | STD_LOGIC | Raw inbound asynchronous interrupt request line originating from REIO-Chain |
| **IRQ_DRIVE_RAW** | Input | 1 bit | STD_LOGIC | Raw inbound asynchronous interrupt request line originating from REIO-Drive |
| **IRQ_CHAIN_SECURE**| Output | 1 bit | STD_LOGIC | Hardened, rate-limited output interrupt line routed to the Core CPU interrupt handler |
| **IRQ_DRIVE_SECURE**| Output | 1 bit | STD_LOGIC | Hardened, rate-limited output interrupt line routed to the Core CPU interrupt handler |
| **INT_FAULT_FLAG** | Output | 1 bit | STD_LOGIC | High-reactivity physical infrastructure flooding alerte indicator output pin (Pin T11) |

---

## 📊 4. Behavioral Timing Chronogram & Intrusion Suppression

```text
◀-------------- Nominal Interrupt Routing Cycles --------------▶◀--- Flooding Breach Detection & Line Masking ---▶
0ns                      10ns                     20ns                     30ns                     2580ns

 |                        |                        |                        |                        |
      ______                   ______                   ______                   ______                   ___
_____/      \_______/      \_______/      \_______/      \_______/      \_______/      \_______/      \___  CLK (100 MHz)
___________________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  RESETn (1)
___________________________/XXXXXXXX\________________________________________________________________________  IRQ_CHAIN_RAW (Nominal)
___________________________/XXXXXXXX\________________________________________________________________________  IRQ_CHAIN_SECURE
                                  ___________________________________________________________________________  IRQ_DRIVE_RAW (Attack)
                                  ____________________________________________________________________\______  IRQ_DRIVE_SECURE (Nominal)
                                   [ Counter: 0x01 -> 0x02 -> 0x03 ... Accumulating up to Threshold 0xFF ]
                                                                                                      _______
_____________________________________________________________________________________________________/       \  INT_FAULT_FLAG
                                                                                                      _______
_____________________________________________________________________________________________________/XXXXXXX  Outbounds (Clamped)
```

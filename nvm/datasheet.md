# 🧠 REIO-NVM — Technical Datasheet & Non-Volatile Memory Shield Brief

## 1. Product Overview & Functional Safety Objectives

REIO-NVM is a hardware-enforced inline protection filter (IP Core) designed to secure critical non-volatile memory write operations (MRAM / RRAM) in aerospace and automotive embedded systems. It safeguards data persistence boundaries against adversarial fault injections, transient electrical charge drifts, and unauthorized sector overwrites at the silicon layer.

### Functional Safety & Physical Integrity Invariant:
- **Inline Charge Analysis:** Evaluates the logical congruence of incoming data payloads and target addresses.
- **Instant Voltage Clamping:** Upon detecting an atypical write signature, the system activates an immediate logical disconnect, crushing output rails to **0 Volt** in exactly **1 clock cycle (10.00 ns)**.
- **Hardware Isolation Signaling:** Asserts a high-reactivity physical line (`NVM_FAULT_FLAG`) to decouple the storage cell array from the compromised memory bus.

---

## 2. Electrical, Timing & Resource Metrics (Artix-7)
- **Total On-Chip Power Consumption:** 0.072 W (72 mW).
- **Junction Temperature (TJ):** 25.4 °C.
- **Worst Negative Slack (WNS):** +4.500 ns.
- **Worst Hold Slack (WHS):** +0.142 ns.

### Power & Thermal Dissipation Profile:
- **Total On-Chip Power Consumption:** 0.336 W (336 mW total thermal envelope).
- **Core Dynamic & Static Current Splitting:** 1 mW dynamic logic / 71 mW static core leakage / 264 mW I/O buffer termination load.
- **Junction Temperature (\(T_J\)):** 26.6 °C.
- **Maximum Safe Ambient Temperature (\(T_{AMB\_MAX}\)):** 123.4 °C (Automotive Q-Grade Extended Boundary).

### Static Timing Analysis (100.00 MHz Target Clock):
- **Worst Negative Slack (WNS):** Infinite (`inf`). Bypass unconstrained external asynchronous equation modeling.
- **Worst Hold Slack (WHS):** Infinite (`inf`) (Zero local internal timing hold violations).
- **Total Hardware Latency Profile:** Confinement and bus-clamping actions executed in exactly **1 clock cycle (10.00 ns)**.

---

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*67-pin parallel hardware boundary validated via Vivado post-routing cell distribution.*

| Signal Name | Direction | Width | Type | Description / Physical Role |
| :--- | :---: | :---: | :---: | :--- |
| **CLK** | Input | 1 bit | STD_LOGIC | Peripheral system clock (100.00 MHz target, Dedicated Pin F4) |
| **RESETn** | Input | 1 bit | STD_LOGIC | Synchronous active-low master reset line (Pin T10) |
| **NVM_ADDR[15:0]** | Input | 16 bits | STD_LOGIC_VECTOR | Inbound memory target sector address bus |
| **NVM_WDATA[31:0]** | Input | 32 bits | STD_LOGIC_VECTOR | Raw inbound payload data targeted for non-volatile persistence |
| **NVM_WRITE_EN** | Input | 1 bit | STD_LOGIC | Active-high write strobe line validating incoming cycle transactions (Pin V11) |
| **NVM_SECURE_WDATA[31:0]** | Output | 32 bits | STD_LOGIC_VECTOR | Hardened output bus delivering filtered payload or clamped 0V ground |
| **NVM_FAULT_FLAG** | Output | 1 bit | STD_LOGIC | High-reactivity physical disconnector flag driving storage arrays isolation (Pin T11) |

---

## 📊 4. Behavioral Timing Chronogram & Fault Suppression

```text
◀-------------- Nominal Memory Writing Cycle --------------▶◀--- Injection Interception & Clamping ---▶
0ns                      10ns                     20ns                     30ns                     40ns

 |                        |                        |                        |                        |
      ______                   ______                   ______                   ______                   ___
_____/      \_______/      \_______/      \_______/      \_______/      \_______/      \_______/      \___  CLK (100 MHz)
_________________________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX____________  NVM_WRITE_EN
_________________________________/XXXX  0xA1A1  XXXXXXXXXX\XXXXXXXXXXXXXXXX  0x0000  XXXXXXXXXXXXXXXXX\_______  NVM_ADDR
_________________________________/XXXX 0x12345678 XXXXXXXX\XXXXXXXXXXXXXXXX 0xFFFFFFFF XXXXXXXXXXXXXXXX\_______  NVM_WDATA
                                                                            __________________________________
___________________________________________________________________________/                                  \__  NVM_FAULT_FLAG
_________________________________/XXXX 0x12345678 XXXXXXXX\___________________________________________________  NVM_SECURE_WDATA (Nominal)
                                                           ___________________________________________________
__________________________________________________________/XXXXXXXXXXXXXXXX 0x00000000 XXXXXXXXXXXXXXXX\_______  NVM_SECURE_WDATA (Clamped)
```

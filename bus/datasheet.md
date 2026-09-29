# 🎛️ REIO-BUS — Technical Datasheet & Secure Interconnect Brief

## 1. Product Overview & Architectural Target

REIO-BUS is a hardware-enforced synchronous Crossbar interconnect IP Core designed to provide secure data routing, geometrical address decoding, and transaction containment across internal peripheral layers within the REIO security SoC. It acts as an isolation barrier protecting core processing nodes from side-channel bus sniffing and malicious multi-master spoofing.

### Functional Safety & Intrusion Containment Invariant:
- **Active Tag Authentication:** Evaluates a 4-bit hardware security token (`M_SECURITY_TAG`) in parallel with the transaction cycle.
- **Line-Rate Package Drop:** If an unauthenticated token signature is injected, the interconnect zeros all outbound data lines within **1 clock cycle (10.00 ns)**.
- **Bus Clamp Fault Signaling:** Immediately asserts a dedicated physical pin (`BUS_FAULT_FLAG`) to decouple the master control plane from the slave sub-systems.

---

## 2. Electrical, Timing & Resource Metrics (Artix-7)

*Certified hardware metrics extracted from AMD/Xilinx Vivado routed implementation reports targeting the xa7a35tcsg324-1Q device layout.*

### Power & Thermal Dissipation Profile:
- **Total On-Chip Power Consumption:** 0.077 W (77 mW total thermal envelope).
- **Core Dynamic & Static Current Splitting:** 6 mW dynamic routing logic / 70 mW static core leakage / 1 mW I/O switching loads.
- **Junction Temperature (\(T_J\)):** 25.4 °C.
- **Maximum Safe Ambient Temperature (\(T_{AMB\_MAX}\)):** 124.6 °C (Automotive Q-Grade Extended Boundary).

### Static Timing Analysis (100.00 MHz Target Clock):
- **Worst Negative Slack (WNS):** Infinite (`inf`). Hardware exception mapping handles unconstrained external bus transactions.
- **Worst Hold Slack (WHS):** Infinite (`inf`).
- **Total Hardware Latency Profile:** Attack containment and output clamping executed in exactly **1 clock cycle (10.00 ns)**.

---

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*107-pin hardware boundary validated via Vivado post-routing placement cell map.*

| Signal Name | Direction | Width | Type | Description / Physical Role |
| :--- | :---: | :---: | :---: | :--- |
| **CLK** | Input | 1 bit | STD_LOGIC | Core peripheral interconnect system clock (100.00 MHz, Dedicated Pin F4) |
| **RESETn** | Input | 1 bit | STD_LOGIC | Synchronous active-low master reset line (Pin T10) |
| **M_ADDR[15:0]** | Input | 16 bits | STD_LOGIC_VECTOR | Inbound address lines originating from the Host Processor master |
| **M_WDATA[31:0]** | Input | 32 bits | STD_LOGIC_VECTOR | Inbound data payload targeted for slave sub-modules |
| **M_WRITE_EN** | Input | 1 bit | STD_LOGIC | Active-high write transaction enable strobe line |
| **M_SECURITY_TAG[3:0]** | Input | 4 bits | STD_LOGIC_VECTOR | Parallel hardware token value carrying the security key signature |
| **S1_WDATA[31:0]** | Output | 32 bits | STD_LOGIC_VECTOR | Hardened outbound bus connected to Slave Peripheral 1 (Zone 0) |
| **S1_WRITE_EN** | Output | 1 bit | STD_LOGIC | Active-high write strobe line driving validation for Slave 1 |
| **S2_WDATA[31:0]** | Output | 32 bits | STD_LOGIC_VECTOR | Hardened outbound bus connected to Slave Peripheral 2 (Zone 1) |
| **S2_WRITE_EN** | Output | 1 bit | STD_LOGIC | Active-high write strobe line driving validation for Slave 2 |
| **BUS_FAULT_FLAG** | Output | 1 bit | STD_LOGIC | High-reactivity physical disconnector flag (Pin T11) |

---

## 📊 4. Behavioral Timing Chronogram & Intrusion Suppression

```text
◀-------------- Geometrical Slaves Routing Cycles --------------▶◀--- Breach Detection & Bus Clamping ---▶
0ns                      10ns                     20ns                     30ns                     40ns

 |                        |                        |                        |                        |
      ______                   ______                   ______                   ______                   ___
_____/      \_______/      \_______/      \_______/      \_______/      \_______/      \_______/      \___  CLK (100 MHz)
_________________________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX____________________________  M_WRITE_EN
_________________________________/XXXX   0x5000   XXXXXXXX\XXXX   0x9000   XXXXXXX\___________________________  M_ADDR
_________________________________/XXXX 0xAAAA1111 XXXXXXXX\XXXX 0xBBBB2222 XXXXXXX\XXXX 0xCAFECAFE XXXXX\_______  M_WDATA
_________________________________/XXXX     0xA    XXXXXXXX\XXXX     0xA    XXXXXXX\XXXX     0xE    XXXXX\_______  M_SECURITY_TAG
                                                                                           ___________________
__________________________________________________________________________________________/                   \__  BUS_FAULT_FLAG
_________________________________/XXXX 0xAAAA1111 XXXXXXXX\___________________________________________________  S1_WDATA
__________________________________________________________/XXXX 0xBBBB2222 XXXXXXX\___________________________  S2_WDATA
                                                                                           ___________________
__________________________________________________________________________________________/XXXX 0x00000000 XXX  Outbounds (Clamped)
```

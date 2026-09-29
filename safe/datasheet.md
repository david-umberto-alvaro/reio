# 🛡️ REIO-Safe — Technical Datasheet & Storage Hardening Brief

## 1. Product Overview & Functional Safety Objectives

REIO-Safe is an ultra-low-latency, hardware-based protection disconnector designed for safety-critical storage controller layers, specifically targeting **Flash and SSD NAND** physical infrastructures.

Engineered to mitigate ransomware threats, malicious mass encryption routines, and unauthorized physical page tampering, the IP core sits inline directly on the interface control plane. It surgically intercepts data traffic to enforce hardwired memory isolation as soon as behavioral anomalies are identified.

### Functional Safety Compliance (ISO 26262):
- **Design Philosophy:** Implemented as a fully registered, zero-glitch synchronous verification engine. The design isolates logic boundaries behind a hardware entropy counter and synchronous latches, passing the runtime context cleanly to the embedded software ecosystem.

---

## 2. Electrical, Timing & Thermal Metrics (Artix-7)

*Certified metrics under AMD/Xilinx Vivado targeting xa7a35tcsg324-1Q (100.00 MHz core clock, WNS +5.222 ns, WHS +0.222 ns).*

### Power & Thermal Dissipation Profile:
- **Device Static & Dynamic Power:** 72 mW / 20 mW (Total 92 mW).
- **Max Ambient Temperature (\(T_{AMB\_MAX}\)):** 124.6 °C (Automotive Q-Grade compliant).
- **Slice LUTs Utilization:** 28 LUTs (0.13% of the device)
- **Slice Registers Count:** 37 Registers (36 rising edge-triggered FDCE and 1 FDPE flip-flops due to register replication for 0xDEADBEEF drive stabilization)

---

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*68-pin parallel interface validated via Vivado post-routing placement (CSG324 Package).*

| Signal Name | Direction | Width | Type | Physical Pin / Description |
| :--- | :---: | :---: | :---: | :--- |
| **PCLK** | Input | 1 bit | STD_LOGIC | Main system clock (Target 100.00 MHz, Dedicated Pin F4) |
| **PRESETn** | Input | 1 bit | STD_LOGIC | Synchronous active-low system reset (Pin T10) |
| **PADDR[31:0]** | Input | 32 bits | STD_LOGIC_VECTOR | Parallel APB peripheral address bus (Virtualized routes) |
| **PSEL** | Input | 1 bit | STD_LOGIC | APB peripheral select line triggering evaluation (Pin V11) |
| **PENABLE** | Input | 1 bit | STD_LOGIC | APB strobe signal validating the transfer cycle (Pin U11) |
| **PWRITE** | Input | 1 bit | STD_LOGIC | Direction control ('1' = Write transaction, Pin V10) |
| **PWDATA[31:0]** | Input | 32 bits | STD_LOGIC_VECTOR | Parallel host write data bus payload (Virtualized routes) |
| **PRDATA[31:0]** | Output | 32 bits | STD_LOGIC_VECTOR | Volatile telemetry data bus (`0xDEADBEEF` on isolation) |
| **PREADY** | Output | 1 bit | STD_LOGIC | Slave ready indicator acknowledging host interface (Pin U12) |
| **PSLVERR** | Output | 1 bit | STD_LOGIC | Critical protocol transaction error exception line (Pin V12) |
| **SIG_FLASH_WRITE_ENABLE** | Output | 1 bit | STD_LOGIC | Dedicated hardwired write voltage cutoff output (Pin T11) |

---

## 📊 4. Behavioral Timing Chronogram & Fault Injection

```text
◀------------------ Nominal Execution ------------------▶◀--- Ransomware Entropy Detection & 0V Cutoff ---▶
0ns                      10ns                     20ns                     30ns                     40ns

 |                        |                        |                        |                        |
      ______                   ______                   ______                   ______                   ___
_____/      \_______/      \_______/      \_______/      \_______/      \_______/      \_______/      \___  PCLK (100 MHz)
XXXXXXXXXXXXXXXXXXXX_Nominal_Write_XXXXXXXXXXXXXXXXXXXXX_Ransomware_Payload_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  PWDATA[31:0]
                                                            ▲ (Malicious write detected at 20ns)
____________________________________________________________
                                                            \________________________________________________  SIG_FLASH_WRITE_ENABLE (1->0V)
                                                            ▼ (Radical hardware cutoff in exactly 1 cycle)
_____________________________________________________________________________________________________________
                                                            /------------------------------------------------  PSLVERR & PRDATA (0xDEADBEEF)
```

---


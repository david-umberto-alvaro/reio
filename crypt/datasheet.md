# 🔑 REIO-Crypt (SPU_106) — Technical Datasheet & Crypto-Accelerator Brief

## 1. Product Overview & Functional Safety Objectives

REIO-Crypt (SPU_106) is a hardware-accelerated coprocesseur engine designed for high-security embedded systems. It specializes in **Zero-Knowledge Proof (ZKP)** generation and **Elliptic Curve Cryptography (ECC)** token enforcement.

Operating on the **Autonomous Heterogeneous Decoupled (AHD)** architectural pattern, the IP core implements inline mathematical pipelines directly connected to a 32-bit peripheral bus. It isolates hardware math execution from the host CPU clock domain to mitigate Side-Channel Attacks (SCA) and active voltage manipulation threats.

### Functional Safety & Physical Immunity (Invariant CIP-V6):
- **Glitch Protection:** Features a dedicated `VOLTAGE_GLITCH_DETECT` physical sensor line. If a fault injection or electrical manipulation occurs, the core triggers an immediate internal hardware reset, clamping the read bus logic to ground and preventing telemetry leakage.

---

## 2. Electrical, Timing & Thermal Metrics (Artix-7)

*Certified hardware metrics extracted from AMD/Xilinx Vivado routed implementation reports targeting the xa7a35tcsg324-1Q device layout.*

### Power & Thermal Dissipation Profile:
- **Total On-Chip Power Consumption:** 0.075 W (75 mW total envelope).
- **Core Dynamic & Static Current Splitting:** 3 mW dynamic toggling / 72 mW static leakage floor.
- **Junction Temperature (\(T_J\)):** 25.4 °C.
- **Maximum Safe Ambient Temperature (\(T_{AMB\_MAX}\)):** 124.6 °C (Automotive Q-Grade Extended Boundary).

---

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*105-pin parallel interface validated via Vivado post-routing placement (CSG324 Package).*

| Signal Name | Direction | Width | Type | Physical Pin / Description |
| :--- | :---: | :---: | :---: | :--- |
| **PCLK** | Input | 1 bit | STD_LOGIC | Main peripheral system clock (Target 100.00 MHz, Dedicated Pin F4) |
| **PRESETn** | Input | 1 bit | STD_LOGIC | Synchronous active-low system reset line (Pin T10) |
| **PADDR[31:0]** | Input | 32 bits | STD_LOGIC_VECTOR | Parallel APB address bus mapping the internal ZK token space |
| **PSEL** | Input | 1 bit | STD_LOGIC | APB peripheral select line initiating transaction validation (Pin V11) |
| **PENABLE** | Input | 1 bit | STD_LOGIC | APB strobe signal validating the current data phase (Pin U11) |
| **PWRITE** | Input | 1 bit | STD_LOGIC | Read/Write control wire ('1' = Write transaction, Pin V10) |
| **PWDATA[31:0]** | Input | 32 bits | STD_LOGIC_VECTOR | Host payload write data bus carrying secret tokens |
| **PRDATA[31:0]** | Output | 32 bits | STD_LOGIC_VECTOR | Host read data bus returning the scellé ZK signature output |
| **PREADY** | Output | 1 bit | STD_LOGIC | Slave ready indicator driving bus wait-state contraction (Pin U12) |
| **PSLVERR** | Output | 1 bit | STD_LOGIC | Slave error exception asserted upon protocol violation or glitch (Pin V12) |
| **VOLTAGE_GLITCH_DETECT** | Input | 1 bit | STD_LOGIC | Physical security sensor tap interface line (Hardwired Pin H14) |
| **SIG_CRYPT_HARD_RESET** | Output | 1 bit | STD_LOGIC | Active hardware disconnector signal forcing system zeroization (Pin T11) |

---

## 📊 4. Behavioral Timing Chronogram & Pipelined Execution

```text
◀------------------ Host Token Injection Phase ------------------▶◀---- 16-Cycle Pipelined ZK Calculation ----▶
0ns                      10ns                     20ns                     30ns                     40ns

 |                        |                        |                        |                        |
      ______                   ______                   ______                   ______                   ___
_____/      \_______/      \_______/      \_______/      \_______/      \_______/      \_______/      \___  PCLK (100 MHz)
_____________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\_____________________________________________  PSEL & PWRITE
XXXXXXXXXXXXXXXXXXXXX_Secret_Token_Payload_(0xA5A5A5A5)_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  PWDATA[31:0]
______________________________________________
                                              \______________________________________________________________  start_zkp_internal (1->0)
________________________________________________________________________
                                                                        \____________________________________  mult_reg (Stage N Product)
_____________________________________________________________________________________________________________
                                                                                             /---------------  proof_ready & PRDATA (0x2990FF53)
```

---

## ⚖ 5. Commercial Integration & Engineering Services

The REIO-Safe (SPU_102) architecture is part of a high-value engineering portfolio, demonstrating specialized expertise in Functional Safety (ISO 26262 ASIL-D), hardware-enforced ransomware isolation, and robust RTL optimization.

- **Scope of Intervention:** Seamless integration of secure IP cores into automotive Flash/NAND flash topologies, mitigation of asynchronous Clock Domain Crossing (CDC) anomalies, and preparation of documentation files for international safety cases.
- **Cooperation Model:** Engineering consultancy and custom IP development services are available under corporate contract agreements, handled transparently through specialized freelancing and wage-portage channels (**SMART Belgium** / direct enterprise agreements).


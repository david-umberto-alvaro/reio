# 🔑 REIO-Crypt — Technical Datasheet & Crypto-Accelerator Brief

## 1. Product Overview & Functional Safety Objectives

REIO-Crypt is a hardware-accelerated coprocesseur engine designed for high-security embedded systems. It specializes in **Zero-Knowledge Proof (ZKP)** generation and **Elliptic Curve Cryptography (ECC)** token enforcement.

Operating on the **Autonomous Heterogeneous Decoupled (AHD)** architectural pattern, the IP core implements inline mathematical pipelines directly connected to a 32-bit peripheral bus. It isolates hardware math execution from the host CPU clock domain to mitigate Side-Channel Attacks (SCA) and active voltage manipulation threats.

### Functional Safety & Physical Immunity (Invariant CIP-V6):
- **Glitch Protection:** Features a dedicated `VOLTAGE_GLITCH_DETECT` physical sensor line. If a fault injection or electrical manipulation occurs, the core triggers an immediate internal hardware reset, clamping the read bus logic to ground and preventing telemetry leakage.

---

## 2. Electrical, Timing & Thermal Metrics (Artix-7)

*Certified hardware metrics extracted from AMD/Xilinx Vivado routed implementation reports targeting the xa7a35tcsg324-1Q device layout.*

### Power & Thermal Dissipation Profile:
- **Total On-Chip Power Consumption:** **11.753 W** (Vivado Out-of-Context default switching activity layout).
- **Core Dynamic & Static Current Splitting:** **11.593 W** dynamic toggling / **0.159 W (159 mW)** static leakage floor.
- **Junction Temperature (\(T_J\)):** **81.2 °C** (Thermal profile calculated under continuous peak math stress).
- **Maximum Safe Ambient Temperature (\(T_{AMB\_MAX}\)):** **68.8 °C** under maximum I/O stress constraints.

---

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*69-pin parallel interface validated via Vivado post-routing placement (Bonded IOB - 36 inputs / 33 outputs).*

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


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
- **Total On-Chip Power Consumption:** **0.077 W** (77 mW total thermal envelope).
- **Core Dynamic & Static Current Splitting:** **6 mW** dynamic routing logic / **70 mW** static core leakage / **1 mW** I/O switching loads.
- **Junction Temperature (\(T_J\)):** **25.4 °C**.
- **Maximum Safe Ambient Temperature (\(T_{AMB\_MAX}\)):** **124.6 °C** (Automotive Q-Grade Extended Boundary).

### ### Static Timing Analysis (100.00 MHz Target Clock):
- **Worst Negative Slack (WNS):** **+4.723 ns** (0 Failing Endpoints sur le domaine synchrone `clk_sys_domain`).
- **Worst Hold Slack (WHS):** **+0.192 ns** (Zéro violation de Hold face aux bruits de tension).
- **Total Hardware Latency Profile:** Attack containment and output clamping executed in exactly **1 clock cycle (10.00 ns)**.

---

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*104-pin hardware boundary validated via Vivado post-routing placement cell map (Bonded IOB - 49.52% device utilization).*

| Signal Name | Direction | Width | Type | Description / Physical Role |
| :--- | :---: | :---: | :---: | :--- |
| **CLK** | Input | 1 bit | STD_LOGIC | Core peripheral interconnect system clock (Target 100.00 MHz, Dedicated Pin F4) |
| **RESETn** | Input | 1 bit | STD_LOGIC | Synchronous active-low master reset line (Pin T10) |
| **S1_PADDR[31:0]** | Input | 32 bits | STD_LOGIC_VECTOR | Inbound address lines originating from the Host Processor master APB bus |
| **S1_PWDATA[31:0]** | Input | 32 bits | STD_LOGIC_VECTOR | Inbound data payload targeted for secured slave sub-modules |
| **S1_PWRITE** | Input | 1 bit | STD_LOGIC | Read/Write control strobe line originating from the host master |
| **S1_PSEL** | Input | 1 bit | STD_LOGIC | APB peripheral select signal validating the transaction address phase |
| **S1_PENABLE** | Input | 1 bit | STD_LOGIC | APB enable strobe signal orchestrating the transaction data phase |
| **S1_PRDATA[31:0]** | Output | 32 bits | STD_LOGIC_VECTOR | Hardened outbound read data bus returning secure filtered data to host |
| **S1_PREADY** | Output | 1 bit | STD_LOGIC | Slave ready indicator locked to '1' for deterministic low-latency access |
| **UART_TXD** | Output | 1 bit | STD_LOGIC | Hardened serial diagnostic transmission outport line (Dedicated Pin U12) |
| **BUS_FAULT_FLAG** | Output | 1 bit | STD_LOGIC | High-reactivity physical disconnector fault exception alert flag (Pin T11) |

---

## 📊 4. Behavioral Timing Chronogram & Intrusion Suppression

```text
       <-- S1 Transaction (OK) --> <--------- Inbound Interception & Clamping --------->
210ns             220ns            270ns                                  290ns

|                 |                |                                      |
  _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _
_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_  CLK (100 MHz)
__________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  S1_PSEL & S1_PENABLE & S1_PWRITE
XXXXXXXXXXXXXXXXXX_Sane_Address_(0x00001000)_XXXXX_Hostile_Target_(0xFFFFFFFF)XXXXXX  S1_PADDR[31:0]
XXXXXXXXXXXXXXXXXX_Log_Payload_A_(0x00000041)XXXXX_Attack_Vector_(0x12345678)XXXXXX  S1_PWDATA[31:0]
__________________________________________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  internal_nvm_fault
                                                  __________________________________  
_________________________________________________/                                  \  BUS_FAULT_FLAG / internal_nvm_fault (1->0)
                  \_______________________________                                    
__________________________________________________\_________________________________  UART_TXD / ST_ISOLATION_CLAMP_STATE
                  /XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\_________________________________  internal_secure_wdata[31:0] (Forced to 0V)
````

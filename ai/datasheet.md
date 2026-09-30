# 🧠 REIO-AI — Technical Datasheet & Neuromorphic Safety Brief

## 1. Product Overview & Functional Safety Objectives

REIO-AI is a hardware-enforced logical protection shield (IP Core) designed for critical autonomous embedded architectures. It specializes in **inline neural hallucination interception**, register drift mitigation, and adversarial injection blocking targeting neuromorphic processing units (NPU/TPU).

Operating on a pure deterministic co-design methodology, the supervisor monitors parallel probabilistic inference streams at the nanosecond layer. It decouples high-level machine learning computation from the safety-critical control plane by asserting physical boundaries directly on the silicon matrix.

### Functional Safety & Physical Immunity Invariant:
- **Anti-Hallucination Filtering:** The hardware layer monitors the logical congruence of incoming neuronal weights. If two naturally antagonistic nodes or conflicting decision fields are asserted simultaneously, the circuit identifies a critical state failure.
- **Instant Core Isolation:** Upon detection of an adversarial contradiction, the internal Finite State Machine (FSM) leaves the nominal path to latch into a secure hardware confinement state (`ST_HALT`) within exactly **1 clock cycle (10.00 ns)**.
- **Active Bus Clamping:** The data routing bus is immediately zeroized and forced to inject an immutable quarantine token (`0xDEADBEEF`), ensuring the host control system is decoupled from aberrant or corrupted NPU metrics.

---

## 2. Electrical, Timing & Thermal Metrics (Artix-7)

*Certified hardware metrics extracted from AMD/Xilinx Vivado routed implementation reports targeting the xa7a35tcsg324-1Q device layout.*

### Power & Thermal Dissipation Profile:
- **Total On-Chip Power Consumption:** **0.098 W** (98 mW total thermal envelope).
- **Core Dynamic & Static Current Splitting:** **26 mW** dynamic switching activity / **72 mW** static silicon leakage floor.
- **Junction Temperature (\(T_J\)):** **25.5 °C.**
- **Maximum Safe Ambient Temperature (\(T_{AMB\_MAX}\)):** **124.5 °C** (Automotive Q-Grade Extended Boundary).

### Static Timing Analysis (100.00 MHz Target Clock):
- **Worst Negative Slack (WNS):** **+7,272 ns** (0 Failing Endpoints). Data path propagation delay clocks at a mere **2.462 ns**.
- **Worst Hold Slack (WHS):** **+0.260 ns** (0 Clock-skew violations).

---

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*102-pin parallel interface validated via Vivado post-routing placement (CSG324 Package).*

| Signal Name | Direction | Width | Type | Description / Physical Role |
| :--- | :---: | :---: | :---: | :--- |
| **CLK** | Input | 1 bit | STD_LOGIC | Main peripheral system clock (Target 100.00 MHz, Dedicated Pin F4) |
| **RESETn** | Input | 1 bit | STD_LOGIC | Synchronous active-low master reset line (Pin T10) |
| **NPU_NEURON_A[31:0]** | Input | 32 bits | STD_LOGIC_VECTOR | Parallel data bus carrying the primary inference probability weight |
| **NPU_NEURON_B[31:0]** | Input | 32 bits | STD_LOGIC_VECTOR | Parallel data bus carrying the antagonistic control weight |
| **NPU_DATA_VALID** | Input | 1 bit | STD_LOGIC | Strobe signal from the NPU validating active inference data (Pin V11) |
| **PRDATA[31:0]** | Output | 32 bits | STD_LOGIC_VECTOR | Secure host bus returning nominal data or the locked quarantine token |
| **PREADY** | Output | 1 bit | STD_LOGIC | Active-high peripheral ready response line driving bus validation (Pin U12) |
| **PSLVERR** | Output | 1 bit | STD_LOGIC | Hardware transaction error asserted upon contradiction state (Pin V12) |
| **SIG_QUARANTINE_ENGAGED** | Output | 1 bit | STD_LOGIC | High-reactivity physical disconnector pin forcing NPU shutdown (Pin T11) |

---

### 4. Behavioral Timing Chronogram & Fault Interception

```text
    <------------ Nominal Inference Stream ------------> <-- Anomaly Detection & Confinement -->
0ns                10ns               20ns               30ns               40ns

|                  |                  |                  |                  |
   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _
__/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_  CLK (100 MHz)
______________________________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  NPU_DATA_VALID
__________________/XXXX 0x00000000 XXXXX_________________/XXXX 0x00000001 XXXXXXXXXXXX  NPU_NEURON_A
_________________________________________________________/XXXX 0x00000001 XXXXXXXXXXXX  NPU_NEURON_B

_________________________________________________________/____________________________  SIG_QUARANTINE_ENGAGED
__________________/XXXX 0x00000000 XXXXX______________________________________________  PRDATA (Nominal)
                                                         \_______/XXXX 0xDEADBEEF XXXX  PRDATA (Quarantine)
```



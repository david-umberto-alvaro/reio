# ⚡ REIO-Chain — Technical Datasheet & Network Firewall Brief

## 1. Product Overview & Architectural Target

REIO-Chain is an ultra-high-speed synchronous hardware network filter IP Core designed for inline packet monitoring, deterministic masking, and line-rate isolation of Layer 3 data streams, decoupling a 125 MHz line data plane from a 400 MHz control plane.

---

## 2. Electrical, Timing & Resource Metrics (Artix-7)

*Certified post-placement-routing metrics under AMD/Xilinx Vivado v2026.1 targeting the xc7a12tlcpg238-2L component (Extended Automotive Temperature Grade).*

- **Core Clock Frequency (Control):** 400.00 MHz (Period: 2.50 ns)
- **Line Clock Frequency (Data):** 125.00 MHz (Period: 8.00 ns)
- **Worst Negative Slack (WNS):** **+0.531 ns** (Zero timing violations on the control plane)
- **Worst Hold Slack (WHS):** **+0.142 ns**
- **Worst Pulse Width Slack (WPWS):** +0.750 ns

### Power & Silicon Footprint Profile:
- **Slice LUTs Utilization:** **52 LUTs** (Post-routing physical optimization, 0.65% of the device)
- **Slice Registers Count:** **153 Registers** (0.96% of the device)
- **Device Static Power:** 56 mW
- **Core Active Dynamic Power (REIO-Core):** 3 mW (Total design dynamic power verified at 3 mW)
- **Total On-Chip Power Consumption:** **59 mW**

---

## 3. Register Map & MMIO Control Plane Interface

| Offset Address | Register Name | Access | Width | Description / Functional Bitfield |
| :---: | :--- | :---: | :---: | :--- |
| **0x00** | REG_CTRL | R/W | 32 bits | [Bit 0]: Software Reset \| [Bit 1]: Force Manual Isolation |
| **0x04** | REG_STATUS | R | 32 bits | [Bit 0]: Security Status ('1'=Nominal, '0'=Isolated) |
| **0x08** | REG_THREAT_SIG | R/W | 8 bits | Target threat signature (Default: 0x7F) |
| **0x0C** | REG_CNT_CLEAN | R | 32 bits | Counter for clean packets |
| **0x10** | REG_CNT_ANOM | R | 32 bits | Counter for blocked anomalies |

---

## 4. Behavioral Timing Chronogram & Invariant Bounds

```text
◀------- Nominal Line Processing -------▶◀---- Surgical Masking (1 Control Cycle Latency) ----▶
0ns                      2.5ns                    5.0ns                    7.5ns                    10.0ns

 |                        |                        |                        |                        |
      ______                   ______                   ______                   ______                   ___
_____/      \_______/      \_______/      \_______/      \_______/      \_______/      \_______/      \___  SYS_CLK (400 MHz)
______________________________________________________________________________________________________________  RESET (Active-High)
XXXXX 0xAA (Valid)  XXXXX 0x7F (Threat)  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  AXIS_TDATA (8b/64b)
                           ▲ (Signature Detected)
 _________________________________________________
                                                  \___________________________________________________________  REG_STATUS [Bit 0] (1->0)
                                                   ▼ (Line Masked on Next Edge)
```

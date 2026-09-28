# ⚡ REIO-Chain — Technical Datasheet & Network Firewall Brief

## 1. Product Overview & Architectural Target
REIO-Chain is an ultra-high-speed synchronous hardware network filter IP Core designed for inline packet monitoring, deterministic masking, and line-rate isolation of Layer 3 data streams, decoupling a 125 MHz line data plane from a 400 MHz control plane.

---

## 2. Electrical, Timing & Resource Metrics (Artix-7)

*Certified post-placement-routing metrics under AMD/Xilinx Vivado v2026.1 targeting the xc7a12tlcpg238-2L component (Extended Automotive Temperature Grade).*

- **Core Clock Frequency (Control):** 400.00 MHz (Period: 2.50 ns)
- **Line Clock Frequency (Data):** 125.00 MHz (Period: 8.00 ns)
- **Worst Negative Slack (WNS):** **+1.596 ns** (Zéro violation sur le plan de contrôle)
- **Worst Pulse Width Slack (WPWS):** +0.750 ns

### Power & Silicon Footprint Profile:

- **Slice LUTs Utilization:** 12 LUTs (0.15% du composant)
- **Slice Registers Count:** 111 Registers (0.69% du composant)
- **Device Static Power:** 58 mW
- **Core Active Dynamic Power (REIO-Core):** 1 mW (Total design dynamic power verified at 2 mW)

---

## 3. Register Map & MMIO Control Plane Interface

| Offset Address | Register Name | Access | Width | Description / Functional Bitfield |
| :--- | :--- | :--- | :--- | :--- |
| `0x00` | `REG_CTRL` | R/W | 32 bits | [Bit 0]: Software Reset \| [Bit 1]: Force Manual Isolation |
| `0x04` | `REG_STATUS` | R | 32 bits | [Bit 0]: Security Status ('1'=Nominal, '0'=Isolated) |
| `0x08` | `REG_THREAT_SIG`| R/W | 8 bits | Target threat signature (Default: `0x7F`) |
| `0x0C` | `REG_CNT_CLEAN` | R | 32 bits | Counter for clean packets |
| `0x10` | `REG_CNT_ANOM`  | R | 32 bits | Counter for blocked anomalies |

---

## 4. Behavioral Timing Chronogram & Invariant Bounds

```text
◀------- Nominal Line Processing -------▶◀---- Surgical Masking (1 Control Cycle Latency) ----
0ns                 2.5ns               5.0ns              7.5ns              10.0ns

|                   |                   |                  |                  |
   ______              ______              ______             ______             ______
__/      \____________/      \____________/      \___________/      \___________/      \_  SYS_CLK (400 MHz)

_________________________________________________________________________________________  RESET (Active-High)

XXXXX  0xAA (Valid)  XXXXX                       0x7F (Threat)  XXXXXXXXXXXXXXXXXXXXXXX  AXIS_TDATA (8b/64b)
                                                        ▲ (Signature Detected)

________________________________________________________
                                                        \______________________________  REG_STATUS [Bit 0] (1->0)
                                                         ▼ (Line Masked on Next Edge)
```

---

## 5. Software Control Plane Integration (Rust no_std)
The IP Core exposes a standard C-FFI boundary through `reio_chain.h`. The bare-metal driver guarantees execution with memory safety and zero dynamic allocation.

---

## 6. Commercial Integration & Portfolio Framework
The REIO-Chain (SPU_103) architecture is part of a professional co-design portfolio demonstrating hardware security filtering and advanced RTL constraints resolution.

*   **Consulting & Custom IP Adaptation:** Tailoring to custom networking fabrics, bus boundaries mitigation (CDC), and driver interfacing.
*   **Engagement Model:** Engineering missions are available under freelance contracts or payroll umbrella structures (**SMART Belgium** / direct enterprise contracts).

💡 **Engineering Note:** The open-core hardware implementation reports are targeted and verified on the xc7a12tlcpg238-2L matrix for physical footprint validation.

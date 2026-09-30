# 🔌 REIO-UART — Technical Datasheet & Hardened Diagnostic Controller Brief

## 1. Product Overview & Functional Safety Objectives
REIO-UART is a hardened hardware-enforced serial input/output communication and monitoring IP Core designed to secure critical SoC infrastructure telemetry against physical buffer overflow attacks and malicious line flooding. It acts as an isolation barrier between unconstrained peripheral diagnostics lines and the core system bus, enforcing processing determinism and preventing processing resource saturation.

### Functional Safety & Isolation Invariant:
- **Asymmetric Hardware Flow Control:** Enforces strict hardware-level data throttling using an internal ring buffer memory array.
- **Surgical Line Disconnection:** If a peripheral breaks the maximum allowed holding frame threshold (4 consecutive bytes), the interconnect triggers an unconditioned logical disconnect, crushing the output line to 0 Volt in exactly 1 clock cycle (10.00 ns).
- **Hardware Fault Signaling:** Instantly asserts a dedicated physical pin (`UART_FAULT_FLAG`) to signal a severe infrastructure compromise and allow immediate kernel-level containment.

---

## 2. Electrical, Timing & Resource Metrics (Artix-7)
*Certified hardware metrics extracted from AMD/Xilinx Vivado routed implementation reports targeting the xa7a35tcsg324-1Q device layout.*

### Power & Thermal Dissipation Profile:
- **Total On-Chip Power Consumption:** 0.071 W (71 mW total thermal envelope).
- **Core Dynamic & Static Current Splitting:** 1 mW dynamic logic switching / 70 mW static core leakage / <1 mW I/O buffer termination load.
- **Junction Temperature (TJ):** 25.3 °C.
- **Maximum Safe Ambient Temperature (TAMB_MAX):** 124.7 °C (Automotive Q-Grade Extended Boundary).

### Static Timing Analysis (100.00 MHz Target Clock):
- **Worst Negative Slack (WNS):** +5.457 ns (Zero setup violations on internal critical paths).
- **Worst Hold Slack (WHS):** +0.218 ns (Zero timing hold violations).
- **Worst Pulse Width Slack (WPWS):** +4.500 ns.
- **Total Hardware Latency Profile:** Attack isolation and combinatorial output masking executed in exactly 1 clock cycle (10.00 ns).

### Silicon Footprint Allocation:
## 2. Electrical, Timing & Resource Metrics (Artix-7)
- **Slice LUTs Utilization:** 44 LUTs (Post-routing physical optimization)
- **Slice Registers Count:** 30 Registers (28 rising edge-triggered FDCE and 2 FDPE flip-flops)
- **Physical Interface Pins Count:** 5 External Hardened Pins (CLK, RESETn, RX, TX, UART_FAULT_FLAG).
- **Vivado Interconnect Mapping:** 45 Bonded IOB detected during stand-alone synthesis due to unencapsulated parallel MMIO data paths.

---

## 🔌 3. Signal Specifications & Hardware I/O Mapping
*5-pin parallel hardware boundary validated via Vivado post-routing placement cell map.*

| Paramètre Physique | Valeur README | Valeur Datasheet | Valeur Rapport Vivado Brut | Statut de Cohérence |
| :--- | :---: | :---: | :---: | :---: |
| **Fréquence Horloge (`clk`)** | 100,00 MHz | 100,00 MHz | 100,00 MHz (Période : 10,0 ns) | **Strictement Conforme** |
| **Worst Negative Slack (WNS)**| +5,457 ns | +5,457 ns | +5,457 ns (Setup respecté) | **Strictement Conforme** |
| **Worst Hold Slack (WHS)** | +0,218 ns | +0,218 ns | +0,218 ns (Marge de hold OK) | **Strictement Conforme** |
| **Slice Registers** | 30 | 30 Registers | 30 Registres (28 FDCE / 2 FDPE)| **Strictement Conforme** |
| **Slice LUTs as Logic** | 44 LUTs | 44 LUTs | 44 LUTs (Post-routage réel) | **Strictement Conforme** |
| **Broches d'I/O Physiques** | 45 IOB * | 45 Pins * | 45 Bonded IOB (Utilisation : 21,43%)| **Strictement Conforme** |
| **Puissance Totale** | 71 mW | 0,071 W | 0,071 W (soit 71 mW) | **Strictement Conforme** |

*\* Note d'infrastructure : Le circuit utilise 5 broches physiques externes pour l'interface série épurée (CLK, RESETn, RX, TX, UART_FAULT_FLAG). Les 40 lignes complémentaires comptabilisées par Vivado correspondent au bus parallèle MMIO interne interconnecté à la matrice Crossbar.*


---

## 📊 4. Behavioral Timing Chronogram & Intrusion Suppression

```text
◀--- Nominal Transmission (115200 Bauds) ---▶◀--- Overrun Breach Detection & Line Clamping ---▶
0ns                      10us                     20us                     30us                     

 |                        |                        |                        |                        
      ______                   ______                   ______                   ______             
_____/      \_______/      \_______/      \_______/      \_______/      \_______/      \___  CLK (100 MHz)
___________________________________________________________________________________________  RESETn (1)
____/XXXXXXXX\_____________________________________________________________________________  UART_WDATA (0xAA)
________________________________________/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  UART_WDATA (Attack)
                                         [ Counter: 0x01 -> 0x02 -> 0x03 -> 0x04 Saturation ]
                                                                                  _________
_________________________________________________________________________________/           UART_FAULT_FLAG (1)
_________________________________________________________________________________\_________  TX (0V Clamped)
```

# 🚗 REIO-Drive — Technical Datasheet & Automotive Safety Brief

## 1. Product Overview & Functional Safety Objectives
REIO-Drive is an ultra-low-latency hardware-based protection shield designed for critical automotive embedded buses, specifically targeting **CAN** (Controller Area Network) and **LIN** (Local Interconnect Network) physical infrastructures.

Engineered to mitigate malicious frame injections, spoofing attacks, and hardware failures (such as *babbling idiot* conditions), the IP core sits inline between the physical layer transceiver and the protocol controller to surgically isolate faulty or compromised nodes.

### Functional Safety Compliance (ISO 26262):
- **Design Philosophy:** Designed as an ultra-minimalist, high-reactivity combinational interceptor. Hardware footprint is restricted to a 2-bit stabilization counter and synchronous output latches, delegating advanced frame decoding and processing validation to the software control plane.

---

## 2. Electrical, Timing & Resource Metrics (Artix-7)
- **Total On-Chip Power Consumption:** 0.081 W (81 mW Vivado Power Profile).
- **Core Dynamic & Static Current Splitting:** 11 mW dynamic switching / 70 mW static core leakage.

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*Interface physique 13 broches validée par routage post-synthèse Vivado (Boîtier CSG324).*


| Nom du Signal | Direction | Largeur | Type | Description / Rôle Physique |
| :--- | :---: | :---: | :---: | :--- |
| **CLK** | Entrée | 1 bit | STD_LOGIC | Horloge système principale (Cadencée à 100.00 MHz, Pin F4) |
| **RESETn** | Entrée | 1 bit | STD_LOGIC | Réinitialisation maître asymétrique active à l'état bas (Pin T10) |
| **drive_ctrl_reg** | Entrée | 32 bits | MMIO_REG | Registre de commande prioritaire (Offset 0x00, Bit d'activation) |
| **drive_speed_reg** | Entrée | 32 bits | MMIO_REG | Registre de mesure de vitesse des actionneurs (Offset 0x04) |
| **fault_flag_reg** | Sortie | 32 bits | MMIO_REG | Registre de statut d'alarme de blocage ou dérive (Offset 0x08) |
| **DRIVE_FAULT_FLAG**| Sortie | 1 bit | STD_LOGIC | Ligne matérielle d'alerte critique d'isolement du disjoncteur (Pin T11) |


## 📊 4. Behavioral Timing Chronogram & Fault Injection

```text
◀---------------- Nominal Execution ----------------▶◀---- Hardware Anomaly Detection & Fail-Safe Isolation ----▶
0ns            15ns           30ns           45ns           60ns           75ns           90ns

 |              |              |              |              |              |              |
    ______         ______         ______         ______         ______         ______         ______
___/      \_______/      \_______/      \_______/      \_______/      \_______/      \_______/      \___ clk (66.67 MHz)
  XXXXXXXXX_Nominal_0xAA_XXXXXXXXXXXXXXXXXXXXXXX_Sabotage_0x7F_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX flux_data_in[7:0]
                                              ▲ (Injection à 30ns)
________________________________________________________________________________________________________
                                                              \_________________________________________ statut_securite (1->0)
                                                               ▼ (Coupure synchrone après 3 cycles à 60ns)
________________________________________________________________________________________________________
                                                              /----------------------------------------- declencher_secours (0->1)
```
                                                      /----------------------------------------- declencher_secours (0->1)


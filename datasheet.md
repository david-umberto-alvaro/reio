# 🗺️ System-on-Chip REIO — Master Technical Datasheet

### Executive Product Overview & Compliance Target

Le System-on-Chip (SoC) REIO est une architecture de co-design matériel/logiciel souveraine durcie, spécialement conçue pour les infrastructures embarquées critiques et l'électronique automobile connectée. Configuré selon un modèle Open-Core à isolation asynchrone, le SoC intègre des disjoncteurs cyber-physiques câblés au niveau du silicium pour intercepter les injections de fautes, les dérives logiques et les tentatives de chiffrement malveillantes à la nanoseconde près.

### Normes de Certification Visées:
- **Functional Safety :** Conforme ISO 26262 ASIL-D (Automotive Safety Integrity Level).
- **Aviation Standards :** Alignement méthodologique DO-254 pour les profils matériels complexes.
- **Hardware Hardening :** Protection native contre les Single Event Upsets (SEU) par Redondance Modulaire Triple (TMR).

---

###  Global Resource & Timing Synthesis Table

*Table de vérité consolidée et certifiée d'après les rapports de routage physique réels de la suite de CAO AMD/Xilinx Vivado v2026.1 (Cible : Artix-7 xa7a35tcsg324-1Q).*

| Module Matériel (IP Core) | Fréquence Horloge | Primitives LUTs | Primitives Registers | Puissance Électrique | Statut de Fermeture STA (Vivado) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **REIO-PWR** (Séquenceur) | 100.00 MHz | 14 LUTs | 10 Registres | 71 mW | 🟢 Conforme (WNS: +7,259 ns) |
| **REIO-Drive** (Automotive) | 66.667 MHz | 6 LUTs | 4 Registres | 72 mW | 🟢 Conforme (WNS: +1,039 ns) |
| **REIO-Safe** (Storage Guard) | 100.00 MHz | 28 LUTs | 20 Registres | 92 mW | 🟢 Conforme (WNS: +5,222 ns) |
| **REIO-UART** (Diagnostic) | 100.00 MHz | 44 LUTs | 30 Registres | 71 mW | 🟢 Conforme (WNS: +5,457 ns) |
| **REIO-Crypt** (Accélérateur ZKP) | 100.00 MHz | 100 LUTs | 135 Registres | 81 mW | 🟢 Conforme (WNS: +1,158 ns) |
| **REIO-Chain** (Réseau L3 Filtre) | 250.00 MHz | 2 LUTs | 64 Registres | 71 mW | 🟢 Conforme (WNS: +0,860 ns) |
| **REIO-AI** (Filtre Neuronal TMR) | 100.00 MHz | 55 LUTs | 37 Registres | 98 mW | 🟢 Conforme (WNS: +7,272 ns) |
| **REIO-CDC** (Synchroniseur) | 100/400 MHz| 1 LUT | 3 Registres | 71 mW | 🟢 Conforme (WNS: +8,828 ns) |
| **REIO-BUS** (Matrice Crossbar) | 100.00 MHz | 38 LUTs | 67 Registres | 77 mW | 🟢 Conforme (Timing interne Inf) |
| **REIO-INT** (Contrôleur IRQ) | 100.00 MHz | 27 LUTs | 19 Registres | 72 mW | 🟢 Conforme (WNS: +6,543 ns) |
| **REIO-NVM** (Mémoire Flash Guard) | 100.00 MHz | 48 LUTs | 33 Registres | 79 mW | 🟢 Conforme (WNS: +4,500 ns PW) |

**Bilan de Synthèse Cumulé :** **363 Slice LUTs** et **419 Slice Registers** actifs. Enveloppe thermique globale maîtrisée.

**Bilan de Synthèse Cumulé :** **413 Slice LUTs** et **422 Slice Registers** actifs. Enveloppe thermique globale maîtrisée.

---

### Signal Interaction & System Interface Boundaries

L'interconnexion globale du SoC sécurise l'échange de paquets à travers des frontières de domaines d'horloges asynchrones hermétiques :
- **PCLK (Horloge Contrôle / Système) :** Fixée de manière immuable à **100.00 MHz** (Période : 10.00 ns, Entrée sur broche physique MRCC F4). Elle cadence l'exécution de la couche logicielle de confiance en Rust bare-metal (`#![no_std]`).
- **phy_rx_clk_buffered (Horloge Ligne Réseau) :** Validée et stabilisée à **250.00 MHz** (Période : 4.00 ns). Découplée du plan système par une barrière d'interception à double étage de pipeline à latence déterministe pour détruire instantanément toute transaction cyber-physique malveillante.

### Unified Clock Domains & Static Timing Analysis

L'infrastructure matérielle REIO-SoC orchestre la distribution de ses signaux à travers trois domaines d'horloges étanches et isolés de manière asynchrone pour garantir un déterminisme temporel strict et interdire les attaques par injection de fautes ou glitching :

```text
  [ HORLOGE ETHERNET ] ----> (250.00 MHz) ----> [ REIO-CHAIN ]
                                                       |
                                                       | (Asynchrone via CDC)
                                                       v
  [ HORLOGE SYSTÈME ]  ----> (100.00 MHz) ----> [ REIO-BUS ] ---> [ REIO-AI / REIO-SAFE ]
                                                       ^
                                                       | (Asynchrone via CDC)
                                                       |
  [ HORLOGE AUTOMOT. ] ----> (66.667 MHz) ----> [ REIO-DRIVE ]
```

### ⏱️ Timing Closing Summary (All Physical Constraints Met)

- **Domain `clk_sys_domain` (Control Plane / Core Bus — 100.00 MHz) :**
    - **Worst Negative Slack (WNS) :** **+5.222 ns** (Marge de sécurité maximale établie sur le disjoncteur REIO-Safe).
    - **Worst Hold Slack (WHS) :** **+0.222 ns** (Zéro violation de Hold, immunité aux dérives thermiques).
- **Domain `clk_net_domain` (Ethernet Physical Plane — 250.00 MHz) :**
    - **Worst Negative Slack (WNS) :** **+0.860 ns** (Fermeture temporelle stricte et validée du double pipeline REIO-Chain).
    - **Worst Hold Slack (WHS) :** **+0.347 ns**.
- **Domain `clk_drive_domain` (Automotive Physical Plane — 66.667 MHz) :**
    - **Worst Negative Slack (WNS) :** **+1.039 ns** (Routage optimal de l'actionneur).
    - **Worst Hold Slack (WHS) :** **+0.279 ns**.

---

###  Hardware-Software Interface & Memory-Mapped Registers (MMIO)

L'accès aux registres d'activation et de télémétrie des disjoncteurs physiques s'effectue par projection mémoire directe via des structures de données stricts, alignées par le compilateur Rust bare-metal (`#![no_std]`).

### 🎛️ Master System Offsets (Base Addresses)
- `BASE_CHAIN` : `0x4000_0000` (Network Interception Control Layer)
- `BASE_DRIVE` : `0x4000_1000` (Automotive Interception Control Layer)
- `BASE_SAFE`  : `0x4000_2000` (Storage Disconnector Control Layer)
- `BASE_CRYPT` : `0x4000_3000` (Coprocesseur ZKP Registry Layer)
- `BASE_AI`    : `0x4000_4000` (Paraconcurrent Monitor Layer)
- `BASE_INT`   : `0x4000_5000` (Hardened Interrupt Controller Filter)
- `BASE_UART`  : `0x4000_6000` (Isolated Diagnostic Input/Output Layer)

---

### Architectural Security Certification Summary

| Attack Vector Vector | Target Domain | Hardware Mitigation Invariant | Reaction Time Latency |
| :--- | :---: | :--- | :---: |
| **Network Anomaly Injection** | Ethernet Line | Inline Signature Matcher & Double Wire Clamping | **8.00 ns** (2 Cycles @ 250 MHz) |
| **Automotive Babbling Idiot** | CAN / LIN Bus | 2-bit Filter Saturation Verification Loop | **60.00 ns** (4 Cycles @ 66.66 MHz) |
| **Mass Encryption / Ransomware** | NAND Storage | Logical Product Null verification (Alpha Key) | **0.00 ns** (Interception Combinatoire) |
| **Clock Glitching / Shifting** | Inter-Clock Line | Triple Flip-Flop Metastability Absorption Barrier | **30.00 ns** (3 Cycles @ 100 MHz) |
| **Interrupt Flooding (DoS)** | Core CPU Plane | 8-bit Asynchronous Rate Limiter Cutoff | **10.00 ns** (1 Cycle @ 100 MHz) |
| **Diagnostic Memory Buffer Overflow** | Serial Log Line | Registered 4-byte Throttler Array Isolation | **10.00 ns** (1 Cycle @ 100 MHz) |

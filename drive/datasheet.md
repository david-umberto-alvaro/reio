# 🚗 REIO-Drive — Technical Datasheet & Automotive Safety Brief

## 1. Product Overview & Functional Safety Objectives
REIO-Drive is an ultra-low-latency hardware-based protection shield designed for critical automotive embedded buses, specifically targeting **CAN** (Controller Area Network) and **LIN** (Local Interconnect Network) physical infrastructures.

Engineered to mitigate malicious frame injections, spoofing attacks, and hardware failures (such as *babbling idiot* conditions), the IP core sits inline between the physical layer transceiver and the protocol controller to surgically isolate faulty or compromised nodes.

### Functional Safety Compliance (ISO 26262):
- **Design Philosophy:** Designed as an ultra-minimalist, high-reactivity combinational interceptor. Hardware footprint is restricted to a 2-bit stabilization counter and synchronous output latches, delegating advanced frame decoding and processing validation to the software control plane.

---

## 2. Electrical, Timing & Thermal Metrics (Artix-7)

*Certified metrics under AMD/Xilinx Vivado targeting xc7a35tcsg324-1 (66.67 MHz core clock, WNS +1.039 ns, WHS +0.279 ns).*

### Power & Thermal Dissipation Profile:
- **Device Static & Dynamic Power:** 72 mW / 2 mW.
- **Max Ambient Temperature ($T_{AMB\_MAX}$):** 84.6 °C.

## 🔌 3. Signal Specifications & Hardware I/O Mapping

*Interface physique 13 broches validée par routage post-synthèse Vivado (Boîtier CSG324).*

| Nom du Signal | Direction | Largeur | Type | Description / Rôle Physique |
| :--- | :---: | :---: | :---: | :--- |
| **clk** | Entrée | 1 bit | STD_LOGIC | Horloge système principale (Cible 66.67 MHz, Pin R10) |
| **reset** | Entrée | 1 bit | STD_LOGIC | Reset matériel synchrone (Actif-Haut, Pin T10) |
| **flux_data_in[7:0]** | Entrée | 8 bits | STD_LOGIC_VECTOR | Bus de données haute vitesse intercepté en parallèle (Pins H14 à A16) |
| **flux_valid_in** | Entrée | 1 bit | STD_LOGIC | Signal stroboscopique de validation des données (Pin V11) |
| **statut_securite** | Sortie | 1 bit | STD_LOGIC | Indicateur d'état du disjoncteur matériel ('1' = Nominal, Pin U12) |
| **declencher_secours** | Sortie | 1 bit | STD_LOGIC | Déclencheur critique d'isolement du disjoncteur (Pin V12) |

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

## ⚖ 5. Commercial Integration & Engineering Services

L'architecture REIO-Drive (SPU_105) fait partie d'un portefeuille d'ingénierie de haute valeur, démontrant une expertise pointue en Sûreté de Fonctionnement (ISO 26262 ASIL-D), isolation de fautes matérielles et synthèse RTL (Vivado).

- **Scope of Intervention:** Seamless integration of secure IP cores into automotive Flash/NAND flash topologies, mitigation of asynchronous Clock Domain Crossing (CDC) anomalies, and preparation of documentation files for international safety cases.
- **Cooperation Model:** Engineering consultancy and custom IP development services are available under corporate contract agreements, handled transparently through specialized freelancing and wage-portage channels 

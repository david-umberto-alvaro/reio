# ⛓️ REIO-Chain (SPU_103)

## Filtre Synchrone d'Interception Réseau & Disjoncteur Matériel (125 MHz / 400 MHz)

REIO-Chain (SPU_103) est un bloc de propriété intellectuelle (IP Core) matériel/logiciel ultra-compact conçu pour l'interception linéaire et le masquage déterministe de flux de données Couche 3 (Layer 3). L'architecture est scindée en un plan de filtrage physique asynchrone cadencé à 125 MHz et un plan de contrôle bare-metal supervisé à 400 MHz.

### 🔬 Performances Matérielles Certifiées (AMD/Xilinx Vivado v2026.1)

Les rapports d'implémentation post-placement-routage sur puce Xilinx Artix-7 (xc7a12tlcpg238-2L) certifient les métriques physiques suivantes :

- **Fréquence Horloge Système (Rust) :** 400 MHz (Période stricte de 2,5 ns)
- **Fréquence Horloge Ligne (Ethernet) :** 125 MHz (Période stricte de 8,0 ns)
- **Worst Negative Slack (WNS) :** +1,596 ns (Setup métrique parfait, zéro violation)
- **Total Negative Slack (TNS) :** 0,000 ns
- **Worst Pulse Width Slack (WPWS) :** +0,750 ns
- **Livrable Temporel :** Coupure réseau déterministe en 1 seul cycle machine

### 🌐 Architecture Fonctionnelle du Pipeline SPU_103

```text
+-------------------------------------------------------+

|                   APPLICATION HÔTE                    |
| (Moteur C++ principal / Couche logicielle du client)  |
+-------------------------------------------------------+
                           |
                           | Liaison Directe (reio_chain.h)
                           v
+-------------------------------------------------------+

|                PILOTE DE CONTRÔLE RUST                |
|     Configuration MMIO & Télémétrie (#![no_std])      |
+-------------------------------------------------------+
                           |
                           | Bus de Contrôle AXI4-Lite
                           v
+=======================================================+

|                       SILICIUM                        |
| ---------------------------------------------------   |
|               DISJONCTEUR MATÉRIEL VHDL               |
|        Confinement & Masquage Réseau (Artix-7)        |
|                                                       |
|   [12 Slice LUTs]                 [111 Registers]     |
|   [Horloge : 400 MHz]             [WNS : +1,596 ns]   |
+=======================================================+
                           ^
                           | Flux Réseau Linéaire AXI-Stream
                    [ LIGNE ETHERNET ]
```

### 📊 Validation Fonctionnelle & Formes d'Ondes (Testbench RTL)

![Chronogramme des formes d'ondes REIO-Chain](reio_chain_simulation_waveform.png)

### 📊 Empreinte Géométrique & Signature Thermique

- **Slice LUTs :** 12 (0,15% du composant)
- **Slice Registers :** 111 (0,69% du composant)
- **Primitives Hardware :** 111 FDCE flip-flops, 24 blocs CARRY4
- **Puissance Électrique Totale :** 58 mW (Puissance dynamique active du cœur : 1 mW)
- **I/O Physiques :** Configuration d'entrées/sorties routées sous contrainte de délai LVCMOS33

### 🛠 Architecture du Framework Unifié

1. **RTL Core (VHDL) :** Pipeline d'interception directe parallèle s'interfaçant avec un bus physique Ethernet. Intègre un bloc de protection contre les inversions d'états, un disjoncteur matériel à verrouillage et une matrice de Télémétrie Multi-Secteurs synchrone.
2. **Control Plane (Rust 2024) :** Pilote autonome s'exécutant sous contraintes strictes `#![no_std]`, effectuant des lectures directes et volatiles par mappage mémoire MMIO, calculant les ratios de corruption en arithmétique entière fixe.
3. **Host Interface (C-FFI) :** Exportation des bindings via un en-tête C (`reio_chain.h`) exploitant des structures unifiées et alignées à 32 octets sur les lignes de cache CPU.

*⚖️ Conformément aux clauses de propriété intellectuelle et de confidentialité, les fichiers de code source (.vhd, .rs) restent strictement confidentiels. Les rapports physiques d'utilisation CAO (.rpt), les résumés des contraintes de timing et les chronogrammes de simulation comportementale sont accessibles en Open-Core.*

# ⛓️ REIO-Chain
# ⛓️ REIO-Chain

## Filtre Synchrone d'Interception Réseau & Disjoncteur Matériel (100 MHz / 250 MHz)

REIO-Chain est un IP Core matériel/logiciel pour l'interception et le masquage de flux Couche 3, combinant un plan de filtrage asynchrone à 250 MHz et un plan de contrôle à 100 MHz.

### 🔬 Performances Matérielles Certifiées (AMD/Xilinx Vivado v2026.1)

Implémentation sur Xilinx Artix-7 (xc7a12tlcpg238-2L) :
- **Fréquence Système (Rust) :** 100 MHz
- **Fréquence Ligne (Ethernet) :** 250 MHz
- **Worst Negative Slack (WNS) :** **+0,860 ns**
- **Worst Hold Slack (WHS) :** **+0,347 ns**
- **Puissance Totale :** **71 mW** (Dynamique : 13 mW, Statique : 58 mW)

### 🌐 Architecture Fonctionnelle du Pipeline

```text
+-------------------------------------------------------+

|                   APPLICATION HÔTE                    |
| (Moteur C++ principal / Couche logicielle du client)  |
+-------------------------------------------------------+
                           |
                           | Liaison Directe (reio_chain.h)
                           v
+-------------------------------------------------------+

|               PILOTE DE CONTRÔLE RUST                 |
|     Configuration MMIO & Télémétrie (#![no_std])      |
+-------------------------------------------------------+
                           |
                           | Bus de Contrôle AXI-Lite
                           v
+=======================================================+

|                       SILICIUM                        |
| ----------------------------------------------------- |
|              DISJONCTEUR MATÉRIEL VHDL                |
|      Confinement & Masquage Réseau (Artix-7)          |
|                                                       |
|   [2 Slice LUTs]                     [64 Registers]   |
|   [Horloge : 250 MHz]                [WNS : +0,860 ns]|
+=======================================================+
                           ^
                           | Flux Réseau Linéaire AXI-Stream
                   [ LIGNE ETHERNET ]
```

### 📊 Validation Fonctionnelle & Formes d'Ondes (Testbench RTL)

![Chronogramme des formes d'ondes REIO-Chain](reio_chain_simulation_waveform.png)

### 🛠 Architecture du Framework Unifié

1. **RTL Core (VHDL) :** Pipeline d'interception directe parallèle s'interfaçant avec un bus physique Ethernet. Intègre un bloc de protection contre les inversions d'états, un disjoncteur matériel à verrouillage et une matrice de Télémétrie Multi-Secteurs synchrone.
2. **Control Plane (Rust 2024) :** Pilote autonome s'exécutant sous contraintes strictes `#![no_std]`, effectuant des lectures directes et volatiles par mappage mémoire MMIO, calculant les ratios de corruption en arithmétique entière fixe.
3. **Host Interface (C-FFI) :** Exportation des bindings via un en-tête C (`reio_chain.h`) exploitant des structures unifiées et alignées à 32 octets sur les lignes de cache CPU.


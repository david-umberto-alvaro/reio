# REIO-Drive (SPU_105)

## Filtre Synchrone d'Interception Réseau & Disjoncteur Matériel (Couplage Direct Stream 100 MHz).

REIO-Drive (SPU_105) est un bloc de propriété intellectuelle (IP Core) matériel/logiciel conçu pour l'interception linéaire, le filtrage de messages au niveau matériel et la coupure déterministe ultra-rapide sur les réseaux multiplexés automobiles CAN/LIN. L'architecture est scindée en un plan de filtrage physique tolérant aux pannes (Lockstep) et un plan de contrôle bare-metal supervisé en Rust.

### 🔬 Performances Matérielles Certifiées (AMD/Xilinx Vivado v2026.1)

Les rapports d'implémentation post-placement-routage sur la matrice AMD/Xilinx Artix-7 certifient les métriques physiques et de sûreté suivantes :

- **Fréquence Horloge Système (Rust) :** Chemin de timing fermé avec succès à **100.00 MHz** (Période : **10.00 ns**).
- **Worst Negative Slack (WNS) :** Entièrement stabilisé dans le vert à **+7.606 ns** (Zéro violation de chemin).
- **Worst Hold Slack (WHS) :** Délais de routage intra-site parfaitement optimisés à **+0.279 ns**.
- **Livrable Temporel :** Coupure réseau déterministe en **1 seul cycle machine** (latence d'un cycle d'horloge).

```text
+--------------------------------------------------------+

|                    APPLICATION HÔTE                    |
|   (Environnement AUTOSAR / Calculateur de Véhicule)    |
+--------------------------------------------------------+
                            |
                            | Liaison Directe (C-FFI Bridge)
                            v
+--------------------------------------------------------+

|                PILOTE DE CONTRÔLE RUST                 |
|   Configuration MMIO & Verrou Temporel (#![no_std])    |
+--------------------------------------------------------+
                            |
                            | Bus de Contrôle AMBA APB
                            v
+========================================================+

|                        SILICIUM                        |
| ------------------------------------------------------ |
|               DISJONCTEUR MATÉRIEL VHDL                |
|      Isolation du Bus & Machine d'États Lockstep       |
|                                                        |
|   [Optimized Slice LUTs]          [Registers]          |
|   [Single-Cycle Mitigation]       [Zero Violations]    |
+========================================================+
                            ^
                            | Interception Parallèle Haute Vitesse
                            | [ BUS CAN / LIN ]
```

### 📊 Validation Fonctionnelle & Formes d'Ondes (Testbench RTL)

![Chronogramme des formes d'ondes REIO-Drive](reio_drive_simulation.png)

### 📊 Empreinte Géométrique & Signature Thermique

- **Utilisation des ressources logiques :** Empreinte matérielle ultra-compacte validée à **6 Slice LUTs** (0.03% de la matrice) et **4 Slice Registers** (<0.01%).
- **Primitives Hardware :** Bascules synchrones (`FDRE`/`FDSE`) couplées à des macros logiques d'optimisation.
- **Puissance Électrique Totale :** Consommation statique fixe mesurée à **72 mW** (`Device Static Power`), avec une dissipation active du cœur dynamique inférieure à **1 mW**.
- **I/O Physiques :** Configuration de **13 broches physiques** (11 ports d'entrée `IBUF`, 2 ports de sortie `OBUF`) routées sous des contraintes électriques strictes.

### 🛠 Architecture du Framework Unifié

1. **RTL Core (VHDL) :** Pipeline d'évaluation de flux à haute vitesse s'interfaçant nativement avec les lignes du contrôleur de communication. Intègre une FSM en mode Lockstep pour contrer les pannes transitoires induites par les radiations (SEU) et un disjoncteur matériel forçant un état sécurisé.
2. **Control Plane (Rust 2024) :** Pilote autonome s'exécutant sous des contraintes strictes `#[no_std]`, effectuant des lectures directes et volatiles par mappage mémoire MMIO, sécurisant la période d'évaluation via un verrou temporel cryptographique immuable.
3. **Host Interface (C-FFI) :** Pont de liaisons C directes exportant des points d'intégration explicites compatibles avec les systèmes d'exploitation automobiles standards et les couches d'exécution temps réel.

*⚖️ Conformément aux clauses de propriété intellectuelle et de confidentialité, les fichiers de code source (.vhd, .rs) restent strictement confidentiels. Les rapports physiques d'utilisation CAO (.rpt), les résumés des contraintes de timing et les chronogrammes de simulation comportementale sont accessibles en Open-Core.*

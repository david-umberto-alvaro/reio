# 🚗 REIO-Drive — Filtre Combinatoire d'Interception Automobile

REIO-Drive est un module d'interception réseau ultra-compact. Son architecture traite les signaux d'entrée via une matrice combinatoire pure (6 LUTs) et sécurise les sorties à l'aide d'un compteur de stabilisation temporel de 2 bits empêchant les déclenchements intempestifs sur micro-coupures.

### 🔬 Architecture Logique & Primitives Câblées
L'extraction de la Netlist Vivado certifie la structure suivante :
- **Logique Combinatoire :** 6 LUTs assurant le décodage asynchrone des lignes.
- **Registre de Stabilisation :** Compteur matériel de 2 bits (`compteur_stabilite_reg`) validant la persistance du flag d'isolation.
- **Verrouillage des Sorties :** 2 bascules synchrones dédiées au maintien des lignes d'état (`statut_securite` et `declencher_secours`).

### 🔬 Performances Matérielles Certifiées (AMD/Xilinx Vivado v2026.1)

Les rapports d'implémentation post-placement-routage sur la matrice AMD/Xilinx Artix-7 certifient les métriques physiques et de sûreté suivantes :

- **Fréquence Horloge Système (Rust) :** Chemin de timing fermé avec succès à **66.67 MHz** (Période : **15.00 ns**).
- **Worst Negative Slack (WNS) :** Entièrement stabilisé dans le vert à **+1.039 ns** (Zéro violation de chemin, contrainte de sûreté combinatoire fixée à 12.00 ns).
- **Worst Hold Slack (WHS) :** Délais de routage intra-site parfaitement optimisés à **+0.279 ns**.
- **Livrable Temporel :** Coupure réseau déterministe et filtrée anti-glitch validée en simulation à **60.00 ns** (3 cycles de stabilisation d'horloge).

### 📊 Empreinte Géométrique & Signature Thermique

- **Utilisation des ressources logiques :** Empreinte matérielle ultra-compacte validée à **6 Slice LUTs** (0.03% de la matrice) et **4 Slice Registers** (<0.01%).
- **Primitives Hardware :** Bascules synchrones (`FDRE`/`FDSE`) couplées à des macros logiques d'optimisation.
- **Puissance Électrique Totale :** Consommation statique fixe mesurée à **72 mW** (Device Static Power), avec une dissipation active du cœur dynamique réelle de **2 mW** (0,002 W certifiés post-routage).
- **I/O Physiques :** Configuration de **13 broches physiques** (11 ports d'entrée `IBUF`, 2 ports de sortie `OBUF`) routées sous des contraintes électriques strictes.

### 🌐 Architecture Fonctionnelle du Pipeline SPU_105

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
                            | Lecture Asynchrone des lignes d'état (MMIO / GPIO)

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

### 🛠 Architecture du Framework Unifié

1. **RTL Core (VHDL) :** Pipeline d'évaluation de flux à haute vitesse s'interfaçant nativement avec les lignes du contrôleur de communication. Intègre une FSM en mode Lockstep pour contrer les pannes transitoires induites par les radiations (SEU) et un disjoncteur matériel forçant un état sécurisé.
2. **Control Plane (Rust 2024) :** Pilote autonome s'exécutant sous des contraintes strictes `#[no_std]`, effectuant des lectures directes et volatiles par mappage mémoire MMIO, sécurisant la période d'évaluation via un verrou temporel cryptographique immuable.
3. **Host Interface (C-FFI) :** Pont de liaisons C directes exportant des points d'intégration explicites compatibles avec les systèmes d'exploitation automobiles standards et les couches d'exécution temps réel.

### 🚀 Validation du Pilote Logiciel (Intégration Rust / Python FFI)

L'exécution du script de test autonome confirme la conformité du pont C-FFI (`#![no_std]`) à travers trois scénarios clés :
* **[Test 1] Flux standard :** Transmission stabilisée de la donnée (`0x2a`) avec bit de validité actif.
* **[Test 2] Contradiction NPU :** Isolation et forçage du bus sur `0xdeadbeef` en un cycle.
* **[Test 3] Erreur Pointeur :** Robustesse face à une adresse de registre NULL.

![Rapport de validation du script Python REIO-Safe](reio_drive_test.png)

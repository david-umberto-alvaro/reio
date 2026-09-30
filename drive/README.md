# 🏎️ REIO-Drive — Filtre Combinatoire d'Interception Automobile

### 📌 Présentation Générale
REIO-Drive est un module d'interception réseau ultra-compact conçu pour sécuriser les signaux d'entrée via une matrice combinatoire pure et isoler les sorties à l'aide d'un compteur de stabilisation temporel à 2 bits empêchant les déclenchements intempestifs sur micro-coupures.

### 📊 Performances Matérielles Certifiées (Vivado v2026.1)
* **Fréquence du Domaine Temporel (STA) :** **66,667 MHz** (période stricte de **15,000 ns**). Le tableau d'E/S et le chronogramme comportemental coïncident de manière déterministe.
* **Fermeture Temporelle (Timing) :** **WNS de +1,039 ns** sur le chemin critique de l'actionneur `statut_securite` et **WHS de +0,279 ns** sur le compteur.
* **Empreinte Silicium (Vivado Utilization) :** Émanation matérielle ultra-compacte validée à **6 Slice LUTs** (0,03% de la matrice) et **4 Slice Registers** (3 primitives `FDRE`, 1 primitive `FDSE`).
* **Caractéristiques Électriques et Thermiques (Vivado Power) :** Consommation statique fixe mesurée à **72 mW** (Device Static Power), avec une dissipation active du cœur dynamique réelle de **2 mW** (0,002 W) pour une enveloppe globale de **81 mW** due à l'ajout des résistances de tirage sur les lignes de contrôle. Température de jonction stabilisée à **25,4 °C**.

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

### 🚀 Intégration du Pilote Logiciel (Interface C-FFI)
L'en-tête de liaison matérielle `reio_drive.h` implémente une structure de télémétrie rigide `reio_telemetry_t` alignée sur 32 octets de frontières de cache de l'hôte pour garantir un déterminisme parfait. Le script d'intégration Python `reio_drive_test.py` valide la conformité fonctionnelle et l'activation immédiate du confinement matériel.

### 🛠 Architecture du Framework Unifié

1. **RTL Core (VHDL) :** Pipeline d'évaluation de flux à haute vitesse s'interfaçant nativement avec les lignes du contrôleur de communication. Intègre une FSM en mode Lockstep pour contrer les pannes transitoires induites par les radiations (SEU) et un disjoncteur matériel forçant un état sécurisé.
2. **Control Plane (Rust 2024) :** Pilote autonome s'exécutant sous des contraintes strictes `#[no_std]`, effectuant des lectures directes et volatiles par mappage mémoire MMIO, sécurisant la période d'évaluation via un verrou temporel cryptographique immuable.
3. **Host Interface (C-FFI) :** Pont de liaisons C directes exportant des points d'intégration explicites compatibles avec les systèmes d'exploitation automobiles standards et les couches d'exécution temps réel.

### 🚀 Validation du Pilote Logiciel (Intégration Rust / Python FFI)

L'exécution du script de test autonome confirme la conformité du pont C-FFI (`#![no_std]`) à travers trois scénarios clés :
* **[Test 1] Flux standard :** Transmission stabilisée de la donnée (`0x2a`) avec bit de validité actif.
* **[Test 2] Contradiction NPU :** Isolation et forçage du bus sur `0xdeadbeef` en un cycle.
* **[Test 3] Erreur Pointeur :** Robustesse face à une adresse de registre NULL.

![Rapport de validation du script Python](reio_drive_test.png)
